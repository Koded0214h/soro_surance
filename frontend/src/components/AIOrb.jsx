import React, { useState, useEffect } from 'react';
import { FiMic, FiMicOff, FiCheck, FiAlertCircle } from 'react-icons/fi';

const AIOrb = ({ onRecordingStateChange, onAudioData }) => {
  const [recordingState, setRecordingState] = useState('idle'); // idle, listening, processing, error
  const [volume, setVolume] = useState(0);

  const getOrbColor = () => {
    switch (recordingState) {
      case 'idle': return 'bg-gradient-to-r from-[#6D28D9] to-purple-800';
      case 'listening': return 'bg-gradient-to-r from-[#34D399] to-emerald-500';
      case 'processing': return 'bg-gradient-to-r from-[#6D28D9] to-blue-500';
      case 'error': return 'bg-gradient-to-r from-[#FB7185] to-red-500';
      default: return 'bg-gradient-to-r from-[#6D28D9] to-purple-800';
    }
  };

  const getIcon = () => {
    switch (recordingState) {
      case 'idle': return <FiMic size={32} />;
      case 'listening': return <div className="w-6 h-6 bg-white rounded-full animate-pulse"></div>;
      case 'processing': return <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin"></div>;
      case 'error': return <FiAlertCircle size={32} />;
      default: return <FiMic size={32} />;
    }
  };

  const handleStartRecording = () => {
    setRecordingState('listening');
    onRecordingStateChange('listening');
    
    // Simulate volume changes
    const interval = setInterval(() => {
      setVolume(Math.floor(Math.random() * 80) + 20);
    }, 100);

    setTimeout(() => {
      clearInterval(interval);
      setRecordingState('processing');
      onRecordingStateChange('processing');
      
      setTimeout(() => {
        setRecordingState('idle');
        onRecordingStateChange('idle');
        if (onAudioData) {
          onAudioData({ transcript: "Sample claim transcript for demonstration", duration: "45s" });
        }
      }, 2000);
    }, 5000);
  };

  return (
    <div className="flex flex-col items-center space-y-6">
      <div className="relative">
        {/* Outer glow */}
        <div className={`absolute inset-0 ${getOrbColor()} blur-xl opacity-50 rounded-full orb-glow`}></div>
        
        {/* Main orb */}
        <div 
          className={`relative w-48 h-48 ${getOrbColor()} rounded-full flex items-center justify-center shadow-2xl cursor-pointer transition-all duration-300 hover:scale-105`}
          onClick={recordingState === 'idle' ? handleStartRecording : null}
        >
          <div className="text-white">
            {getIcon()}
          </div>
          
          {/* Volume visualization */}
          {recordingState === 'listening' && (
            <div className="absolute inset-0 flex items-center justify-center">
              <div 
                className="absolute bg-white/30 rounded-full transition-all duration-100"
                style={{ width: `${volume}%`, height: `${volume}%` }}
              ></div>
            </div>
          )}
        </div>
      </div>

      <div className="text-center">
        <h3 className="text-xl font-semibold text-[#111827] mb-2">
          {recordingState === 'idle' && 'Tap to Start Recording'}
          {recordingState === 'listening' && 'Listening... Speak Now'}
          {recordingState === 'processing' && 'Processing Your Claim'}
          {recordingState === 'error' && 'Recording Error'}
        </h3>
        <p className="text-[#374151]">
          {recordingState === 'idle' && 'Describe your claim in simple words'}
          {recordingState === 'listening' && 'We\'re listening. Speak clearly about what happened.'}
          {recordingState === 'processing' && 'AI is analyzing your claim details'}
          {recordingState === 'error' && 'Please try again or contact support'}
        </p>
      </div>
    </div>
  );
};

export default AIOrb;