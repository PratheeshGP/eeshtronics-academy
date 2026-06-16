import React from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, Zap, Trophy, Users, Sparkles, Code } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui';

export const LandingPage: React.FC = () => {
    const features = [
        {
            icon: Zap,
            title: 'Interactive Playgrounds',
            description: 'Hands-on learning with real-time VLSI, Digital Electronics, and Embedded Systems simulations.',
            color: 'from-primary-500 to-primary-600',
        },
        {
            icon: Trophy,
            title: 'Mission-Based Learning',
            description: 'Progress through structured missions designed to build your skills systematically.',
            color: 'from-secondary-500 to-secondary-600',
        },
        {
            icon: Sparkles,
            title: 'AI Mentor',
            description: 'Get personalized guidance and instant feedback from our advanced AI teaching assistant.',
            color: 'from-accent-500 to-accent-600',
        },
        {
            icon: Users,
            title: 'Clan System',
            description: 'Collaborate with peers, share knowledge, and compete in engineering challenges.',
            color: 'from-purple-500 to-purple-600',
        },
    ];

    return (
        <div className="min-h-screen">
            {/* Hero Section */}
            <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
                {/* Animated Background */}
                <div className="absolute inset-0 overflow-hidden">
                    <div className="absolute w-96 h-96 bg-primary-500/20 rounded-full blur-3xl -top-48 -left-48 animate-pulse"></div>
                    <div className="absolute w-96 h-96 bg-secondary-500/20 rounded-full blur-3xl -bottom-48 -right-48 animate-pulse" style={{ animationDelay: '1s' }}></div>
                    <div className="absolute w-96 h-96 bg-accent-500/20 rounded-full blur-3xl top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 animate-pulse" style={{ animationDelay: '2s' }}></div>
                </div>

                <div className="relative z-10 max-w-7xl mx-auto px-8 text-center">
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8 }}
                    >
                        <div className="inline-flex items-center gap-2 px-4 py-2 glass rounded-full mb-6">
                            <Sparkles className="w-4 h-4 text-accent-400" />
                            <span className="text-sm text-slate-300">Powered by Advanced AI</span>
                        </div>

                        <h1 className="text-7xl md:text-8xl font-display font-black mb-6 leading-tight">
                            Master Engineering
                            <br />
                            <span className="gradient-text animate-gradient bg-gradient-to-r from-primary-400 via-secondary-400 to-accent-400">
                                The Fun Way
                            </span>
                        </h1>

                        <p className="text-xl md:text-2xl text-slate-400 max-w-3xl mx-auto mb-12">
                            Dive into Digital Electronics, VLSI, and Embedded Systems with interactive playgrounds,
                            AI mentorship, and a thriving community of engineers.
                        </p>

                        <div className="flex items-center gap-4 justify-center">
                            <Link to="/dashboard">
                                <Button size="lg" variant="primary">
                                    Start Learning
                                    <ArrowRight className="w-5 h-5" />
                                </Button>
                            </Link>
                            <Button size="lg" variant="ghost">
                                <Code className="w-5 h-5" />
                                View Demo
                            </Button>
                        </div>

                        <div className="mt-16 flex items-center justify-center gap-12 text-sm text-slate-500">
                            <div>
                                <div className="text-3xl font-bold gradient-text">10K+</div>
                                <div>Engineers</div>
                            </div>
                            <div className="w-px h-12 bg-white/10"></div>
                            <div>
                                <div className="text-3xl font-bold gradient-text">500+</div>
                                <div>Missions</div>
                            </div>
                            <div className="w-px h-12 bg-white/10"></div>
                            <div>
                                <div className="text-3xl font-bold gradient-text">95%</div>
                                <div>Success Rate</div>
                            </div>
                        </div>
                    </motion.div>
                </div>
            </section>

            {/* Features Section */}
            <section className="relative py-32 px-8">
                <div className="max-w-7xl mx-auto">
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        className="text-center mb-20"
                    >
                        <h2 className="text-5xl font-display font-bold mb-6">
                            Everything You Need to
                            <span className="gradient-text"> Excel</span>
                        </h2>
                        <p className="text-xl text-slate-400 max-w-2xl mx-auto">
                            A comprehensive platform designed to transform the way you learn and practice engineering.
                        </p>
                    </motion.div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        {features.map((feature, index) => (
                            <motion.div
                                key={feature.title}
                                initial={{ opacity: 0, y: 30 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }}
                                transition={{ delay: index * 0.1 }}
                                whileHover={{ y: -10 }}
                                className="glass rounded-3xl p-8 glass-hover border border-white/10"
                            >
                                <div className={`w-16 h-16 bg-gradient-to-br ${feature.color} rounded-2xl flex items-center justify-center mb-6 shadow-lg`}>
                                    <feature.icon className="w-8 h-8 text-white" />
                                </div>
                                <h3 className="text-2xl font-display font-bold mb-4 text-white">
                                    {feature.title}
                                </h3>
                                <p className="text-slate-400 leading-relaxed">
                                    {feature.description}
                                </p>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="relative py-32 px-8">
                <div className="max-w-4xl mx-auto">
                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        whileInView={{ opacity: 1, scale: 1 }}
                        viewport={{ once: true }}
                        className="glass rounded-3xl p-12 text-center border border-white/10 relative overflow-hidden"
                    >
                        <div className="absolute inset-0 bg-gradient-to-r from-primary-500/10 via-secondary-500/10 to-accent-500/10 animate-gradient"></div>
                        <div className="relative z-10">
                            <h2 className="text-5xl font-display font-bold mb-6">
                                Ready to Start Your
                                <span className="gradient-text"> Engineering Journey?</span>
                            </h2>
                            <p className="text-xl text-slate-400 mb-8 max-w-2xl mx-auto">
                                Join thousands of engineers who are already mastering their craft with Eeshtronics Academy.
                            </p>
                            <Link to="/dashboard">
                                <Button size="lg" variant="primary">
                                    Get Started Now
                                    <ArrowRight className="w-5 h-5" />
                                </Button>
                            </Link>
                        </div>
                    </motion.div>
                </div>
            </section>
        </div>
    );
};
