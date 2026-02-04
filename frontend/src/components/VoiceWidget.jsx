import React, { useState } from 'react';
import { FiMic, FiX } from 'react-icons/fi';

const VoiceWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isRecording, setIsRecording] = useState(false);

  return (
    <>
      {/* Widget Trigger */}
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 w-14 h-14 bg-gradient-to-r from-[#6D28D9] to-purple-600 rounded-full shadow-2xl flex items-center justify-center hover:scale-110 transition-transform z-50"
      >
        <FiMic className="text-white" size={24} />
      </button>

      {/* Widget Modal */}
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-end justify-center p-4 sm:items-center sm:p-0">
          <div className="fixed inset-0 bg-black/50" onClick={() => setIsOpen(false)}></div>
          
          <div className="relative bg-white rounded-2xl shadow-2xl w-full max-w-md transform transition-all">
            {/* Header */}
            <div className="flex items-center justify-between p-6 border-b">
              <div>
                <h3 className="text-xl font-bold text-[#111827]">Voice Insurance</h3>
                <p className="text-[#374151] text-sm">Get insured in 60 seconds</p>
              </div>
              <button
                onClick={() => setIsOpen(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <FiX size={24} />
              </button>
            </div>

            {/* Content */}
            <div className="p-6">
              <div className="text-center mb-6">
                <div className="w-20 h-20 bg-gradient-to-r from-[#6D28D9] to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <FiMic className="text-white" size={32} />
                </div>
                <p className="text-[#374151]">
                  Tap the button below and describe what you want to insure
                </p>
              </div>

              {/* Recording Button */}
              <button
                onClick={() => {
                  setIsRecording(true);
                  // Simulate recording
                  setTimeout(() => {
                    setIsRecording(false);
                  }, 3000);
                }}
                className={`w-full py-4 rounded-xl mb-6 ${
                  isRecording
                    ? 'bg-gradient-to-r from-[#FB7185] to-pink-500'
                    : 'bg-gradient-to-r from-[#6D28D9] to-purple-600'
                } text-white font-bold text-lg flex items-center justify-center gap-3`}
              >
                {isRecording ? (
                  <>
                    <div className="w-4 h-4 bg-white rounded-full animate-pulse"></div>
                    <span>Listening...</span>
                  </>
                ) : (
                  <>
                    <FiMic size={24} />
                    <span>Start Speaking</span>
                  </>
                )}
              </button>

              {/* Product Options */}
              <div className="space-y-3 mb-6">
                <h4 className="font-semibold text-[#111827]">Popular Insurance Types:</h4>
                <div className="grid grid-cols-2 gap-3">
                  {['Auto', 'Health', 'Home', 'Travel'].map((type) => (
                    <button
                      key={type}
                      className="p-3 border border-gray-200 rounded-lg hover:border-[#6D28D9] hover:bg-[#6D28D9]/5 transition-colors"
                    >
                      <div className="font-medium text-[#111827]">{type}</div>
                      <div className="text-xs text-[#374151]">From ₦500/month</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* USSD Option */}
              <div className="bg-gradient-to-r from-[#34D399]/10 to-emerald-500/10 rounded-xl p-4 text-center">
                <p className="text-sm text-[#374151] mb-2">Prefer USSD?</p>
                <div className="font-mono font-bold text-lg text-[#111827]">*347*7#</div>
                <p className="text-xs text-[#374151] mt-1">Works on all mobile networks</p>
              </div>
            </div>

            {/* Footer */}
            <div className="p-4 bg-[#F9FAFB] rounded-b-2xl text-center">
              <p className="text-xs text-[#374151]">
                Powered by Sorosurance AI • Secure & Encrypted
              </p>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default VoiceWidget;