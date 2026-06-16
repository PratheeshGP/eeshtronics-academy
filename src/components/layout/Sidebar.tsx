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
    LogOut
} from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';

const navigation = [
    { name: 'Home', href: '/dashboard', icon: Home },
    { name: 'Playground', href: '/playground', icon: Zap },
    { name: 'Missions', href: '/missions', icon: Trophy },
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
        <div className="w-72 h-screen glass border-r border-white/10 flex flex-col">
            <div className="p-6">
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex items-center gap-3"
                >
                    <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-lg flex items-center justify-center">
                        <Zap className="w-6 h-6 text-white" />
                    </div>
                    <div>
                        <h1 className="text-xl font-display font-bold gradient-text">Eeshtronics</h1>
                        <p className="text-xs text-slate-400">Academy Playground</p>
                    </div>
                </motion.div>
            </div>

            <nav className="flex-1 px-4 space-y-2">
                {navigation.map((item, index) => {
                    const isActive = location.pathname === item.href;
                    return (
                        <motion.div
                            key={item.name}
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: index * 0.1 }}
                        >
                            <Link
                                to={item.href}
                                className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 group ${isActive
                                        ? 'bg-gradient-to-r from-primary-600/30 to-secondary-600/30 text-white border border-primary-500/30'
                                        : 'text-slate-400 hover:text-white hover:bg-white/5'
                                    }`}
                            >
                                <item.icon className={`w-5 h-5 ${isActive ? 'text-primary-400' : 'group-hover:text-primary-400'}`} />
                                <span className="flex-1 font-medium">{item.name}</span>
                                {isActive && (
                                    <motion.div
                                        layoutId="activeIndicator"
                                        className="w-1.5 h-1.5 bg-primary-400 rounded-full"
                                    />
                                )}
                                <ChevronRight className="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity" />
                            </Link>
                        </motion.div>
                    );
                })}
            </nav>

            {user && (
                <div className="p-4 border-t border-white/10">
                    <div className="glass rounded-xl p-4 flex flex-col gap-3">
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 bg-gradient-to-br from-accent-500 to-accent-600 rounded-full flex items-center justify-center text-white font-bold">
                                {getInitials(user.username)}
                            </div>
                            <div className="flex-1 min-w-0">
                                <p className="text-sm font-semibold text-white truncate">{user.username}</p>
                                <p className="text-xs text-slate-400">Level {user.level || 1} Engineer</p>
                            </div>
                        </div>
                        <button
                            onClick={logout}
                            className="flex items-center justify-center gap-2 w-full py-2 px-3 rounded-lg text-xs font-medium text-red-400 hover:text-white hover:bg-red-500/20 border border-red-500/20 hover:border-red-500/50 transition-all duration-300"
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
