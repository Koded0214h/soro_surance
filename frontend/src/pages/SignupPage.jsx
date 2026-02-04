import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  FiUser, FiMail, FiPhone, FiLock, FiEye, FiEyeOff, 
  FiCalendar, FiMapPin, FiCheck 
} from 'react-icons/fi';

const SignupPage = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const [formData, setFormData] = useState({
    fullName: '',
    phone: '',
    email: '',
    password: '',
    confirmPassword: '',
    dateOfBirth: '',
    address: '',
    city: '',
    state: 'Lagos',
    insuranceType: 'auto',
    voiceVerification: true,
    ussdAccess: true,
    termsAccepted: false
  });

  const states = [
    'Lagos', 'Abuja', 'Kano', 'Rivers', 'Oyo', 'Kaduna', 'Edo', 'Delta',
    'Ogun', 'Plateau', 'Sokoto', 'Bornu', 'Bauchi', 'Akwa Ibom', 'Anambra'
  ];

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleNextStep = (e) => {
    e.preventDefault();
    if (step < 3) {
      setStep(step + 1);
    } else {
      handleSubmit(e);
    }
  };

  const handlePrevStep = () => {
    setStep(step - 1);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    setTimeout(() => {
      setIsSubmitting(false);
      navigate('/login?signup=success');
    }, 2000);
  };

  const handleVoiceSignup = () => {
    alert("Voice signup: Call +234 800 SOROINS to create account with voice");
  };

  return (
    <div className="min-h-screen flex flex-col lg:flex-row">
      {/* Left Side - Branding */}
      <div className="lg:w-2/5 bg-gradient-to-br from-[#111827] via-[#6D28D9] to-purple-900 p-8 lg:p-12 text-white">
        <Link to="/" className="flex items-center space-x-3 mb-8 lg:mb-16">
          <div className="w-10 h-10 lg:w-12 lg:h-12 bg-gradient-to-r from-[#34D399] to-[#6D28D9] rounded-full flex items-center justify-center">
            <span className="text-lg lg:text-xl font-bold">S</span>
          </div>
          <span className="text-xl lg:text-2xl font-bold">Sorosurance</span>
        </Link>

        <div className="mb-8 lg:mb-12">
          <h1 className="text-3xl lg:text-4xl font-bold mb-4">Join the Future of Insurance</h1>
          <p className="text-gray-300">
            Get insured in minutes with our voice-first AI platform.
          </p>
        </div>

        {/* Progress Steps */}
        <div className="mb-8 lg:mb-12">
          <div className="flex items-center space-x-2 mb-6">
            {[1, 2, 3].map((stepNum) => (
              <React.Fragment key={stepNum}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                  step >= stepNum ? 'bg-white text-[#6D28D9]' : 'bg-white/20 text-white'
                } font-bold`}>
                  {step >= stepNum ? '✓' : stepNum}
                </div>
                {stepNum < 3 && (
                  <div className={`flex-1 h-1 ${
                    step > stepNum ? 'bg-white' : 'bg-white/20'
                  }`}></div>
                )}
              </React.Fragment>
            ))}
          </div>
          <div className="text-sm text-gray-300">
            Step {step} of 3: {step === 1 ? 'Basic Info' : step === 2 ? 'Personal Details' : 'Insurance Setup'}
          </div>
        </div>

        {/* Features */}
        <div className="space-y-6">
          <div className="flex items-start space-x-3">
            <div className="w-10 h-10 bg-white/10 rounded-lg flex items-center justify-center flex-shrink-0">
              <FiPhone size={20} />
            </div>
            <div>
              <h3 className="font-semibold text-lg mb-1">Voice-First Signup</h3>
              <p className="text-sm text-gray-300">
                Speak your details - no typing required
              </p>
            </div>
          </div>

          <div className="flex items-start space-x-3">
            <div className="w-10 h-10 bg-white/10 rounded-lg flex items-center justify-center flex-shrink-0">
              <div className="text-xl">🎯</div>
            </div>
            <div>
              <h3 className="font-semibold text-lg mb-1">USSD Access</h3>
              <p className="text-sm text-gray-300">
                Manage your policy from any mobile phone
              </p>
            </div>
          </div>
        </div>

        {/* Voice Signup CTA */}
        <div className="mt-8 lg:mt-12 bg-white/10 backdrop-blur-sm rounded-xl p-6">
          <h3 className="font-semibold text-lg mb-3">Prefer Voice?</h3>
          <button
            onClick={handleVoiceSignup}
            className="w-full bg-gradient-to-r from-[#34D399] to-emerald-500 text-white py-3 rounded-lg font-semibold hover:opacity-90 transition-opacity"
          >
            Call to Sign Up: +234 800 SOROINS
          </button>
        </div>
      </div>

      {/* Right Side - Signup Form */}
      <div className="flex-1 p-6 lg:p-12 bg-gradient-to-b from-[#F9FAFB] to-white">
        <div className="max-w-2xl mx-auto">
          {/* Mobile Header */}
          <div className="lg:hidden mb-8">
            <Link to="/" className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 bg-gradient-to-r from-[#6D28D9] to-[#34D399] rounded-full flex items-center justify-center">
                <span className="text-white text-lg font-bold">S</span>
              </div>
              <span className="text-xl font-bold text-[#111827]">Sorosurance</span>
            </Link>
          </div>

          <form onSubmit={handleNextStep} className="space-y-8">
            {/* Step 1: Basic Info */}
            {step === 1 && (
              <>
                <div>
                  <h2 className="text-2xl font-bold text-[#111827] mb-2">Create Your Account</h2>
                  <p className="text-[#374151]">Let's start with your basic information</p>
                </div>

                <div className="space-y-6">
                  <div>
                    <label className="block text-sm font-medium text-[#374151] mb-2">
                      Full Name
                    </label>
                    <div className="relative">
                      <FiUser className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                      <input
                        type="text"
                        name="fullName"
                        value={formData.fullName}
                        onChange={handleInputChange}
                        placeholder="John Adebayo"
                        className="w-full pl-10 pr-4 py-3 border-2 border-gray-200 rounded-xl focus:border-[#6D28D9] focus:outline-none"
                        required
                      />
                    </div>
                  </div>

                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-[#374151] mb-2">
                        Phone Number
                      </label>
                      <div className="relative">
                        <FiPhone className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                        <input
                          type="tel"
                          name="phone"
                          value={formData.phone}
                          onChange={handleInputChange}
                          placeholder="0801 234 5678"
                          className="w-full pl-10 pr-4 py-3 border-2 border-gray-200 rounded-xl focus:border-[#6D28D9] focus:outline-none"
                          required
                        />
                      </div>
                    </div>

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
                          placeholder="john@example.com"
                          className="w-full pl-10 pr-4 py-3 border-2 border-gray-200 rounded-xl focus:border-[#6D28D9] focus:outline-none"
                          required
                        />
                      </div>
                    </div>
                  </div>

                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-[#374151] mb-2">
                        Create Password
                      </label>
                      <div className="relative">
                        <FiLock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                        <input
                          type={showPassword ? "text" : "password"}
                          name="password"
                          value={formData.password}
                          onChange={handleInputChange}
                          placeholder="Minimum 6 characters"
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
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-[#374151] mb-2">
                        Confirm Password
                      </label>
                      <div className="relative">
                        <FiLock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                        <input
                          type={showPassword ? "text" : "password"}
                          name="confirmPassword"
                          value={formData.confirmPassword}
                          onChange={handleInputChange}
                          placeholder="Re-enter your password"
                          className="w-full pl-10 pr-4 py-3 border-2 border-gray-200 rounded-xl focus:border-[#6D28D9] focus:outline-none"
                          required
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </>
            )}

            {/* Step 2: Personal Details */}
            {step === 2 && (
              <>
                <div>
                  <h2 className="text-2xl font-bold text-[#111827] mb-2">Personal Details</h2>
                  <p className="text-[#374151]">Help us personalize your insurance experience</p>
                </div>

                <div className="space-y-6">
                  <div>
                    <label className="block text-sm font-medium text-[#374151] mb-2">
                      Date of Birth
                    </label>
                    <div className="relative">
                      <FiCalendar className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                      <input
                        type="date"
                        name="dateOfBirth"
                        value={formData.dateOfBirth}
                        onChange={handleInputChange}
                        className="w-full pl-10 pr-4 py-3 border-2 border-gray-200 rounded-xl focus:border-[#6D28D9] focus:outline-none"
                        required
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-[#374151] mb-2">
                      Residential Address
                    </label>
                    <div className="relative">
                      <FiMapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                      <input
                        type="text"
                        name="address"
                        value={formData.address}
                        onChange={handleInputChange}
                        placeholder="Street address"
                        className="w-full pl-10 pr-4 py-3 border-2 border-gray-200 rounded-xl focus:border-[#6D28D9] focus:outline-none"
                        required
                      />
                    </div>
                  </div>

                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-[#374151] mb-2">
                        City
                      </label>
                      <input
                        type="text"
                        name="city"
                        value={formData.city}
                        onChange={handleInputChange}
                        placeholder="e.g., Lagos"
                        className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-[#6D28D9] focus:outline-none"
                        required
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-[#374151] mb-2">
                        State
                      </label>
                      <select
                        name="state"
                        value={formData.state}
                        onChange={handleInputChange}
                        className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-[#6D28D9] focus:outline-none bg-white"
                        required
                      >
                        {states.map((state) => (
                          <option key={state} value={state}>{state}</option>
                        ))}
                      </select>
                    </div>
                  </div>
                </div>
              </>
            )}

            {/* Step 3: Insurance Setup */}
            {step === 3 && (
              <>
                <div>
                  <h2 className="text-2xl font-bold text-[#111827] mb-2">Insurance Setup</h2>
                  <p className="text-[#374151]">Choose your preferences and get instant coverage</p>
                </div>

                <div className="space-y-6">
                  <div>
                    <label className="block text-sm font-medium text-[#374151] mb-2">
                      What would you like to insure?
                    </label>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                      {['Auto', 'Health', 'Home', 'Travel', 'Life', 'Business'].map((type) => (
                        <label
                          key={type}
                          className={`border-2 rounded-xl p-4 cursor-pointer transition-all ${
                            formData.insuranceType === type.toLowerCase()
                              ? 'border-[#6D28D9] bg-[#6D28D9]/5'
                              : 'border-gray-200 hover:border-gray-300'
                          }`}
                        >
                          <input
                            type="radio"
                            name="insuranceType"
                            value={type.toLowerCase()}
                            checked={formData.insuranceType === type.toLowerCase()}
                            onChange={handleInputChange}
                            className="hidden"
                          />
                          <div className="text-center">
                            <div className="w-10 h-10 bg-gradient-to-r from-[#6D28D9]/20 to-purple-500/20 rounded-lg flex items-center justify-center mx-auto mb-2">
                              <span className="text-[#6D28D9] font-bold">{type.charAt(0)}</span>
                            </div>
                            <span className="font-medium text-[#111827]">{type}</span>
                          </div>
                        </label>
                      ))}
                    </div>
                  </div>

                  <div className="space-y-4">
                    <h3 className="font-medium text-[#111827]">Access Preferences</h3>
                    
                    <label className="flex items-start space-x-3 p-4 border border-gray-200 rounded-xl hover:border-gray-300 cursor-pointer">
                      <input
                        type="checkbox"
                        name="voiceVerification"
                        checked={formData.voiceVerification}
                        onChange={handleInputChange}
                        className="mt-1 text-[#6D28D9] focus:ring-[#6D28D9]"
                      />
                      <div>
                        <div className="font-medium text-[#111827]">Enable Voice Verification</div>
                        <p className="text-sm text-[#374151]">
                          Log in and verify claims using your voice
                        </p>
                      </div>
                    </label>

                    <label className="flex items-start space-x-3 p-4 border border-gray-200 rounded-xl hover:border-gray-300 cursor-pointer">
                      <input
                        type="checkbox"
                        name="ussdAccess"
                        checked={formData.ussdAccess}
                        onChange={handleInputChange}
                        className="mt-1 text-[#6D28D9] focus:ring-[#6D28D9]"
                      />
                      <div>
                        <div className="font-medium text-[#111827]">Enable USSD Access</div>
                        <p className="text-sm text-[#374151]">
                          Access your policy by dialing *347*7#
                        </p>
                      </div>
                    </label>

                    <label className="flex items-start space-x-3 p-4 border border-gray-200 rounded-xl hover:border-gray-300 cursor-pointer">
                      <input
                        type="checkbox"
                        name="termsAccepted"
                        checked={formData.termsAccepted}
                        onChange={handleInputChange}
                        className="mt-1 text-[#6D28D9] focus:ring-[#6D28D9]"
                        required
                      />
                      <div>
                        <div className="font-medium text-[#111827]">
                          I agree to the Terms & Conditions
                        </div>
                      </div>
                    </label>
                  </div>
                </div>
              </>
            )}

            {/* Navigation Buttons */}
            <div className="flex justify-between pt-8">
              {step > 1 ? (
                <button
                  type="button"
                  onClick={handlePrevStep}
                  className="px-8 py-3 border-2 border-gray-300 text-[#374151] rounded-xl font-semibold hover:bg-gray-50 transition-colors"
                >
                  ← Back
                </button>
              ) : (
                <div></div>
              )}

              <button
                type="submit"
                disabled={isSubmitting}
                className={`px-8 py-3 rounded-xl font-semibold transition-all ${
                  isSubmitting
                    ? 'bg-gray-400 cursor-not-allowed'
                    : 'bg-gradient-to-r from-[#FB7185] to-pink-500 hover:opacity-90'
                } text-white`}
              >
                {isSubmitting ? (
                  <div className="flex items-center gap-2">
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    {step === 3 ? 'Creating Account...' : 'Processing...'}
                  </div>
                ) : step === 3 ? (
                  'Complete Signup'
                ) : (
                  'Continue'
                )}
              </button>
            </div>

            {/* Login Link */}
            <div className="text-center pt-6 border-t">
              <p className="text-[#374151]">
                Already have an account?{' '}
                <Link to="/login" className="text-[#6D28D9] font-semibold hover:underline">
                  Login here
                </Link>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default SignupPage;