import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import RiskHeatmap from '../components/RiskHeatmap';
import { FiFilter, FiSearch, FiDownload, FiAlertTriangle, FiCheckCircle, FiClock } from 'react-icons/fi';

const AdminDashboard = () => {
  const [timeRange, setTimeRange] = useState('7d');
  
  const stats = [
    { label: 'Total Claims', value: '1,247', change: '+12%', color: 'text-[#111827]' },
    { label: 'Auto-Approved', value: '845', change: '+8%', color: 'text-[#34D399]' },
    { label: 'Under Review', value: '203', change: '+15%', color: 'text-[#F59E0B]' },
    { label: 'Requires Action', value: '42', change: '-3%', color: 'text-[#FB7185]' },
  ];

  const recentClaims = [
    { id: 'CLM-00125', customer: 'Adebayo Chukwu', score: 28, amount: '₦150K', status: 'approved', time: '2h ago' },
    { id: 'CLM-00124', customer: 'Fatima Bello', score: 75, amount: '₦89K', status: 'review', time: '4h ago' },
    { id: 'CLM-00123', customer: 'James Okafor', score: 42, amount: '₦210K', status: 'review', time: '6h ago' },
    { id: 'CLM-00122', customer: 'Grace Okoro', score: 15, amount: '₦45K', status: 'approved', time: '1d ago' },
    { id: 'CLM-00121', customer: 'Musa Ibrahim', score: 88, amount: '₦320K', status: 'action', time: '1d ago' },
  ];

  return (
    <div className="min-h-screen bg-[#F9FAFB]">
      <Navbar isAdmin={true} />
      
      <main className="p-6">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-[#111827]">Admin Dashboard</h1>
          <p className="text-[#374151]">AI-powered claims management system</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => (
            <div key={index} className="bg-white rounded-xl p-6 shadow-lg">
              <div className="flex justify-between items-start">
                <div>
                  <p className="text-[#374151] text-sm">{stat.label}</p>
                  <p className={`text-2xl font-bold ${stat.color} mt-2`}>{stat.value}</p>
                </div>
                <span className={`text-sm font-medium ${
                  stat.change.startsWith('+') ? 'text-[#34D399]' : 'text-[#FB7185]'
                }`}>
                  {stat.change}
                </span>
              </div>
            </div>
          ))}
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Left Column - Risk Heatmap */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-bold text-[#111827]">Risk Heatmap</h2>
                <select 
                  value={timeRange}
                  onChange={(e) => setTimeRange(e.target.value)}
                  className="border border-gray-300 rounded-lg px-3 py-2 text-[#374151]"
                >
                  <option value="24h">Last 24 hours</option>
                  <option value="7d">Last 7 days</option>
                  <option value="30d">Last 30 days</option>
                </select>
              </div>
              <RiskHeatmap />
            </div>

            {/* Recent Claims Table */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-bold text-[#111827]">Recent Claims</h2>
                <div className="flex items-center space-x-4">
                  <div className="relative">
                    <FiSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                    <input 
                      type="text" 
                      placeholder="Search claims..."
                      className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-[#6D28D9]"
                    />
                  </div>
                  <button className="flex items-center space-x-2 border border-gray-300 rounded-lg px-4 py-2 hover:bg-gray-50">
                    <FiFilter size={18} />
                    <span>Filter</span>
                  </button>
                </div>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b">
                      <th className="text-left py-3 text-[#374151] font-medium">Claim ID</th>
                      <th className="text-left py-3 text-[#374151] font-medium">Customer</th>
                      <th className="text-left py-3 text-[#374151] font-medium">Soro-Score</th>
                      <th className="text-left py-3 text-[#374151] font-medium">Amount</th>
                      <th className="text-left py-3 text-[#374151] font-medium">Status</th>
                      <th className="text-left py-3 text-[#374151] font-medium">Time</th>
                    </tr>
                  </thead>
                  <tbody>
                    {recentClaims.map((claim, index) => (
                      <tr key={index} className="border-b hover:bg-gray-50 cursor-pointer">
                        <td className="py-4">
                          <span className="font-medium text-[#111827]">{claim.id}</span>
                        </td>
                        <td className="py-4">{claim.customer}</td>
                        <td className="py-4">
                          <div className={`px-3 py-1 rounded-full text-sm font-medium inline-block ${
                            claim.score < 30 ? 'bg-[#34D399]/20 text-[#34D399]' :
                            claim.score < 70 ? 'bg-[#F59E0B]/20 text-[#F59E0B]' :
                            'bg-[#FB7185]/20 text-[#FB7185]'
                          }`}>
                            {claim.score}
                          </div>
                        </td>
                        <td className="py-4 font-medium">{claim.amount}</td>
                        <td className="py-4">
                          <div className="flex items-center">
                            {claim.status === 'approved' && (
                              <>
                                <FiCheckCircle className="text-[#34D399] mr-2" />
                                <span className="text-[#34D399]">Approved</span>
                              </>
                            )}
                            {claim.status === 'review' && (
                              <>
                                <FiClock className="text-[#F59E0B] mr-2" />
                                <span className="text-[#F59E0B]">Review</span>
                              </>
                            )}
                            {claim.status === 'action' && (
                              <>
                                <FiAlertTriangle className="text-[#FB7185] mr-2" />
                                <span className="text-[#FB7185]">Action</span>
                              </>
                            )}
                          </div>
                        </td>
                        <td className="py-4 text-[#374151]">{claim.time}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div className="flex justify-between items-center mt-6">
                <button className="flex items-center space-x-2 text-[#6D28D9] hover:underline">
                  <FiDownload size={18} />
                  <span>Export Data</span>
                </button>
                <div className="flex space-x-2">
                  <button className="w-8 h-8 flex items-center justify-center border rounded-lg hover:bg-gray-50">
                    1
                  </button>
                  <button className="w-8 h-8 flex items-center justify-center border rounded-lg hover:bg-gray-50">
                    2
                  </button>
                  <button className="w-8 h-8 flex items-center justify-center border rounded-lg hover:bg-gray-50">
                    3
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column - Actions & Sentiment */}
          <div>
            {/* Quick Actions */}
            <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
              <h2 className="text-xl font-bold text-[#111827] mb-6">Quick Actions</h2>
              <div className="space-y-4">
                <button className="w-full bg-[#FB7185] text-white py-3 rounded-lg font-semibold hover:bg-pink-500 transition-colors">
                  Review High-Risk Claims (12)
                </button>
                <button className="w-full border-2 border-[#6D28D9] text-[#6D28D9] py-3 rounded-lg font-semibold hover:bg-[#6D28D9]/10 transition-colors">
                  Generate Weekly Report
                </button>
                <button className="w-full border-2 border-gray-300 text-[#374151] py-3 rounded-lg font-semibold hover:bg-gray-50 transition-colors">
                  Voice Call Analytics
                </button>
                <button className="w-full border-2 border-gray-300 text-[#374151] py-3 rounded-lg font-semibold hover:bg-gray-50 transition-colors">
                  Soro-Score Settings
                </button>
              </div>
            </div>

            {/* Sentiment Analysis */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-xl font-bold text-[#111827] mb-6">Voice Sentiment Highlights</h2>
              <div className="space-y-6">
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-[#374151]">Positive Sentiment</span>
                    <span className="font-medium text-[#34D399]">68%</span>
                  </div>
                  <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                    <div className="h-full bg-[#34D399] rounded-full" style={{ width: '68%' }}></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-[#374151]">Urgency Detection</span>
                    <span className="font-medium text-[#FB7185]">42%</span>
                  </div>
                  <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                    <div className="h-full bg-[#FB7185] rounded-full" style={{ width: '42%' }}></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-[#374151]">Inconsistency Rate</span>
                    <span className="font-medium text-[#F59E0B]">23%</span>
                  </div>
                  <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                    <div className="h-full bg-[#F59E0B] rounded-full" style={{ width: '23%' }}></div>
                  </div>
                </div>
              </div>

              <div className="mt-8 p-4 bg-[#F9FAFB] rounded-xl">
                <h3 className="font-semibold text-[#111827] mb-2">Top Keywords</h3>
                <div className="flex flex-wrap gap-2">
                  {['accident', 'emergency', 'help', 'urgent', 'damage', 'police'].map((word, index) => (
                    <span key={index} className="px-3 py-1 bg-[#6D28D9]/10 text-[#6D28D9] rounded-full text-sm">
                      {word}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default AdminDashboard;