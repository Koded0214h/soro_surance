import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import ClaimPage from './pages/ClaimPage';
import PaymentPage from './pages/PaymentPage';
import AdminDashboard from './pages/AdminDashboard';
import AdminClaimDetail from './pages/AdminClaimDetail';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-[#F9FAFB]">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/claim" element={<ClaimPage />} />
          <Route path="/payment" element={<PaymentPage />} />
          <Route path="/admin" element={<AdminDashboard />} />
          <Route path="/admin/claim/:id" element={<AdminClaimDetail />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;