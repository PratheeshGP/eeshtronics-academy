import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Lock, Mail, User, Eye, EyeOff } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

export default function LoginPage() {
    const [isLogin, setIsLogin] = useState(true);
    const [showPassword, setShowPassword] = useState(false);
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const { login, register } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            if (isLogin) {
                await login(formData.username, formData.password);
            } else {
                await register(formData.username, formData.email, formData.password);
            }
            navigate('/dashboard');
        } catch (err: any) {
            setError(err.message || 'An error occurred');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-[#08080a] relative overflow-hidden">
            {/* Animated floating background bubble blobs */}
            <div className="absolute inset-0 overflow-hidden pointer-events-none">
                <div className="absolute top-10 left-10 w-96 h-96 bg-[#ff007f]/5 rounded-full blur-3xl animate-float-slow"></div>
                <div className="absolute bottom-10 right-10 w-96 h-96 bg-purple-600/5 rounded-full blur-3xl animate-float-medium"></div>
                <div className="absolute top-1/2 left-1/3 w-80 h-80 bg-fuchsia-600/5 rounded-full blur-3xl animate-float-fast"></div>
            </div>

            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5 }}
                className="relative z-10 w-full max-w-md p-8"
            >
                {/* Logo and Branding */}
                <div className="text-center mb-8">
                    <img
                        src="/eeshtronics_academy_logo.png"
                        alt="Eeshtronics Academy"
                        className="w-20 h-20 mx-auto mb-4 animate-float-medium"
                    />
                    <h1 className="text-4xl font-extrabold mb-1" style={{ fontFamily: 'Outfit, sans-serif' }}>
                        <span className="text-[#ff007f] drop-shadow-[0_0_10px_rgba(255,0,127,0.4)]">
                            EESHTRONICS
                        </span>
                        <br />
                        <span className="text-white text-xl tracking-[0.25em] font-light">ACADEMY</span>
                    </h1>
                    <p className="text-slate-400 text-sm mt-2">
                        {isLogin ? 'Welcome back, Engineer!' : 'Start your VLSI learning journey'}
                    </p>
                </div>

                {/* Login/Register Glassmorphic Bubbly Card */}
                <motion.div
                    layout
                    className="bg-[#0e0e12]/70 backdrop-blur-xl rounded-[2rem] p-8 shadow-2xl border border-[#ff007f]/15 shadow-[#ff007f]/5"
                >
                    {/* Toggle Tabs (Capsule/Bubble Style) */}
                    <div className="flex gap-2 p-1 mb-6 bg-black/45 rounded-full border border-white/5">
                        <button
                            type="button"
                            onClick={() => setIsLogin(true)}
                            className={`flex-1 py-2 px-4 rounded-full font-medium transition-all ${isLogin
                                    ? 'bg-gradient-to-r from-[#ff007f] to-purple-600 text-white shadow-md'
                                    : 'text-slate-400 hover:text-white'
                                }`}
                        >
                            Login
                        </button>
                        <button
                            type="button"
                            onClick={() => setIsLogin(false)}
                            className={`flex-1 py-2 px-4 rounded-full font-medium transition-all ${!isLogin
                                    ? 'bg-gradient-to-r from-[#ff007f] to-purple-600 text-white shadow-md'
                                    : 'text-slate-400 hover:text-white'
                                }`}
                        >
                            Register
                        </button>
                    </div>

                    {/* Error Message */}
                    {error && (
                        <div className="mb-4 p-3 bg-red-500/10 border border-red-500/25 rounded-2xl text-red-400 text-sm">
                            {error}
                        </div>
                    )}

                    {/* Form */}
                    <form onSubmit={handleSubmit} className="space-y-4">
                        {/* Username */}
                        <div>
                            <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 ml-4">
                                Username
                            </label>
                            <div className="relative">
                                <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
                                <input
                                    type="text"
                                    value={formData.username}
                                    onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                                    className="w-full bg-slate-950/50 border border-white/10 rounded-full py-3 px-12 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-[#ff007f] focus:ring-1 focus:ring-[#ff007f] transition-all"
                                    placeholder="Username"
                                    required
                                />
                            </div>
                        </div>

                        {/* Email (Register only) */}
                        {!isLogin && (
                            <div>
                                <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 ml-4">
                                    Email Address
                                </label>
                                <div className="relative">
                                    <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
                                    <input
                                        type="email"
                                        value={formData.email}
                                        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                        className="w-full bg-slate-950/50 border border-white/10 rounded-full py-3 px-12 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-[#ff007f] focus:ring-1 focus:ring-[#ff007f] transition-all"
                                        placeholder="Email address"
                                        required={!isLogin}
                                    />
                                </div>
                            </div>
                        )}

                        {/* Password */}
                        <div>
                            <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 ml-4">
                                Password
                            </label>
                            <div className="relative">
                                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
                                <input
                                    type={showPassword ? 'text' : 'password'}
                                    value={formData.password}
                                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                    className="w-full bg-slate-950/50 border border-white/10 rounded-full py-3 px-12 pr-12 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-[#ff007f] focus:ring-1 focus:ring-[#ff007f] transition-all"
                                    placeholder="Password"
                                    required
                                    minLength={8}
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowPassword(!showPassword)}
                                    className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300"
                                >
                                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                                </button>
                            </div>
                            {!isLogin && (
                                <p className="mt-2 text-[10px] text-slate-500 ml-4">
                                    Min. 8 characters with uppercase, lowercase, and numbers
                                </p>
                            )}
                        </div>

                        {/* Forgot Password */}
                        {isLogin && (
                            <div className="text-right">
                                <Link to="/forgot-password" className="text-xs text-[#ff007f] hover:underline mr-4">
                                    Forgot password?
                                </Link>
                            </div>
                        )}

                        {/* Submit Button (Bubbly Pink Neon) */}
                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full mt-2 bg-gradient-to-r from-[#ff007f] to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white font-bold py-3 px-6 rounded-full transition-all shadow-lg shadow-[#ff007f]/10 hover:shadow-xl hover:shadow-[#ff007f]/30 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {loading ? 'Processing...' : isLogin ? 'Sign In' : 'Create Account'}
                        </button>
                    </form>
                </motion.div>

                {/* Footer */}
                <p className="text-center text-slate-500 text-xs mt-6">
                    By continuing, you agree to our{' '}
                    <Link to="/terms" className="text-[#ff007f] hover:underline">
                        Terms of Service
                    </Link>{' '}
                    and{' '}
                    <Link to="/privacy" className="text-[#ff007f] hover:underline">
                        Privacy Policy
                    </Link>
                </p>
            </motion.div>
        </div>
    );
}
