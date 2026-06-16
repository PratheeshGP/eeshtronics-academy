import React, { useState } from 'react';
import { Bell, Search, Sparkles, LogOut } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '../../contexts/AuthContext';

export const Navbar: React.FC = () => {
    const { user, logout } = useAuth();
    const [showDropdown, setShowDropdown] = useState(false);

    const getInitials = (name: string) => {
        if (!name) return 'U';
        return name
            .split(' ')
            .map((n) => n[0])
            .join('')
            .slice(0, 2)
            .toUpperCase();
    };

    return (
        <div className="h-16 glass border-b border-[#ff007f]/10 flex items-center justify-between px-8 relative">
            <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex-1 max-w-xl"
            >
                <div className="relative">
                    <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <input
                        type="text"
                        placeholder="Search missions, topics, or ask AI mentor..."
                        className="w-full pl-12 pr-4 py-2.5 bg-slate-950/40 border border-white/10 rounded-full text-slate-200 placeholder-slate-500 focus:outline-none focus:border-[#ff007f]/50 focus:bg-slate-950/60 transition-all"
                    />
                </div>
            </motion.div>

            <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex items-center gap-4"
            >
                <button className="glass glass-hover p-2.5 rounded-full relative border-white/10 hover:border-[#ff007f]/30">
                    <Sparkles className="w-5 h-5 text-purple-400" />
                    <span className="absolute -top-1 -right-1 w-3 h-3 bg-[#ff007f] rounded-full animate-pulse shadow-[0_0_8px_#ff007f]"></span>
                </button>
                <button className="glass glass-hover p-2.5 rounded-full relative border-white/10 hover:border-[#ff007f]/30">
                    <Bell className="w-5 h-5 text-slate-400" />
                    <span className="absolute -top-1 -right-1 w-2 h-2 bg-[#ff007f] rounded-full shadow-[0_0_5px_#ff007f]"></span>
                </button>

                {user && (
                    <div className="relative">
                        <button
                            onClick={() => setShowDropdown(!showDropdown)}
                            className="flex items-center gap-2 p-1.5 rounded-full hover:bg-white/5 transition-all duration-300 border border-transparent hover:border-[#ff007f]/10"
                        >
                            <div className="w-8 h-8 bg-gradient-to-br from-[#ff007f] to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-sm shadow-md shadow-[#ff007f]/10">
                                {getInitials(user.username)}
                            </div>
                            <span className="text-sm font-medium text-slate-200 hidden sm:block max-w-[120px] truncate">
                                {user.username}
                            </span>
                        </button>

                        <AnimatePresence>
                            {showDropdown && (
                                <>
                                    <div className="fixed inset-0 z-10" onClick={() => setShowDropdown(false)} />
                                    <motion.div
                                        initial={{ opacity: 0, y: 10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        exit={{ opacity: 0, y: 10 }}
                                        className="absolute right-0 mt-2 w-48 bg-[#0e0e12]/95 border border-[#ff007f]/20 rounded-2xl shadow-2xl py-2 z-20"
                                    >
                                        <div className="px-4 py-2 border-b border-white/5">
                                            <p className="text-xs text-slate-400">Signed in as</p>
                                            <p className="text-sm font-semibold text-white truncate">{user.username}</p>
                                        </div>
                                        <button
                                            onClick={() => {
                                                setShowDropdown(false);
                                                logout();
                                            }}
                                            className="flex items-center gap-2 w-full text-left px-4 py-2.5 text-sm text-[#ff007f] hover:bg-[#ff007f]/10 transition-colors"
                                        >
                                            <LogOut className="w-4 h-4" />
                                            Log Out
                                        </button>
                                    </motion.div>
                                </>
                            )}
                        </AnimatePresence>
                    </div>
                )}
            </motion.div>
        </div>
    );
};
