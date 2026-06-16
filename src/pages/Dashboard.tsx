import React from 'react';
import { motion } from 'framer-motion';
import { Card, Badge } from '../components/ui';
import { Zap, TrendingUp, Award, Clock } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

export const Dashboard: React.FC = () => {
    const { user } = useAuth();

    const stats = [
        { label: 'Current Level', value: user?.level?.toString() || '1', icon: Award, color: 'text-primary-400' },
        { label: 'XP Points', value: user?.xp_points?.toLocaleString() || '0', icon: TrendingUp, color: 'text-accent-400' },
        { label: 'Hours Practiced', value: '48', icon: Clock, color: 'text-secondary-400' },
        { label: 'Ether Balance', value: user?.ether_balance?.toLocaleString() || '0', icon: Zap, color: 'text-yellow-400' },
    ];

    const recentMissions = [
        { title: 'Digital Logic Gates', status: 'completed', progress: 100 },
        { title: 'Combinational Circuits', status: 'in-progress', progress: 60 },
        { title: 'Sequential Logic', status: 'locked', progress: 0 },
    ];

    return (
        <div className="max-w-7xl mx-auto space-y-8">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <h1 className="text-4xl font-display font-bold mb-2">
                    Welcome back, <span className="gradient-text">{user?.username || 'Engineer'}</span>!
                </h1>
                <p className="text-slate-400">Continue your engineering journey where you left off.</p>
            </motion.div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                {stats.map((stat, index) => (
                    <motion.div
                        key={stat.label}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.1 }}
                    >
                        <Card hover={false} className="border border-white/10">
                            <div className="flex items-center justify-between mb-2">
                                <stat.icon className={`w-5 h-5 ${stat.color}`} />
                            </div>
                            <div className="text-3xl font-bold text-white mb-1">{stat.value}</div>
                            <div className="text-sm text-slate-400">{stat.label}</div>
                        </Card>
                    </motion.div>
                ))}
            </div>

            {/* Recent Missions */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
            >
                <h2 className="text-2xl font-display font-bold mb-6">Your Missions</h2>
                <div className="space-y-4">
                    {recentMissions.map((mission, index) => (
                        <Card key={mission.title} className="border border-white/10">
                            <div className="flex items-center justify-between">
                                <div className="flex-1">
                                    <div className="flex items-center gap-3 mb-3">
                                        <h3 className="text-lg font-semibold text-white">{mission.title}</h3>
                                        <Badge
                                            variant={
                                                mission.status === 'completed' ? 'accent' :
                                                    mission.status === 'in-progress' ? 'primary' :
                                                        'default'
                                            }
                                        >
                                            {mission.status.replace('-', ' ')}
                                        </Badge>
                                    </div>
                                    <div className="w-full bg-slate-800 rounded-full h-2">
                                        <motion.div
                                            initial={{ width: 0 }}
                                            animate={{ width: `${mission.progress}%` }}
                                            transition={{ delay: 0.5 + index * 0.1, duration: 0.8 }}
                                            className="bg-gradient-to-r from-primary-500 to-secondary-500 h-2 rounded-full"
                                        />
                                    </div>
                                </div>
                                <div className="ml-6 text-2xl font-bold text-slate-600">
                                    {mission.progress}%
                                </div>
                            </div>
                        </Card>
                    ))}
                </div>
            </motion.div>

            {/* Quick Actions */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 }}
            >
                <h2 className="text-2xl font-display font-bold mb-6">Quick Actions</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <Card className="border border-white/10 cursor-pointer">
                        <div className="text-center">
                            <div className="w-16 h-16 bg-gradient-to-br from-primary-500 to-primary-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
                                <Zap className="w-8 h-8 text-white" />
                            </div>
                            <h3 className="text-lg font-semibold text-white mb-2">Enter Playground</h3>
                            <p className="text-sm text-slate-400">Start simulating circuits</p>
                        </div>
                    </Card>

                    <Card className="border border-white/10 cursor-pointer">
                        <div className="text-center">
                            <div className="w-16 h-16 bg-gradient-to-br from-secondary-500 to-secondary-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
                                <Award className="w-8 h-8 text-white" />
                            </div>
                            <h3 className="text-lg font-semibold text-white mb-2">Browse Missions</h3>
                            <p className="text-sm text-slate-400">Discover new challenges</p>
                        </div>
                    </Card>

                    <Card className="border border-white/10 cursor-pointer">
                        <div className="text-center">
                            <div className="w-16 h-16 bg-gradient-to-br from-accent-500 to-accent-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
                                <TrendingUp className="w-8 h-8 text-white" />
                            </div>
                            <h3 className="text-lg font-semibold text-white mb-2">View Progress</h3>
                            <p className="text-sm text-slate-400">Track your growth</p>
                        </div>
                    </Card>
                </div>
            </motion.div>
        </div>
    );
};
