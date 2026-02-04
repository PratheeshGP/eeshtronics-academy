import React from 'react';
import { Bell, Search, Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';

export const Navbar: React.FC = () => {
    return (
        <div className="h-16 glass border-b border-white/10 flex items-center justify-between px-8">
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
                        className="w-full pl-12 pr-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-slate-200 placeholder-slate-500 focus:outline-none focus:border-primary-500/50 focus:bg-white/10 transition-all"
                    />
                </div>
            </motion.div>

            <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex items-center gap-4"
            >
                <button className="glass glass-hover p-2.5 rounded-xl relative">
                    <Sparkles className="w-5 h-5 text-accent-400" />
                    <span className="absolute -top-1 -right-1 w-3 h-3 bg-accent-500 rounded-full animate-pulse"></span>
                </button>
                <button className="glass glass-hover p-2.5 rounded-xl relative">
                    <Bell className="w-5 h-5 text-slate-400" />
                    <span className="absolute -top-1 -right-1 w-2 h-2 bg-primary-500 rounded-full"></span>
                </button>
            </motion.div>
        </div>
    );
};
