import React from 'react';
import { motion } from 'framer-motion';

interface CardProps {
    children: React.ReactNode;
    className?: string;
    hover?: boolean;
}

export const Card: React.FC<CardProps> = ({ children, className = '', hover = true }) => {
    return (
        <motion.div
            whileHover={hover ? { y: -5, scale: 1.01 } : {}}
            transition={{ duration: 0.3 }}
            className={`glass rounded-3xl p-6 ${hover ? 'glass-hover' : ''} ${className}`}
        >
            {children}
        </motion.div>
    );
};

interface BadgeProps {
    children: React.ReactNode;
    variant?: 'primary' | 'secondary' | 'accent' | 'default';
    className?: string;
}

export const Badge: React.FC<BadgeProps> = ({
    children,
    variant = 'default',
    className = ''
}) => {
    const variantStyles = {
        primary: 'bg-pink-500/15 text-pink-400 border-pink-500/25',
        secondary: 'bg-purple-500/15 text-purple-400 border-purple-500/25',
        accent: 'bg-cyan-500/15 text-cyan-400 border-cyan-500/25',
        default: 'bg-slate-800/60 text-slate-300 border-slate-700/60',
    };

    return (
        <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold border ${variantStyles[variant]} ${className}`}>
            {children}
        </span>
    );
};
