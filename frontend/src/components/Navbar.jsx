import React from 'react';
import { FiMenu, FiBell, FiUser, FiLogIn } from 'react-icons/fi';
import { Link, useLocation } from 'react-router-dom';

const Navbar = ({ isAdmin = false }) => {
  const location = useLocation();
  const isAuthPage = location.pathname === '/login' || location.pathname === '/signup';
  
  // For demo: check if we're on admin or home page to show different buttons
  const isHomePage = location.pathname === '/';
  const isLoggedIn = false; // Change to true to test logged-in state

  return (
    <nav className="bg-[#560591] text-white px-4 py-3 shadow-lg">
      <div className="container mx-auto flex justify-between items-center">
        <div className="flex items-center space-x-4">
          <button className="lg:hidden">
            <FiMenu size={24} />
          </button>
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-[#6D28D9] to-[#34D399] rounded-full flex items-center justify-center">
              <span className="text-white font-bold">S</span>
            </div>
            <span className="text-xl font-bold">Sorosurance</span>
          </Link>
        </div>

        <div className="hidden lg:flex items-center space-x-8">
          {!isAdmin && !isAuthPage && (
            <>
              <Link to="/" className={`hover:text-[#34D399] transition-colors ${isHomePage ? 'text-[#34D399]' : ''}`}>Home</Link>
              <Link to="/claim" className="hover:text-[#34D399] transition-colors">File Claim</Link>
              <Link to="/payment" className="hover:text-[#34D399] transition-colors">Payments</Link>
            </>
          )}
          {isAdmin && (
            <>
              <Link to="/admin" className="hover:text-[#34D399] transition-colors">Dashboard</Link>
              <Link to="/" className="hover:text-[#34D399] transition-colors">Customer View</Link>
            </>
          )}
        </div>

        <div className="flex items-center space-x-4">
          {!isAuthPage && !isLoggedIn && (
            <div className="flex items-center space-x-3">
              <Link to="/login" className="flex items-center space-x-2 text-white hover:text-gray-300 transition-colors">
                <FiLogIn size={18} />
                <span>Login</span>
              </Link>
              <Link to="/signup" className="bg-gradient-to-r from-[#FB7185] to-pink-500 text-white px-4 py-2 rounded-lg font-medium hover:opacity-90 transition-opacity">
                Sign Up Free
              </Link>
            </div>
          )}
          {isLoggedIn && (
            <>
              <button className="relative">
                <FiBell size={22} />
                <span className="absolute -top-1 -right-1 w-2 h-2 bg-[#FB7185] rounded-full"></span>
              </button>
              <button className="flex items-center space-x-2 bg-[#6D28D9] px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors">
                <FiUser size={18} />
                <span>{isAdmin ? 'Admin Panel' : 'My Account'}</span>
              </button>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;