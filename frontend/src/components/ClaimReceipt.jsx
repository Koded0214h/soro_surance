import React from 'react';
import { FiCopy, FiShare2, FiDownload } from 'react-icons/fi';

const ClaimReceipt = ({ claimData }) => {
  const {
    claimId = "CLM-2023-00125",
    date = "Dec 15, 2023 14:30",
    status = "Processing",
    soroScore = 42,
    estimatedPayout = "₦150,000",
    nextSteps = "Under review by AI",
    qrData = "https://sorosurance.com/claim/CLM-2023-00125"
  } = claimData || {};

  const getStatusColor = () => {
    if (soroScore < 30) return 'bg-[#34D399] text-white';
    if (soroScore < 70) return 'bg-[#F59E0B] text-white';
    return 'bg-[#FB7185] text-white';
  };

  return (
    <div className="bg-white rounded-2xl shadow-xl p-6 max-w-md mx-auto">
      <div className="text-center mb-6">
        <div className="w-16 h-16 bg-gradient-to-r from-[#6D28D9] to-[#34D399] rounded-full flex items-center justify-center mx-auto mb-4">
          <span className="text-white text-2xl font-bold">S</span>
        </div>
        <h2 className="text-2xl font-bold text-[#111827]">Claim Receipt</h2>
        <p className="text-[#374151] mt-1">AI-Powered Insurance Platform</p>
      </div>

      <div className="space-y-4">
        <div className="flex justify-between items-center py-3 border-b">
          <span className="text-[#374151] font-medium">Claim ID</span>
          <span className="text-[#111827] font-bold">{claimId}</span>
        </div>

        <div className="flex justify-between items-center py-3 border-b">
          <span className="text-[#374151] font-medium">Date Filed</span>
          <span className="text-[#111827]">{date}</span>
        </div>

        <div className="flex justify-between items-center py-3 border-b">
          <span className="text-[#374151] font-medium">Soro-Score</span>
          <div className={`px-3 py-1 rounded-full ${getStatusColor()} font-bold`}>
            {soroScore}/100
          </div>
        </div>

        <div className="flex justify-between items-center py-3 border-b">
          <span className="text-[#374151] font-medium">Status</span>
          <span className="text-[#111827] font-semibold">{status}</span>
        </div>

        <div className="bg-gradient-to-r from-[#34D399]/10 to-[#6D28D9]/10 rounded-xl p-4 my-4">
          <div className="text-center">
            <div className="text-3xl font-bold text-[#111827] mb-1">{estimatedPayout}</div>
            <div className="text-[#374151]">Estimated Payout</div>
          </div>
        </div>

        <div className="text-center my-6">
          <div className="text-[#374151] font-medium mb-2">QR Code for Tracking</div>
          <div className="bg-white p-4 rounded-lg inline-block border-2 border-[#6D28D9]/20">
            {/* QR Code Placeholder */}
            <div className="w-32 h-32 bg-gradient-to-br from-[#6D28D9]/20 to-[#34D399]/20 flex items-center justify-center">
              <div className="text-center">
                <div className="text-[#6D28D9] font-bold text-lg">SORO</div>
                <div className="text-xs text-[#374151] mt-1">Scan to track</div>
              </div>
            </div>
          </div>
        </div>

        <div className="flex justify-center space-x-4 mt-6">
          <button className="flex items-center space-x-2 bg-[#111827] text-white px-4 py-2 rounded-lg hover:bg-gray-800 transition-colors">
            <FiCopy size={18} />
            <span>Copy Link</span>
          </button>
          <button className="flex items-center space-x-2 bg-[#6D28D9] text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors">
            <FiShare2 size={18} />
            <span>Share</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default ClaimReceipt;