import os
import json
import tempfile
from datetime import datetime
import speech_recognition as sr
from pydub import AudioSegment
import numpy as np
from django.conf import settings


class VoiceProcessingService:
    """Service for processing voice claims"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.supported_formats = ['.wav', '.mp3', '.m4a', '.ogg']
    
    def process_voice_claim(self, audio_file_path):
        """Process voice claim audio file"""
        result = {
            'success': False,
            'transcript': '',
            'confidence': 0.0,
            'keywords': [],
            'sentiment_score': 0.0,
            'sentiment_label': 'neutral',
            'emotion_scores': {},
            'recording_quality': 'unknown',
            'word_count': 0,
            'speaking_rate': 0.0,
            'duration': 0
        }
        
        try:
            # Convert audio to WAV if needed
            wav_path = self._convert_to_wav(audio_file_path)
            
            # Get audio duration
            audio = AudioSegment.from_file(wav_path)
            result['duration'] = len(audio) / 1000  # Convert to seconds
            
            # Analyze audio quality
            result['recording_quality'] = self._analyze_audio_quality(audio)
            
            # Transcribe audio
            transcript_data = self._transcribe_audio(wav_path)
            result['transcript'] = transcript_data.get('text', '')
            result['confidence'] = transcript_data.get('confidence', 0.0)
            
            if result['transcript']:
                # Extract keywords
                result['keywords'] = self._extract_keywords(result['transcript'])
                
                # Calculate word count and speaking rate
                words = result['transcript'].split()
                result['word_count'] = len(words)
                result['speaking_rate'] = (len(words) / result['duration']) * 60 if result['duration'] > 0 else 0
                
                # Analyze sentiment
                sentiment_result = self._analyze_sentiment(result['transcript'])
                result['sentiment_score'] = sentiment_result['score']
                result['sentiment_label'] = sentiment_result['label']
                result['sentiment_scores'] = sentiment_result.get('scores', {})
                
                # Detect emotions
                result['emotion_scores'] = self._detect_emotions(result['transcript'])
                
                result['success'] = True
            
            # Cleanup temporary file
            if wav_path != audio_file_path:
                os.remove(wav_path)
                
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _convert_to_wav(self, audio_file_path):
        """Convert audio file to WAV format"""
        if audio_file_path.lower().endswith('.wav'):
            return audio_file_path
        
        try:
            audio = AudioSegment.from_file(audio_file_path)
            temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            audio.export(temp_wav.name, format='wav')
            return temp_wav.name
        except Exception as e:
            raise Exception(f"Audio conversion failed: {str(e)}")
    
    def _analyze_audio_quality(self, audio_segment):
        """Analyze audio quality"""
        try:
            # Calculate loudness
            dBFS = audio_segment.dBFS
            
            # Calculate noise level (simplified)
            samples = np.array(audio_segment.get_array_of_samples())
            noise_level = np.std(samples[:1000]) if len(samples) > 1000 else np.std(samples)
            
            if dBFS > -20 and noise_level < 1000:
                return 'good'
            elif dBFS > -30 and noise_level < 5000:
                return 'fair'
            else:
                return 'poor'
        except:
            return 'unknown'
    
    def _transcribe_audio(self, wav_file_path):
        """Transcribe audio to text"""
        try:
            with sr.AudioFile(wav_file_path) as source:
                audio_data = self.recognizer.record(source)
                
                # Try Google Speech Recognition first
                try:
                    text = self.recognizer.recognize_google(audio_data, language='en-NG')
                    return {'text': text, 'confidence': 0.9, 'engine': 'google'}
                except:
                    pass
                
                # Fallback to Sphinx (offline)
                try:
                    text = self.recognizer.recognize_sphinx(audio_data)
                    return {'text': text, 'confidence': 0.6, 'engine': 'sphinx'}
                except:
                    pass
                
                return {'text': '', 'confidence': 0.0, 'engine': 'none'}
                
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")
    
    def _extract_keywords(self, text):
        """Extract keywords from transcript"""
        # Common insurance keywords
        insurance_keywords = {
            'accident', 'crash', 'collision', 'damage', 'broken', 'stolen',
            'theft', 'robbery', 'burglary', 'fire', 'flood', 'water',
            'hospital', 'doctor', 'sick', 'illness', 'injury', 'pain',
            'emergency', 'urgent', 'immediate', 'serious', 'severe',
            'witness', 'police', 'report', 'case', 'investigation',
            'repair', 'replace', 'cost', 'expensive', 'value', 'money'
        }
        
        # Nigerian specific keywords
        nigerian_keywords = {
            'naija', 'lagos', 'abuja', 'port harcourt', 'kano',
            'okada', 'keke', 'danfo', 'molue', 'boda boda',
            'area boys', 'lastma', 'frsc', 'efcc', 'ndlea'
        }
        
        words = text.lower().split()
        found_keywords = []
        
        for word in words:
            if word in insurance_keywords and word not in found_keywords:
                found_keywords.append(word)
        
        # Check for Nigerian location mentions
        for location in nigerian_keywords:
            if location in text.lower() and location not in found_keywords:
                found_keywords.append(location)
        
        return found_keywords[:10]  # Return top 10 keywords
    
    def _analyze_sentiment(self, text):
        """Analyze sentiment of text"""
        # Simple sentiment analysis
        positive_words = {'good', 'great', 'excellent', 'happy', 'satisfied', 
                         'thank', 'thanks', 'helpful', 'quick', 'fast'}
        negative_words = {'bad', 'terrible', 'awful', 'angry', 'frustrated',
                         'slow', 'late', 'problem', 'issue', 'complaint',
                         'pain', 'hurt', 'damage', 'lost', 'stolen'}
        
        words = text.lower().split()
        pos_count = sum(1 for word in words if word in positive_words)
        neg_count = sum(1 for word in words if word in negative_words)
        
        total = pos_count + neg_count
        if total > 0:
            score = (pos_count - neg_count) / total
        else:
            score = 0
        
        # Normalize to -1 to 1 range
        score = max(-1, min(1, score))
        
        if score > 0.3:
            label = 'positive'
        elif score < -0.3:
            label = 'negative'
        else:
            label = 'neutral'
        
        return {
            'score': score,
            'label': label,
            'scores': {
                'positive': pos_count,
                'negative': neg_count,
                'neutral': len(words) - pos_count - neg_count
            }
        }
    
    def _detect_emotions(self, text):
        """Detect emotions in text (simplified)"""
        # Emotion keywords
        emotion_keywords = {
            'anger': {'angry', 'mad', 'furious', 'rage', 'annoyed'},
            'fear': {'scared', 'afraid', 'frightened', 'terrified', 'panic'},
            'sadness': {'sad', 'unhappy', 'depressed', 'cry', 'tears'},
            'joy': {'happy', 'joy', 'delighted', 'pleased', 'excited'},
            'surprise': {'surprised', 'shocked', 'amazed', 'astonished'}
        }
        
        words = text.lower().split()
        emotion_scores = {}
        
        for emotion, keywords in emotion_keywords.items():
            count = sum(1 for word in words if word in keywords)
            emotion_scores[emotion] = count
        
        return emotion_scores