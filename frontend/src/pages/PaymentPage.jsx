import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import { FiCreditCard, FiSmartphone, FiShield, FiCheckCircle, FiAlertCircle } from 'react-icons/fi';

const PaymentPage = () => {
  const [paymentMethod, setPaymentMethod] = useState('card');
  const [isProcessing, setIsProcessing] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  const handlePayment = () => {
    setIsProcessing(true);
    // Simulate payment processing
    setTimeout(() => {
      setIsProcessing(false);
      setIsSuccess(true);
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#F9FAFB] to-white">
      <Navbar />
      
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-[#111827] mb-4">Secure Payment</h1>
            <p className="text-xl text-[#374151]">Pay your premium or deductible with voice confirmation</p>
          </div>

          <div className="grid lg:grid-cols-3 gap-8">
            {/* Left Column - Payment Details */}
            <div className="lg:col-span-2">
              <div className="bg-white rounded-2xl shadow-xl p-6 mb-6">
                <h2 className="text-2xl font-bold text-[#111827] mb-6">Payment Details</h2>
                
                <div className="space-y-6">
                  <div className="bg-gradient-to-r from-[#6D28D9]/10 to-purple-500/10 rounded-xl p-6">
                    <div className="flex justify-between items-center mb-4">
                      <div>
                        <h3 className="font-bold text-[#111827]">Premium Payment</h3>
                        <p className="text-[#374151]">Policy #POL-2023-04567</p>
                      </div>
                      <div className="text-right">
                        <div className="text-3xl font-bold text-[#111827]">₦25,000</div>
                        <div className="text-[#374151]">Due today</div>
                      </div>
                    </div>
                    <div className="flex items-center text-[#34D399]">
                      <FiCheckCircle size={20} className="mr-2" />
                      <span>Voice confirmation enabled</span>
                    </div>
                  </div>

                  {/* Payment Method Selection */}
                  <div>
                    <h3 className="font-semibold text-[#111827] mb-4">Payment Method</h3>
                    <div className="grid grid-cols-2 gap-4 mb-6">
                      <button
                        onClick={() => setPaymentMethod('card')}
                        className={`p-4 rounded-xl border-2 flex flex-col items-center justify-center ${
                          paymentMethod === 'card' 
                            ? 'border-[#6D28D9] bg-[#6D28D9]/5' 
                            : 'border-gray-200 hover:border-gray-300'
                        }`}
                      >
                        <FiCreditCard size={32} className="mb-2" />
                        <span>Card</span>
                      </button>
                      <button
                        onClick={() => setPaymentMethod('transfer')}
                        className={`p-4 rounded-xl border-2 flex flex-col items-center justify-center ${
                          paymentMethod === 'transfer' 
                            ? 'border-[#6D28D9] bg-[#6D28D9]/5' 
                            : 'border-gray-200 hover:border-gray-300'
                        }`}
                      >
                        <FiSmartphone size={32} className="mb-2" />
                        <span>Transfer</span>
                      </button>
                    </div>

                    {/* Payment Form */}
                    {paymentMethod === 'card' && (
                      <div className="space-y-4">
                        <div>
                          <label className="block text-[#374151] mb-2">Card Number</label>
                          <input 
                            type="text" 
                            placeholder="1234 5678 9012 3456"
                            className="w-full p-3 border-2 border-gray-200 rounded-lg focus:border-[#6D28D9] focus:outline-none"
                          />
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                          <div>
                            <label className="block text-[#374151] mb-2">Expiry Date</label>
                            <input 
                              type="text" 
                              placeholder="MM/YY"
                              className="w-full p-3 border-2 border-gray-200 rounded-lg focus:border-[#6D28D9] focus:outline-none"
                            />
                          </div>
                          <div>
                            <label className="block text-[#374151] mb-2">CVV</label>
                            <input 
                              type="text" 
                              placeholder="123"
                              className="w-full p-3 border-2 border-gray-200 rounded-lg focus:border-[#6D28D9] focus:outline-none"
                            />
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Security Info */}
              <div className="bg-white rounded-2xl shadow-xl p-6">
                <div className="flex items-start space-x-3">
                  <FiShield className="text-[#34D399] mt-1" size={24} />
                  <div>
                    <h3 className="font-semibold text-[#111827] mb-2">Secure Payment Guaranteed</h3>
                    <p className="text-[#374151]">
                      Powered by RedPay & Paystack. Your payment is encrypted and secure. 
                      We never store your card details on our servers.
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Right Column - Summary & Actions */}
            <div>
              <div className="bg-white rounded-2xl shadow-xl p-6 sticky top-8">
                <h3 className="font-bold text-[#111827] mb-6">Order Summary</h3>
                
                <div className="space-y-4 mb-6">
                  <div className="flex justify-between">
                    <span className="text-[#374151]">Premium Amount</span>
                    <span className="font-medium">₦22,500</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-[#374151]">Processing Fee</span>
                    <span className="font-medium">₦500</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-[#374151]">VAT</span>
                    <span className="font-medium">₦2,000</span>
                  </div>
                  <div className="border-t pt-4">
                    <div className="flex justify-between text-lg font-bold">
                      <span>Total</span>
                      <span className="text-[#111827]">₦25,000</span>
                    </div>
                  </div>
                </div>

                {!isSuccess ? (
                  <button
                    onClick={handlePayment}
                    disabled={isProcessing}
                    className={`w-full py-4 rounded-xl font-bold text-lg transition-all ${
                      isProcessing
                        ? 'bg-gray-400 cursor-not-allowed'
                        : 'bg-gradient-to-r from-[#FB7185] to-pink-500 hover:opacity-90'
                    } text-white`}
                  >
                    {isProcessing ? (
                      <div className="flex items-center justify-center gap-2">
                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                        Processing...
                      </div>
                    ) : (
                      'Pay Now'
                    )}
                  </button>
                ) : (
                  <div className="text-center p-4 bg-gradient-to-r from-[#34D399]/10 to-emerald-500/10 rounded-xl">
                    <FiCheckCircle className="text-[#34D399] text-4xl mx-auto mb-3" />
                    <h4 className="font-bold text-[#111827] mb-1">Payment Successful!</h4>
                    <p className="text-[#374151] text-sm mb-4">
                      Your payment has been processed. A voice confirmation has been sent.
                    </p>
                    <button className="w-full bg-[#111827] text-white py-2 rounded-lg hover:bg-gray-800 transition-colors">
                      View Receipt
                    </button>
                  </div>
                )}

                {/* Voice Payment Option */}
                <div className="mt-6 p-4 bg-[#F9FAFB] rounded-xl">
                  <div className="flex items-center space-x-3 mb-3">
                    <div className="w-10 h-10 bg-gradient-to-r from-[#6D28D9] to-purple-600 rounded-full flex items-center justify-center">
                      <FiSmartphone className="text-white" size={20} />
                    </div>
                    <div>
                      <h4 className="font-semibold text-[#111827]">Voice Payment</h4>
                      <p className="text-sm text-[#374151]">Call +234 800 SOROINS</p>
                    </div>
                  </div>
                  <button className="w-full border-2 border-[#6D28D9] text-[#6D28D9] py-2 rounded-lg font-medium hover:bg-[#6D28D9]/10 transition-colors">
                    Pay via Voice Call
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

export default PaymentPage;