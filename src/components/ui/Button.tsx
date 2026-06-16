import React from 'react';
import { motion } from 'framer-motion';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
    size?: 'sm' | 'md' | 'lg';
    children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
    variant = 'primary',
    size = 'md',
    children,
    className = '',
    ...props
}) => {
    const baseStyles = 'font-semibold rounded-full transition-all duration-300 inline-flex items-center justify-center gap-2';

    const variantStyles = {
        primary: 'border border-[#ff007f] text-[#ff007f] bg-transparent hover:bg-[#ff007f] hover:text-black shadow-lg shadow-[#ff007f]/10 hover:shadow-xl hover:shadow-[#ff007f]/45',
        secondary: 'border border-purple-500 text-purple-400 bg-transparent hover:bg-purple-500 hover:text-white shadow-lg shadow-purple-500/10 hover:shadow-[#ff007f]/30',
        ghost: 'glass glass-hover text-slate-200 border-white/10 hover:border-[#ff007f]/30',
        danger: 'border border-red-500 text-red-500 bg-transparent hover:bg-red-500 hover:text-white shadow-lg shadow-red-500/10',
    };

    const sizeStyles = {
        sm: 'px-4 py-1.5 text-sm',
        md: 'px-6 py-2.5 text-base',
        lg: 'px-8 py-3.5 text-lg',
    };

    return (
        <motion.button
            whileHover={{ scale: 1.04 }}
            whileTap={{ scale: 0.96 }}
            className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${className}`}
            onClick={props.onClick}
            disabled={props.disabled}
            type={props.type}
        >
            {children}
        </motion.button>
    );
};
