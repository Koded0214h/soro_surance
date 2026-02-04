import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import { useParams } from 'react-router-dom';
import { FiPlay, FiPause, FiDownload, FiCheck, FiX, FiAlertTriangle, FiMessageCircle } from 'react-icons/fi';

const AdminClaimDetail = () => {
  const { id } = useParams();
  const [isPlaying, setIsPlaying] = useState(false);

  const claimData = {
    id: id || 'CLM-00125',
    customer: {
      name: 'Adebayo Chukwu',
      phone: '+234 801 234 5678',
      policy: 'POL-2023-04567',
      location: 'Lagos, Nigeria'
    },
    details: {
      type: 'Vehicle Accident',
      date: 'Dec 14, 2023 10:30 AM',
      location: 'Lagos Expressway, KM 42',
      description: 'Minor collision with another vehicle. Front bumper damaged. No injuries reported.',
      estimatedAmount: '₦150,000'
    },
    analysis: {
      soroScore: 42,
      sentiment: 'Moderate Urgency',
      inconsistencies: 'Low',
      keywords: ['accident', 'bumper', 'expressway', 'minor', 'no injuries'],
      aiSummary: 'Claim shows moderate risk factors. Damage appears consistent with description. No major red flags detected.'
    },
    media: [
      { type: 'image', name: 'damage_front.jpg', uploaded: '2h ago' },
      { type: 'image', name: 'damage_side.jpg', uploaded: '2h ago' },
      { type: 'audio', name: 'voice_recording.mp3', duration: '1:45', uploaded: '3h ago' }
    ]
  };

  return (
    <div className="min-h-screen bg-[#F9FAFB]">
      <Navbar isAdmin={true} />
      
      <main className="p-6">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="mb-8">
            <div className="flex justify-between items-start">
              <div>
                <h1 className="text-3xl font-bold text-[#111827]">Claim Review: {claimData.id}</h1>
                <p className="text-[#374151] mt-2">AI Analysis + Human Review Interface</p>
              </div>
              <div className="flex space-x-4">
                <button className="flex items-center space-x-2 border border-gray-300 rounded-lg px-4 py-2 hover:bg-gray-50">
                  <FiDownload size={18} />
                  <span>Export</span>
                </button>
                <button className="bg-[#111827] text-white rounded-lg px-6 py-2 hover:bg-gray-800">
                  Back to Dashboard
                </button>
              </div>
            </div>
          </div>

          <div className="grid lg:grid-cols-3 gap-8">
            {/* Left Column - Claim Details */}
            <div className="lg:col-span-2 space-y-8">
              {/* Customer Info */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h2 className="text-xl font-bold text-[#111827] mb-6">Customer Information</h2>
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm text-[#374151] mb-1">Full Name</label>
                    <p className="font-medium">{claimData.customer.name}</p>
                  </div>
                  <div>
                    <label className="block text-sm text-[#374151] mb-1">Phone Number</label>
                    <p className="font-medium">{claimData.customer.phone}</p>
                  </div>
                  <div>
                    <label className="block text-sm text-[#374151] mb-1">Policy Number</label>
                    <p className="font-medium">{claimData.customer.policy}</p>
                  </div>
                  <div>
                    <label className="block text-sm text-[#374151] mb-1">Location</label>
                    <p className="font-medium">{claimData.customer.location}</p>
                  </div>
                </div>
              </div>

              {/* Claim Details */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h2 className="text-xl font-bold text-[#111827] mb-6">Claim Details</h2>
                <div className="space-y-6">
                  <div>
                    <label className="block text-sm text-[#374151] mb-1">Incident Type</label>
                    <p className="font-medium">{claimData.details.type}</p>
                  </div>
                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm text-[#374151] mb-1">Date & Time</label>
                      <p className="font-medium">{claimData.details.date}</p>
                    </div>
                    <div>
                      <label className="block text-sm text-[#374151] mb-1">Location</label>
                      <p className="font-medium">{claimData.details.location}</p>
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm text-[#374151] mb-1">Description</label>
                    <div className="bg-[#F9FAFB] rounded-lg p-4 mt-2">
                      <p className="text-[#374151]">{claimData.details.description}</p>
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm text-[#374151] mb-1">Estimated Claim Amount</label>
                    <p className="text-2xl font-bold text-[#111827]">{claimData.details.estimatedAmount}</p>
                  </div>
                </div>
              </div>

              {/* Media Files */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h2 className="text-xl font-bold text-[#111827] mb-6">Media Files</h2>
                <div className="grid md:grid-cols-3 gap-4">
                  {claimData.media.map((file, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-4 hover:border-[#6D28D9] transition-colors">
                      <div className="flex items-start justify-between mb-2">
                        <div className="w-10 h-10 bg-gradient-to-r from-[#6D28D9]/10 to-purple-500/10 rounded-lg flex items-center justify-center">
                          {file.type === 'audio' ? (
                            <FiMessageCircle className="text-[#6D28D9]" />
                          ) : (
                            <div className="text-[#6D28D9] font-bold">IMG</div>
                          )}
                        </div>
                        <button className="text-[#374151] hover:text-[#111827]">
                          <FiDownload size={18} />
                        </button>
                      </div>
                      <p className="font-medium text-[#111827] text-sm truncate">{file.name}</p>
                      <p className="text-xs text-[#374151] mt-1">
                        {file.type === 'audio' ? `${file.duration} • ` : ''}
                        {file.uploaded}
                      </p>
                      {file.type === 'audio' && (
                        <button 
                          onClick={() => setIsPlaying(!isPlaying)}
                          className="w-full mt-3 flex items-center justify-center space-x-2 bg-[#6D28D9] text-white py-2 rounded-lg hover:bg-purple-700 transition-colors"
                        >
                          {isPlaying ? (
                            <>
                              <FiPause size={18} />
                              <span>Pause Recording</span>
                            </>
                          ) : (
                            <>
                              <FiPlay size={18} />
                              <span>Play Recording</span>
                            </>
                          )}
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Right Column - AI Analysis & Actions */}
            <div className="space-y-8">
              {/* AI Analysis Card */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h2 className="text-xl font-bold text-[#111827] mb-6">AI Analysis</h2>
                
                <div className="space-y-6">
                  {/* Soro-Score */}
                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-[#374151]">Soro-Score Risk Assessment</span>
                      <div className={`px-4 py-2 rounded-full font-bold ${
                        claimData.analysis.soroScore < 30 ? 'bg-[#34D399] text-white' :
                        claimData.analysis.soroScore < 70 ? 'bg-[#F59E0B] text-white' :
                        'bg-[#FB7185] text-white'
                      }`}>
                        {claimData.analysis.soroScore}/100
                      </div>
                    </div>
                    <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-gradient-to-r from-[#34D399] via-[#F59E0B] to-[#FB7185] rounded-full"
                        style={{ width: `${claimData.analysis.soroScore}%` }}
                      ></div>
                    </div>
                  </div>

                  {/* Sentiment */}
                  <div>
                    <label className="block text-sm text-[#374151] mb-2">Voice Sentiment</label>
                    <div className="bg-gradient-to-r from-[#6D28D9]/10 to-purple-500/10 rounded-lg p-4">
                      <p className="font-medium">{claimData.analysis.sentiment}</p>
                    </div>
                  </div>

                  {/* Inconsistency */}
                  <div>
                    <label className="block text-sm text-[#374151] mb-2">Inconsistency Detection</label>
                    <div className="flex items-center space-x-2">
                      <div className={`w-3 h-3 rounded-full ${
                        claimData.analysis.inconsistencies === 'Low' ? 'bg-[#34D399]' :
                        claimData.analysis.inconsistencies === 'Medium' ? 'bg-[#F59E0B]' :
                        'bg-[#FB7185]'
                      }`}></div>
                      <span className="font-medium">{claimData.analysis.inconsistencies} Inconsistency</span>
                    </div>
                  </div>

                  {/* Keywords */}
                  <div>
                    <label className="block text-sm text-[#374151] mb-2">Detected Keywords</label>
                    <div className="flex flex-wrap gap-2">
                      {claimData.analysis.keywords.map((keyword, index) => (
                        <span key={index} className="px-3 py-1 bg-[#6D28D9]/10 text-[#6D28D9] rounded-full text-sm">
                          {keyword}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* AI Summary */}
                  <div>
                    <label className="block text-sm text-[#374151] mb-2">AI Summary</label>
                    <div className="bg-[#F9FAFB] rounded-lg p-4">
                      <p className="text-[#374151]">{claimData.analysis.aiSummary}</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Action Card */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h2 className="text-xl font-bold text-[#111827] mb-6">Review Actions</h2>
                
                <div className="space-y-4">
                  <div className="flex items-center space-x-3 p-4 bg-[#34D399]/10 rounded-lg">
                    <FiCheck className="text-[#34D399]" size={24} />
                    <div>
                      <h3 className="font-semibold text-[#111827]">Approve Claim</h3>
                      <p className="text-sm text-[#374151]">Auto-payout within 2 hours</p>
                    </div>
                  </div>

                  <div className="flex items-center space-x-3 p-4 bg-[#F59E0B]/10 rounded-lg">
                    <FiAlertTriangle className="text-[#F59E0B]" size={24} />
                    <div>
                      <h3 className="font-semibold text-[#111827]">Request More Info</h3>
                      <p className="text-sm text-[#374151]">Send voice call request</p>
                    </div>
                  </div>

                  <div className="flex items-center space-x-3 p-4 bg-[#FB7185]/10 rounded-lg">
                    <FiX className="text-[#FB7185]" size={24} />
                    <div>
                      <h3 className="font-semibold text-[#111827]">Reject Claim</h3>
                      <p className="text-sm text-[#374151]">Requires justification</p>
                    </div>
                  </div>
                </div>

                <div className="mt-8 space-y-4">
                  <button className="w-full bg-[#34D399] text-white py-3 rounded-lg font-semibold hover:bg-emerald-500 transition-colors">
                    Approve & Process Payment
                  </button>
                  <button className="w-full border-2 border-[#6D28D9] text-[#6D28D9] py-3 rounded-lg font-semibold hover:bg-[#6D28D9]/10 transition-colors">
                    Call Customer for Clarification
                  </button>
                  <button className="w-full border-2 border-gray-300 text-[#374151] py-3 rounded-lg font-semibold hover:bg-gray-50 transition-colors">
                    Flag for Senior Review
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default AdminClaimDetail;