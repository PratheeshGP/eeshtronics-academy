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
            whileHover={hover ? { y: -5, scale: 1.02 } : {}}
            transition={{ duration: 0.3 }}
            className={`glass rounded-2xl p-6 ${hover ? 'glass-hover' : ''} ${className}`}
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
        primary: 'bg-primary-500/20 text-primary-300 border-primary-500/30',
        secondary: 'bg-secondary-500/20 text-secondary-300 border-secondary-500/30',
        accent: 'bg-accent-500/20 text-accent-300 border-accent-500/30',
        default: 'bg-slate-700/50 text-slate-300 border-slate-600/50',
    };

    return (
        <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold border ${variantStyles[variant]} ${className}`}>
            {children}
        </span>
    );
};
