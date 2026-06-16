import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
    Home,
    Zap,
    BookOpen,
    Trophy,
    Users,
    Settings,
    ChevronRight,
    LogOut,
    UploadCloud
} from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';

const navigation = [
    { name: 'Home', href: '/dashboard', icon: Home },
    { name: 'Playground', href: '/playground', icon: Zap },
    { name: 'Missions', href: '/missions', icon: Trophy },
    { name: 'Requirements', href: '/requirements', icon: UploadCloud },
    { name: 'Knowledge Base', href: '/knowledge', icon: BookOpen },
    { name: 'Clan', href: '/clan', icon: Users },
    { name: 'Settings', href: '/settings', icon: Settings },
];

export const Sidebar: React.FC = () => {
    const location = useLocation();
    const { user, logout } = useAuth();

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
        <div className="w-72 h-screen glass border-r border-[#ff007f]/10 flex flex-col">
            <div className="p-6">
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex items-center gap-3"
                >
                    <div className="w-10 h-10 bg-gradient-to-br from-[#ff007f] to-purple-600 rounded-2xl flex items-center justify-center shadow-lg shadow-[#ff007f]/20">
                        <Zap className="w-6 h-6 text-white" />
                    </div>
                    <div>
                        <h1 className="text-xl font-display font-black text-white tracking-wide">
                            Eeshtronics<span className="text-[#ff007f]">.</span>
                        </h1>
                        <p className="text-[10px] text-slate-400 font-semibold tracking-widest uppercase">Academy</p>
                    </div>
                </motion.div>
            </div>

            <nav className="flex-1 px-4 space-y-2 overflow-y-auto">
                {navigation.map((item, index) => {
                    const isActive = location.pathname === item.href;
                    return (
                        <motion.div
                            key={item.name}
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: index * 0.05 }}
                        >
                            <Link
                                to={item.href}
                                className={`flex items-center gap-3 px-4 py-3 rounded-full transition-all duration-300 group ${isActive
                                        ? 'bg-gradient-to-r from-[#ff007f]/15 to-purple-600/15 text-white border border-[#ff007f]/30 shadow-[0_0_15px_rgba(255,0,127,0.1)]'
                                        : 'text-slate-400 hover:text-white hover:bg-white/5'
                                    }`}
                            >
                                <item.icon className={`w-5 h-5 ${isActive ? 'text-[#ff007f]' : 'group-hover:text-[#ff007f]'} transition-colors duration-300`} />
                                <span className="flex-1 font-medium text-sm">{item.name}</span>
                                {isActive && (
                                    <motion.div
                                        layoutId="activeIndicator"
                                        className="w-1.5 h-1.5 bg-[#ff007f] rounded-full shadow-[0_0_8px_#ff007f]"
                                    />
                                )}
                                <ChevronRight className="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity" />
                            </Link>
                        </motion.div>
                    );
                })}
            </nav>

            {user && (
                <div className="p-4 border-t border-[#ff007f]/10">
                    <div className="glass rounded-[2rem] p-4 flex flex-col gap-3 border-[#ff007f]/10 shadow-[0_0_15px_rgba(255,0,127,0.02)]">
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 bg-gradient-to-br from-[#ff007f] to-purple-600 rounded-full flex items-center justify-center text-white font-bold shadow-md shadow-[#ff007f]/20">
                                {getInitials(user.username)}
                            </div>
                            <div className="flex-1 min-w-0">
                                <p className="text-sm font-semibold text-white truncate">{user.username}</p>
                                <p className="text-xs text-slate-400">Level {user.level || 1} Engineer</p>
                            </div>
                        </div>
                        <button
                            onClick={logout}
                            className="flex items-center justify-center gap-2 w-full py-2 px-3 rounded-full text-xs font-semibold text-[#ff007f] hover:text-white hover:bg-[#ff007f]/20 border border-[#ff007f]/20 hover:border-[#ff007f]/50 shadow-sm transition-all duration-300"
                        >
                            <LogOut className="w-3.5 h-3.5" />
                            Log Out
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};
