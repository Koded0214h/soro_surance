import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import AIOrb from '../components/AIOrb';
import KeywordBubble from '../components/KeywordBubble';
import ClaimReceipt from '../components/ClaimReceipt';
import { FiUpload, FiCamera, FiInfo, FiArrowRight } from 'react-icons/fi';

const ClaimPage = () => {
  const [step, setStep] = useState(1); // 1: Voice, 2: Media, 3: Review, 4: Receipt
  const [audioData, setAudioData] = useState(null);
  const [soroScore, setSoroScore] = useState(null);

  const detectedKeywords = [
    { text: "Accident", category: "damage" },
    { text: "Yesterday", category: "urgency" },
    { text: "Lagos", category: "location" },
    { text: "Car", category: "vehicle" },
    { text: "Front Bumper", category: "damage" },
    { text: "No Injuries", category: "success" },
  ];

  const handleAudioData = (data) => {
    setAudioData(data);
    // Simulate Soro-Score calculation
    setTimeout(() => {
      const score = Math.floor(Math.random() * 100);
      setSoroScore(score);
      setStep(2);
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#F9FAFB] to-white">
      <Navbar />
      
      <main className="container mx-auto px-4 py-8">
        {/* Progress Steps */}
        <div className="max-w-4xl mx-auto mb-12">
          <div className="flex justify-between items-center relative">
            {[1, 2, 3, 4].map((stepNum) => (
              <div key={stepNum} className="flex flex-col items-center relative z-10">
                <div className={`w-12 h-12 rounded-full flex items-center justify-center mb-2 ${
                  step >= stepNum 
                    ? stepNum === 4 
                      ? 'bg-[#34D399]' 
                      : 'bg-[#6D28D9]'
                    : 'bg-gray-300'
                } text-white font-bold text-lg`}>
                  {stepNum === 4 ? '✓' : stepNum}
                </div>
                <span className={`text-sm font-medium ${
                  step >= stepNum ? 'text-[#111827]' : 'text-gray-400'
                }`}>
                  {['Voice Claim', 'Add Media', 'Review', 'Receipt'][stepNum - 1]}
                </span>
              </div>
            ))}
            <div className="absolute top-6 left-0 w-full h-1 bg-gray-300 -z-10">
              <div 
                className="h-full bg-gradient-to-r from-[#6D28D9] via-purple-500 to-[#34D399] transition-all duration-500"
                style={{ width: `${((step - 1) / 3) * 100}%` }}
              ></div>
            </div>
          </div>
        </div>

        {/* Step Content */}
        <div className="max-w-4xl mx-auto">
          {step === 1 && (
            <div className="bg-white rounded-3xl shadow-xl p-8">
              <h1 className="text-3xl font-bold text-[#111827] mb-2">Describe Your Claim</h1>
              <p className="text-[#374151] mb-8">Speak naturally about what happened. Our AI understands any language.</p>
              
              <div className="mb-8">
                <div className="bg-gradient-to-r from-[#6D28D9]/10 to-[#34D399]/10 rounded-xl p-6 mb-6">
                  <div className="flex items-start space-x-3">
                    <FiInfo className="text-[#6D28D9] mt-1" size={20} />
                    <div>
                      <h3 className="font-semibold text-[#111827] mb-1">What to mention:</h3>
                      <ul className="list-disc pl-5 text-[#374151] space-y-1">
                        <li>What happened and when</li>
                        <li>Location of the incident</li>
                        <li>Type of damage or loss</li>
                        <li>Any other parties involved</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>

              <AIOrb onAudioData={handleAudioData} />
            </div>
          )}

          {step === 2 && (
            <div className="bg-white rounded-3xl shadow-xl p-8">
              <h1 className="text-3xl font-bold text-[#111827] mb-2">Add Supporting Media</h1>
              <p className="text-[#374151] mb-8">Upload photos or videos to help verify your claim (optional but recommended).</p>

              <div className="grid md:grid-cols-2 gap-8 mb-8">
                <div>
                  <h3 className="text-lg font-semibold text-[#111827] mb-4">Detected Keywords:</h3>
                  <div className="flex flex-wrap gap-3">
                    {detectedKeywords.map((keyword, index) => (
                      <KeywordBubble key={index} {...keyword} />
                    ))}
                  </div>
                  
                  {soroScore !== null && (
                    <div className="mt-8 p-4 bg-gradient-to-r from-[#6D28D9]/10 to-purple-500/10 rounded-xl">
                      <div className="flex items-center justify-between">
                        <span className="text-[#374151] font-medium">AI Soro-Score:</span>
                        <div className={`px-4 py-2 rounded-full font-bold ${
                          soroScore < 30 ? 'bg-[#34D399] text-white' :
                          soroScore < 70 ? 'bg-[#F59E0B] text-white' :
                          'bg-[#FB7185] text-white'
                        }`}>
                          {soroScore}/100
                        </div>
                      </div>
                      <p className="text-sm text-[#374151] mt-2">
                        {soroScore < 30 ? 'Low risk - Likely auto-approved' :
                         soroScore < 70 ? 'Medium risk - Under review' :
                         'High risk - Manual review required'}
                      </p>
                    </div>
                  )}
                </div>

                <div>
                  <div className="border-2 border-dashed border-gray-300 rounded-2xl p-8 text-center hover:border-[#6D28D9] transition-colors cursor-pointer">
                    <FiUpload className="mx-auto text-4xl text-gray-400 mb-4" />
                    <h3 className="text-lg font-semibold text-[#111827] mb-2">Upload Photos/Videos</h3>
                    <p className="text-[#374151] mb-4">Drag & drop or click to browse</p>
                    <button className="bg-[#6D28D9] text-white px-6 py-2 rounded-lg hover:bg-purple-700 transition-colors">
                      Choose Files
                    </button>
                  </div>

                  <div className="mt-6 border-2 border-dashed border-gray-300 rounded-2xl p-8 text-center hover:border-[#34D399] transition-colors cursor-pointer">
                    <FiCamera className="mx-auto text-4xl text-gray-400 mb-4" />
                    <h3 className="text-lg font-semibold text-[#111827] mb-2">Take Photo Now</h3>
                    <p className="text-[#374151]">Use your device camera</p>
                  </div>
                </div>
              </div>

              <div className="flex justify-between">
                <button 
                  onClick={() => setStep(1)}
                  className="text-[#6D28D9] font-medium hover:underline"
                >
                  ← Back to Voice Recording
                </button>
                <button 
                  onClick={() => setStep(3)}
                  className="bg-[#FB7185] text-white px-8 py-3 rounded-lg font-semibold hover:bg-pink-500 transition-colors flex items-center gap-2"
                >
                  Continue to Review
                  <FiArrowRight size={20} />
                </button>
              </div>
            </div>
          )}

          {step === 3 && (
            <div className="bg-white rounded-3xl shadow-xl p-8">
              <h1 className="text-3xl font-bold text-[#111827] mb-2">Review Your Claim</h1>
              <p className="text-[#374151] mb-8">Verify the details before submission.</p>

              <div className="grid md:grid-cols-2 gap-8 mb-8">
                <div>
                  <div className="bg-gray-50 rounded-xl p-6 mb-6">
                    <h3 className="font-semibold text-[#111827] mb-3">Claim Summary</h3>
                    <div className="space-y-3">
                      <div className="flex justify-between">
                        <span className="text-[#374151]">Claim Type:</span>
                        <span className="font-medium">Vehicle Accident</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-[#374151]">Date of Incident:</span>
                        <span className="font-medium">Dec 14, 2023</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-[#374151]">Location:</span>
                        <span className="font-medium">Lagos Expressway</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-[#374151]">Estimated Damage:</span>
                        <span className="font-medium text-[#111827]">₦150,000 - ₦200,000</span>
                      </div>
                    </div>
                  </div>

                  <div className="bg-gradient-to-r from-[#34D399]/10 to-emerald-500/10 rounded-xl p-6">
                    <h3 className="font-semibold text-[#111827] mb-3">AI Assessment</h3>
                    <div className="flex items-center justify-between mb-4">
                      <span className="text-[#374151]">Soro-Score:</span>
                      <div className="px-4 py-2 bg-[#34D399] text-white rounded-full font-bold">
                        42/100
                      </div>
                    </div>
                    <p className="text-[#374151] text-sm">
                      Based on our AI analysis, your claim shows <strong>medium risk factors</strong>. 
                      It will be reviewed by our team within 2-4 hours.
                    </p>
                  </div>
                </div>

                <div>
                  <h3 className="font-semibold text-[#111827] mb-4">Next Steps</h3>
                  <div className="space-y-4">
                    <div className="flex items-start space-x-3">
                      <div className="w-8 h-8 bg-[#6D28D9] text-white rounded-full flex items-center justify-center flex-shrink-0">
                        1
                      </div>
                      <div>
                        <h4 className="font-medium text-[#111827]">Submit Claim</h4>
                        <p className="text-sm text-[#374151]">Your claim will be queued for review</p>
                      </div>
                    </div>
                    <div className="flex items-start space-x-3">
                      <div className="w-8 h-8 bg-[#F59E0B] text-white rounded-full flex items-center justify-center flex-shrink-0">
                        2
                      </div>
                      <div>
                        <h4 className="font-medium text-[#111827]">AI + Human Review</h4>
                        <p className="text-sm text-[#374151]">Combined assessment for accuracy</p>
                      </div>
                    </div>
                    <div className="flex items-start space-x-3">
                      <div className="w-8 h-8 bg-[#34D399] text-white rounded-full flex items-center justify-center flex-shrink-0">
                        3
                      </div>
                      <div>
                        <h4 className="font-medium text-[#111827]">Decision & Payout</h4>
                        <p className="text-sm text-[#374151]">Receive notification via voice call or WhatsApp</p>
                      </div>
                    </div>
                  </div>

                  <button 
                    onClick={() => setStep(4)}
                    className="w-full mt-8 bg-gradient-to-r from-[#FB7185] to-pink-500 text-white py-4 rounded-xl font-bold text-lg hover:opacity-90 transition-opacity"
                  >
                    Submit Claim for Review
                  </button>
                </div>
              </div>
            </div>
          )}

          {step === 4 && (
            <div className="text-center">
              <h1 className="text-3xl font-bold text-[#111827] mb-2">Claim Submitted Successfully!</h1>
              <p className="text-[#374151] mb-8">Your claim is being processed. Here's your receipt:</p>
              
              <div className="max-w-md mx-auto">
                <ClaimReceipt claimData={{
                  claimId: "CLM-2023-00125",
                  date: "Dec 15, 2023 14:30",
                  status: "Processing",
                  soroScore: 42,
                  estimatedPayout: "₦150,000",
                  nextSteps: "Under review by AI"
                }} />
                
                <div className="mt-8 space-y-4">
                  <button className="w-full bg-[#111827] text-white py-3 rounded-lg font-semibold hover:bg-gray-800 transition-colors">
                    Track Claim Status
                  </button>
                  <button className="w-full border-2 border-[#6D28D9] text-[#6D28D9] py-3 rounded-lg font-semibold hover:bg-[#6D28D9]/10 transition-colors">
                    Return to Home
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default ClaimPage;