// Updated AIOrb.jsx with real recording
import React, { useState, useRef, useEffect } from 'react';
import { FiMic, FiMicOff, FiCheck, FiAlertCircle, FiUpload } from 'react-icons/fi';

const AIOrb = ({ onRecordingComplete }) => {
  const [recordingState, setRecordingState] = useState('idle');
  const [audioURL, setAudioURL] = useState('');
  const [transcript, setTranscript] = useState('');
  const [recordingTime, setRecordingTime] = useState(0);
  
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const streamRef = useRef(null);
  const timerRef = useRef(null);

  const startRecording = async () => {
    try {
      setRecordingState('listening');
      
      // Request microphone permission
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          sampleRate: 48000
        }
      });
      
      streamRef.current = stream;
      
      // Create MediaRecorder
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm;codecs=opus'
      });
      mediaRecorderRef.current = mediaRecorder;
      
      // Setup data handler
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };
      
      // Setup stop handler
      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { 
          type: 'audio/webm;codecs=opus' 
        });
        
        // Create URL for playback
        const url = URL.createObjectURL(audioBlob);
        setAudioURL(url);
        
        // Send to backend for processing
        await processAudio(audioBlob);
        
        // Reset
        audioChunksRef.current = [];
      };
      
      // Start recording
      mediaRecorder.start(1000); // Collect data every second
      
      // Start timer
      let seconds = 0;
      timerRef.current = setInterval(() => {
        seconds += 1;
        setRecordingTime(seconds);
      }, 1000);
      
    } catch (error) {
      console.error('Microphone access error:', error);
      setRecordingState('error');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && 
        mediaRecorderRef.current.state === 'recording') {
      
      clearInterval(timerRef.current);
      mediaRecorderRef.current.stop();
      
      // Stop all tracks
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
      
      setRecordingState('processing');
    }
  };

  const processAudio = async (audioBlob) => {
    try {
      // Create FormData to send audio file
      const formData = new FormData();
      formData.append('audio', audioBlob, 'recording.webm');
      formData.append('language', 'en-NG'); // Nigerian English
      
      // Send to backend API
      const response = await fetch('/api/transcribe', {
        method: 'POST',
        body: formData
      });
      
      const data = await response.json();
      
      if (data.success) {
        setTranscript(data.transcript);
        setRecordingState('completed');
        
        // Pass data to parent component
        if (onRecordingComplete) {
          onRecordingComplete({
            audioBlob: audioBlob,
            audioURL: audioURL,
            transcript: data.transcript,
            keywords: data.keywords,
            sentiment: data.sentiment,
            duration: recordingTime
          });
        }
      } else {
        throw new Error('Transcription failed');
      }
      
    } catch (error) {
      console.error('Processing error:', error);
      setRecordingState('error');
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  // Real-time volume visualization
  const [volume, setVolume] = useState(0);
  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);

  const setupAudioAnalysis = (stream) => {
    if (!audioContextRef.current) {
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
      analyserRef.current = audioContextRef.current.createAnalyser();
      
      const source = audioContextRef.current.createMediaStreamSource(stream);
      source.connect(analyserRef.current);
      
      // Analyze volume in real-time
      const dataArray = new Uint8Array(analyserRef.current.frequencyBinCount);
      
      const analyzeVolume = () => {
        if (analyserRef.current && recordingState === 'listening') {
          analyserRef.current.getByteFrequencyData(dataArray);
          const average = dataArray.reduce((a, b) => a + b) / dataArray.length;
          setVolume(Math.min(100, average));
          requestAnimationFrame(analyzeVolume);
        }
      };
      
      analyzeVolume();
    }
  };

  // Cleanup
  useEffect(() => {
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }
    };
  }, []);

  return (
    <div className="flex flex-col items-center space-y-6">
      {/* Volume visualization */}
      {recordingState === 'listening' && (
        <div className="w-64 h-4 bg-gray-200 rounded-full overflow-hidden">
          <div 
            className="h-full bg-gradient-to-r from-[#34D399] to-emerald-500 transition-all duration-100"
            style={{ width: `${volume}%` }}
          ></div>
        </div>
      )}
      
      {/* Recording timer */}
      {recordingState === 'listening' && (
        <div className="text-2xl font-bold text-[#111827]">
          {formatTime(recordingTime)}
        </div>
      )}
      
      {/* AI Orb */}
      <div className="relative">
        <div className={`absolute inset-0 ${
          recordingState === 'listening' ? 'bg-gradient-to-r from-[#34D399] to-emerald-500' :
          recordingState === 'processing' ? 'bg-gradient-to-r from-[#6D28D9] to-blue-500' :
          recordingState === 'completed' ? 'bg-gradient-to-r from-[#34D399] to-emerald-500' :
          'bg-gradient-to-r from-[#6D28D9] to-purple-800'
        } blur-xl opacity-50 rounded-full orb-glow`}></div>
        
        <button
          onClick={recordingState === 'idle' ? startRecording : 
                  recordingState === 'listening' ? stopRecording : null}
          disabled={recordingState === 'processing'}
          className={`relative w-48 h-48 ${
            recordingState === 'listening' ? 'bg-gradient-to-r from-[#34D399] to-emerald-500' :
            recordingState === 'processing' ? 'bg-gradient-to-r from-[#6D28D9] to-blue-500' :
            recordingState === 'completed' ? 'bg-gradient-to-r from-[#34D399] to-emerald-500' :
            'bg-gradient-to-r from-[#6D28D9] to-purple-800'
          } rounded-full flex items-center justify-center shadow-2xl cursor-pointer transition-all duration-300 hover:scale-105 disabled:cursor-not-allowed`}
        >
          <div className="text-white">
            {recordingState === 'idle' && <FiMic size={32} />}
            {recordingState === 'listening' && (
              <div className="w-8 h-8 bg-white rounded-full animate-pulse"></div>
            )}
            {recordingState === 'processing' && (
              <div className="w-8 h-8 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            )}
            {recordingState === 'completed' && <FiCheck size={32} />}
            {recordingState === 'error' && <FiAlertCircle size={32} />}
          </div>
        </button>
      </div>
      
      {/* Transcript preview */}
      {transcript && (
        <div className="mt-6 p-4 bg-[#F9FAFB] rounded-xl max-w-md">
          <h3 className="font-semibold text-[#111827] mb-2">AI Transcript:</h3>
          <p className="text-[#374151]">{transcript}</p>
        </div>
      )}
      
      {/* Audio playback */}
      {audioURL && (
        <audio controls src={audioURL} className="mt-4" />
      )}
    </div>
  );
};

export default AIOrb;