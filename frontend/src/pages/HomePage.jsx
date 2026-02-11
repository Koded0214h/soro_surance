import React from 'react';
import Navbar from '../components/Navbar';
import AIOrb from '../components/AIOrb';
import KeywordBubble from '../components/KeywordBubble';
import { FiShield, FiMic, FiClock, FiCheckCircle } from 'react-icons/fi';
import { Link } from 'react-router-dom';

const HomePage = () => {
  const keywords = [
    { text: "Car Accident", category: "damage" },
    { text: "Lagos Expressway", category: "location" },
    { text: "Emergency", category: "urgency" },
    { text: "Toyota Camry", category: "vehicle" },
    { text: "Minor Injuries", category: "damage" },
    { text: "Police Report", category: "success" },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#F9FAFB] to-white">
      <Navbar />
      
      <main className="container mx-auto px-4 py-8">
        {/* Hero Section */}
        <section className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-[#111827] mb-9 mt-12">
            Voice-First <span className="text-[#6D28D9]">AI Insurance</span> for Nigeria
          </h1>
          <p className="text-xl text-[#374151] max-w-3xl mx-auto mb-11">
            File claims, get insured, and manage payments—all through simple voice commands. 
            Accessible to everyone, regardless of literacy level.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              to="/claim" 
              className="bg-[#FB7185] text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-pink-500 transition-colors shadow-lg flex items-center justify-center gap-2"
            >
              <FiMic size={20} />
              Start New Claim
            </Link>
            <button className="bg-white text-[#111827] border-2 border-[#6D28D9] px-8 py-3 rounded-lg text-lg font-semibold hover:bg-[#6D28D9]/10 transition-colors">
              Learn How It Works
            </button>
          </div>
        </section>
        
<section className="bg-gradient-to-r from-[#111827] via-[#6d28d9] to-[#111827] rounded-2xl p-8 text-white mb-12">
  <div className="max-w-4xl mx-auto text-center">
    <h2 className="text-2xl font-bold mb-4">Get Protected in 2 Minutes</h2>
    <p className="mb-6">Sign up now and get your first month of basic coverage FREE</p>
    <div className="flex flex-col sm:flex-row gap-4 justify-center">
      <Link 
        to="/signup" 
        className="bg-white text-[#6D28D9] px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
      >
        Start Free Trial
      </Link>
      <Link 
        to="/login" 
        className="bg-transparent border-2 border-white px-8 py-3 rounded-lg font-semibold hover:bg-white/10 transition-colors"
      >
        Existing User? Login
      </Link>
    </div>
  </div>
</section>
        {/* AI Orb Demo */}
        <section className="mb-16">
          <div className="max-w-2xl mx-auto">
            <div className="bg-gradient-to-br from-white to-[#F9FAFB] rounded-3xl p-8 shadow-xl">
              <h2 className="text-2xl font-bold text-center text-[#111827] mb-8">
                Try Our AI Assistant
              </h2>
              <AIOrb />
              
              <div className="mt-8">
                <h3 className="text-lg font-semibold text-[#111827] mb-4">Real-time Keyword Detection</h3>
                <div className="flex flex-wrap gap-3 justify-center">
                  {keywords.map((keyword, index) => (
                    <KeywordBubble key={index} {...keyword} />
                  ))}
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Features Grid */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-center text-[#111827] mb-12">
            Why Choose Sorosurance?
          </h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white p-6 rounded-2xl shadow-lg hover:shadow-xl transition-shadow">
              <div className="w-12 h-12 bg-gradient-to-r from-[#6D28D9] to-purple-600 rounded-lg flex items-center justify-center mb-4">
                <FiMic className="text-white" size={24} />
              </div>
              <h3 className="text-xl font-bold text-[#111827] mb-3">Voice-First Design</h3>
              <p className="text-[#374151]">
                No forms to fill. Simply speak about your claim in your own words, in any language.
              </p>
            </div>

            <div className="bg-white p-6 rounded-2xl shadow-lg hover:shadow-xl transition-shadow">
              <div className="w-12 h-12 bg-gradient-to-r from-[#34D399] to-emerald-500 rounded-lg flex items-center justify-center mb-4">
                <FiClock className="text-white" size={24} />
              </div>
              <h3 className="text-xl font-bold text-[#111827] mb-3">Instant AI Processing</h3>
              <p className="text-[#374151]">
                Our Soro-Score AI analyzes claims in seconds, with most decisions in under 5 minutes.
              </p>
            </div>

            <div className="bg-white p-6 rounded-2xl shadow-lg hover:shadow-xl transition-shadow">
              <div className="w-12 h-12 bg-gradient-to-r from-[#FB7185] to-pink-500 rounded-lg flex items-center justify-center mb-4">
                <FiCheckCircle className="text-white" size={24} />
              </div>
              <h3 className="text-xl font-bold text-[#111827] mb-3">95% Auto-Approval</h3>
              <p className="text-[#374151]">
                Low-risk claims are paid instantly. High-risk claims get human review within hours.
              </p>
            </div>
          </div>
        </section>

        {/* Embedded Widget Preview */}
        <section className="bg-gradient-to-r from-[#111827] to-gray-900 rounded-3xl p-8 text-white">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold mb-6">Embedded Insurance Anywhere</h2>
            <p className="text-gray-300 mb-8">
              Add our voice-to-buy widget to your website or app with one line of JavaScript.
              Your users can get insured without leaving your platform.
            </p>
            
            <div className="bg-gray-800 rounded-xl p-6 font-mono text-sm overflow-x-auto">
              <code className="text-[#34D399]">&lt;script src="https://widget.sorosurance.com/embed.js"&gt;&lt;/script&gt;</code>
              <br />
              <code className="text-[#6D28D9]">&lt;div class="sorosurance-widget" data-product="auto"&gt;&lt;/div&gt;</code>
            </div>
          </div>
        </section>
      </main>

      <footer className="bg-[#111827] text-white py-8 mt-16">
        <div className="container mx-auto px-4 text-center">
          <p>© 2023 Sorosurance. AI-powered insurance for Africa.</p>
          <p className="text-gray-400 mt-2">Available via Web, USSD, and WhatsApp</p>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;