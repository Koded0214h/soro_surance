import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { FiMail, FiLock, FiEye, FiEyeOff, FiPhone, FiShield } from 'react-icons/fi';
import AIOrb from '../components/AIOrb';

const LoginPage = () => {
  const navigate = useNavigate();
  const [loginMethod, setLoginMethod] = useState('phone');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [formData, setFormData] = useState({
    phone: '',
    email: '',
    password: ''
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleLogin = (e) => {
    e.preventDefault();
    setIsLoggingIn(true);
    
    // Simple demo authentication
    setTimeout(() => {
      setIsLoggingIn(false);
      // Admin demo: phone/email = "admin", password = any
      if (formData.phone === 'admin' || formData.email === 'admin@sorosurance.com') {
        navigate('/admin');
      } else {
        navigate('/');
      }
    }, 1500);
  };

  const handleVoiceLogin = () => {
    alert("Voice login: Call +234 800 SOROINS and speak your phone number and PIN");
  };

  return (
    <div className="min-h-screen flex">
      {/* Left Side - Branding & Features */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-[#111827] via-[#6D28D9] to-purple-900 p-12 text-white">
        <div className="max-w-xl">
          <Link to="/" className="flex items-center space-x-3 mb-12">
            <div className="w-12 h-12 bg-gradient-to-r from-[#34D399] to-[#6D28D9] rounded-full flex items-center justify-center">
              <span className="text-xl font-bold">S</span>
            </div>
            <span className="text-2xl font-bold">Sorosurance</span>
          </Link>

          <div className="mb-12">
            <h1 className="text-4xl font-bold mb-4">Welcome Back!</h1>
            <p className="text-gray-300 text-lg">
              Access your AI-powered insurance account with voice, phone, or email.
            </p>
          </div>

          <div className="space-y-8 mb-12">
            <div className="flex items-start space-x-4">
              <div className="w-12 h-12 bg-white/10 rounded-xl flex items-center justify-center flex-shrink-0">
                <FiShield size={24} />
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-2">Secure Voice Login</h3>
                <p className="text-gray-300">
                  Log in with just your voice - no passwords needed
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="w-12 h-12 bg-white/10 rounded-xl flex items-center justify-center flex-shrink-0">
                <div className="text-2xl">🎯</div>
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-2">USSD Access</h3>
                <p className="text-gray-300">
                  Dial *347*7# from any mobile phone to access your account
                </p>
              </div>
            </div>
          </div>

          {/* AI Orb Demo */}
          <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8">
            <h3 className="text-xl font-semibold mb-4 text-center">Try Voice Login</h3>
            <div className="scale-75 transform origin-center">
              <AIOrb />
            </div>
            <p className="text-center text-gray-300 text-sm mt-4">
              "Say: My phone number is zero eight zero..." to log in with voice
            </p>
          </div>
        </div>
      </div>

      {/* Right Side - Login Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8">
        <div className="max-w-md w-full">
          {/* Mobile Header */}
          <div className="lg:hidden mb-8">
            <Link to="/" className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 bg-gradient-to-r from-[#6D28D9] to-[#34D399] rounded-full flex items-center justify-center">
                <span className="text-white text-lg font-bold">S</span>
              </div>
              <span className="text-xl font-bold text-[#111827]">Sorosurance</span>
            </Link>
            <h1 className="text-3xl font-bold text-[#111827] mb-2">Welcome Back</h1>
            <p className="text-[#374151]">Access your AI-powered insurance account</p>
          </div>

          {/* Login Method Toggle */}
          <div className="flex bg-gray-100 rounded-xl p-1 mb-8">
            <button
              onClick={() => setLoginMethod('phone')}
              className={`flex-1 py-3 rounded-lg text-center font-medium transition-all ${
                loginMethod === 'phone'
                  ? 'bg-white shadow-lg text-[#111827]'
                  : 'text-gray-600 hover:text-[#111827]'
              }`}
            >
              <div className="flex items-center justify-center space-x-2">
                <FiPhone size={18} />
                <span>Phone Login</span>
              </div>
            </button>
            <button
              onClick={() => setLoginMethod('email')}
              className={`flex-1 py-3 rounded-lg text-center font-medium transition-all ${
                loginMethod === 'email'
                  ? 'bg-white shadow-lg text-[#111827]'
                  : 'text-gray-600 hover:text-[#111827]'
              }`}
            >
              <div className="flex items-center justify-center space-x-2">
                <FiMail size={18} />
                <span>Email Login</span>
              </div>
            </button>
          </div>

          {/* Login Form */}
          <form onSubmit={handleLogin} className="space-y-6">
            {loginMethod === 'phone' ? (
              <div>
                <label className="block text-sm font-medium text-[#374151] mb-2">
                  Phone Number
                </label>
                <div className="relative">
                  <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
                    🇳🇬 +234
                  </div>
                  <input
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleInputChange}
                    placeholder="801 234 5678"
                    className="w-full pl-20 pr-4 py-3 border-2 border-gray-200 rounded-xl focus:border-[#6D28D9] focus:outline-none"
                    required
                  />
                </div>
              </div>
            ) : (
              <div>
                <label className="block text-sm font-medium text-[#374151] mb-2">
                  Email Address
                </label>
                <div className="relative">
                  <FiMail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    placeholder="you@example.com"
                    className="w-full pl-10 pr-4 py-3 border-2 border-gray-200 rounded-xl focus:border-[#6D28D9] focus:outline-none"
                    required
                  />
                </div>
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-[#374151] mb-2">
                Password / PIN
              </label>
              <div className="relative">
                <FiLock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                <input
                  type={showPassword ? "text" : "password"}
                  name="password"
                  value={formData.password}
                  onChange={handleInputChange}
                  placeholder="Enter your password or 4-digit PIN"
                  className="w-full pl-10 pr-12 py-3 border-2 border-gray-200 rounded-xl focus:border-[#6D28D9] focus:outline-none"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-[#374151]"
                >
                  {showPassword ? <FiEyeOff size={20} /> : <FiEye size={20} />}
                </button>
              </div>
              <div className="flex justify-between items-center mt-2">
                <label className="flex items-center space-x-2">
                  <input type="checkbox" className="rounded text-[#6D28D9] focus:ring-[#6D28D9]" />
                  <span className="text-sm text-[#374151]">Remember me</span>
                </label>
                <Link to="#" className="text-sm text-[#6D28D9] hover:underline">
                  Forgot password?
                </Link>
              </div>
            </div>

            {/* Demo Credentials */}
            <div className="bg-gradient-to-r from-[#6D28D9]/10 to-purple-500/10 rounded-xl p-4">
              <p className="text-sm text-[#374151]">
                <strong>Demo:</strong> Use "admin" as phone/email for admin access
              </p>
            </div>

            {/* Voice Login Option */}
            <div className="text-center">
              <button
                type="button"
                onClick={handleVoiceLogin}
                className="w-full bg-gradient-to-r from-[#6D28D9] to-purple-600 text-white py-3 rounded-xl font-semibold hover:opacity-90 transition-opacity mb-4 flex items-center justify-center gap-3"
              >
                <div className="w-6 h-6 bg-white/20 rounded-full flex items-center justify-center">
                  <FiPhone size={14} />
                </div>
                <span>Login with Voice Call</span>
              </button>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoggingIn}
              className={`w-full py-4 rounded-xl font-bold text-lg transition-all ${
                isLoggingIn
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-gradient-to-r from-[#FB7185] to-pink-500 hover:opacity-90'
              } text-white`}
            >
              {isLoggingIn ? (
                <div className="flex items-center justify-center gap-2">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  Logging in...
                </div>
              ) : (
                'Login to My Account'
              )}
            </button>

            {/* USSD Login Option */}
            <div className="text-center p-4 bg-[#F9FAFB] rounded-xl">
              <p className="text-sm text-[#374151] mb-2">Prefer USSD?</p>
              <div className="font-mono font-bold text-2xl text-[#111827] mb-2">*347*7#</div>
              <p className="text-xs text-[#374151]">
                Dial from any mobile phone, no internet required
              </p>
            </div>

            {/* Signup Link */}
            <div className="text-center pt-6 border-t">
              <p className="text-[#374151]">
                Don't have an account?{' '}
                <Link to="/signup" className="text-[#6D28D9] font-semibold hover:underline">
                  Sign up for free
                </Link>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;