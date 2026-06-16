import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
    UploadCloud, FileText, CheckCircle2, AlertCircle, Clock, 
    Trash2, Save, X, Plus, ExternalLink, RefreshCw 
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { Card, Badge, Button } from '../components/ui';

interface Requirement {
    id: number;
    username: string;
    title: string;
    description: string;
    file: string;
    file_name: string;
    status: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED' | 'REJECTED';
    admin_notes: string;
    completed_at: string | null;
    created_at: string;
    updated_at: string;
}

export default function RequirementsTracker() {
    const { user } = useAuth();
    const [requirements, setRequirements] = useState<Requirement[]>([]);
    const [loading, setLoading] = useState(true);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    // Form states (user upload)
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [showUploadForm, setShowUploadForm] = useState(false);

    // Edit states (admin view)
    const [editingItem, setEditingItem] = useState<Requirement | null>(null);
    const [adminStatus, setAdminStatus] = useState<'PENDING' | 'IN_PROGRESS' | 'COMPLETED' | 'REJECTED'>('PENDING');
    const [adminNotes, setAdminNotes] = useState('');
    const [updatingAdmin, setUpdatingAdmin] = useState(false);

    const fetchRequirements = async () => {
        setLoading(true);
        setError('');
        try {
            const token = localStorage.getItem('access_token');
            const res = await fetch('/api/progress/requirements/', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            if (!res.ok) throw new Error('Failed to fetch requirements');
            const data = await res.json();
            setRequirements(data);
        } catch (err: any) {
            setError(err.message || 'An error occurred while fetching requirements.');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchRequirements();
    }, []);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
            setSelectedFile(e.target.files[0]);
        }
    };

    const handleUploadSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setSuccess('');
        if (!selectedFile) {
            setError('Please select a file to upload.');
            return;
        }

        setUploading(true);
        try {
            const token = localStorage.getItem('access_token');
            const formData = new FormData();
            formData.append('title', title);
            formData.append('description', description);
            formData.append('file', selectedFile);

            const res = await fetch('/api/progress/requirements/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData
            });

            if (!res.ok) {
                const errData = await res.json();
                throw new Error(errData.detail || 'Upload failed');
            }

            setSuccess('Requirement uploaded successfully!');
            setTitle('');
            setDescription('');
            setSelectedFile(null);
            setShowUploadForm(false);
            fetchRequirements();
        } catch (err: any) {
            setError(err.message || 'An error occurred during upload.');
        } finally {
            setUploading(false);
        }
    };

    const handleAdminUpdate = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!editingItem) return;

        setUpdatingAdmin(true);
        setError('');
        setSuccess('');
        try {
            const token = localStorage.getItem('access_token');
            const res = await fetch(`/api/progress/requirements/${editingItem.id}/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    status: adminStatus,
                    admin_notes: adminNotes
                })
            });

            if (!res.ok) throw new Error('Failed to update requirement');
            
            setSuccess('Requirement updated successfully.');
            setEditingItem(null);
            fetchRequirements();
        } catch (err: any) {
            setError(err.message || 'Failed to update requirement.');
        } finally {
            setUpdatingAdmin(false);
        }
    };

    const handleDelete = async (id: number) => {
        if (!confirm('Are you sure you want to delete this requirement?')) return;
        
        setError('');
        setSuccess('');
        try {
            const token = localStorage.getItem('access_token');
            const res = await fetch(`/api/progress/requirements/${id}/`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!res.ok) throw new Error('Failed to delete requirement');
            
            setSuccess('Requirement deleted successfully.');
            fetchRequirements();
        } catch (err: any) {
            setError(err.message || 'Failed to delete.');
        }
    };

    const getStatusIcon = (status: string) => {
        switch (status) {
            case 'COMPLETED': return <CheckCircle2 className="w-5 h-5 text-emerald-400" />;
            case 'REJECTED': return <AlertCircle className="w-5 h-5 text-rose-400" />;
            case 'IN_PROGRESS': return <Clock className="w-5 h-5 text-purple-400 animate-pulse" />;
            default: return <Clock className="w-5 h-5 text-slate-400" />;
        }
    };

    const getStatusBadgeVariant = (status: string) => {
        switch (status) {
            case 'COMPLETED': return 'accent';
            case 'REJECTED': return 'default';
            case 'IN_PROGRESS': return 'secondary';
            default: return 'primary';
        }
    };

    return (
        <div className="max-w-7xl mx-auto space-y-8 relative pb-20">
            {/* Header section */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                >
                    <h1 className="text-4xl font-display font-black mb-2">
                        Requirements & <span className="text-[#ff007f] drop-shadow-[0_0_8px_rgba(255,0,127,0.3)]">Uploads</span>
                    </h1>
                    <p className="text-slate-400">
                        {user?.is_staff 
                            ? 'Admin Console: Review and track user submissions.' 
                            : 'Upload documents, designs, or resources and track review progress.'}
                    </p>
                </motion.div>

                <div className="flex gap-2">
                    <Button onClick={fetchRequirements} variant="ghost" size="sm" className="rounded-full">
                        <RefreshCw className="w-4 h-4" />
                    </Button>
                    {!user?.is_staff && (
                        <Button 
                            onClick={() => setShowUploadForm(!showUploadForm)} 
                            variant="primary" 
                            size="sm"
                            className="rounded-full"
                        >
                            {showUploadForm ? <X className="w-4 h-4" /> : <Plus className="w-4 h-4" />}
                            {showUploadForm ? 'Cancel' : 'New Upload'}
                        </Button>
                    )}
                </div>
            </div>

            {/* Notification Messages */}
            <AnimatePresence>
                {error && (
                    <motion.div 
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0 }}
                        className="p-4 bg-red-500/10 border border-red-500/30 rounded-2xl text-red-400 text-sm flex gap-3 items-center"
                    >
                        <AlertCircle className="w-5 h-5" />
                        <span>{error}</span>
                    </motion.div>
                )}
                {success && (
                    <motion.div 
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0 }}
                        className="p-4 bg-emerald-500/10 border border-emerald-500/30 rounded-2xl text-emerald-400 text-sm flex gap-3 items-center"
                    >
                        <CheckCircle2 className="w-5 h-5" />
                        <span>{success}</span>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* User Upload Form Panel */}
            <AnimatePresence>
                {showUploadForm && (
                    <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        className="overflow-hidden"
                    >
                        <Card className="border border-[#ff007f]/25 rounded-[2rem] p-8 max-w-xl mx-auto shadow-lg shadow-[#ff007f]/5">
                            <h2 className="text-xl font-bold mb-6 text-white flex items-center gap-2">
                                <UploadCloud className="w-5 h-5 text-[#ff007f]" />
                                Upload Requirement
                            </h2>
                            <form onSubmit={handleUploadSubmit} className="space-y-4">
                                <div>
                                    <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 ml-4">
                                        Title / Name
                                    </label>
                                    <input 
                                        type="text"
                                        value={title}
                                        onChange={(e) => setTitle(e.target.value)}
                                        className="w-full bg-slate-950/50 border border-white/10 rounded-full py-3 px-6 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-[#ff007f] focus:ring-1 focus:ring-[#ff007f] transition-all"
                                        placeholder="e.g. Logic Gates Lab Note"
                                        required
                                    />
                                </div>
                                <div>
                                    <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 ml-4">
                                        Description / Details
                                    </label>
                                    <textarea 
                                        value={description}
                                        onChange={(e) => setDescription(e.target.value)}
                                        className="w-full bg-slate-950/50 border border-white/10 rounded-3xl py-3 px-6 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-[#ff007f] focus:ring-1 focus:ring-[#ff007f] min-h-[100px] transition-all"
                                        placeholder="Explain what is included in this document..."
                                        required
                                    />
                                </div>
                                <div>
                                    <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 ml-4">
                                        Select File
                                    </label>
                                    <div className="relative">
                                        <input 
                                            type="file"
                                            onChange={handleFileChange}
                                            className="hidden"
                                            id="requirement-file"
                                            required
                                        />
                                        <label 
                                            htmlFor="requirement-file"
                                            className="flex items-center justify-center gap-2 w-full bg-slate-950/30 hover:bg-slate-950/60 border border-dashed border-white/20 hover:border-[#ff007f]/50 text-slate-400 hover:text-[#ff007f] py-4 rounded-full cursor-pointer transition-all"
                                        >
                                            <UploadCloud className="w-5 h-5" />
                                            <span>{selectedFile ? selectedFile.name : 'Choose file...'}</span>
                                        </label>
                                    </div>
                                </div>
                                <div className="pt-2 flex justify-end gap-2">
                                    <Button 
                                        type="button" 
                                        onClick={() => setShowUploadForm(false)} 
                                        variant="ghost"
                                        className="rounded-full"
                                    >
                                        Cancel
                                    </Button>
                                    <Button 
                                        type="submit" 
                                        disabled={uploading} 
                                        variant="primary"
                                        className="rounded-full"
                                    >
                                        {uploading ? 'Uploading...' : 'Submit Upload'}
                                    </Button>
                                </div>
                            </form>
                        </Card>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Main Listings Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Requirements list */}
                <div className={`space-y-4 ${editingItem ? 'lg:col-span-2' : 'lg:col-span-3'}`}>
                    {loading ? (
                        <div className="flex flex-col items-center py-20 gap-4">
                            <div className="w-10 h-10 border-4 border-[#ff007f]/20 border-t-[#ff007f] rounded-full animate-spin"></div>
                            <p className="text-slate-500 text-sm">Fetching requirements...</p>
                        </div>
                    ) : requirements.length === 0 ? (
                        <Card hover={false} className="border border-white/5 text-center py-16 rounded-[2rem]">
                            <FileText className="w-12 h-12 text-slate-600 mx-auto mb-4" />
                            <h3 className="text-xl font-bold text-white mb-2">No Requirements Found</h3>
                            <p className="text-slate-500 max-w-md mx-auto mb-6">
                                {user?.is_staff 
                                    ? 'No users have submitted requirements yet.' 
                                    : 'You have not uploaded any requirements yet. Submit files or document drafts to get started.'}
                            </p>
                            {!user?.is_staff && (
                                <Button onClick={() => setShowUploadForm(true)} variant="primary" className="rounded-full">
                                    Upload Your First File
                                </Button>
                            )}
                        </Card>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            {requirements.map((req) => (
                                <motion.div key={req.id} layout>
                                    <Card className="border border-[#ff007f]/10 hover:border-[#ff007f]/30 rounded-[2rem] p-6 shadow-md hover:shadow-[#ff007f]/5">
                                        <div className="flex items-start justify-between gap-4 mb-4">
                                            <div>
                                                <Badge variant={getStatusBadgeVariant(req.status)} className="mb-2">
                                                    {req.status.replace('_', ' ')}
                                                </Badge>
                                                <h3 className="text-lg font-bold text-white leading-snug truncate max-w-[220px]">
                                                    {req.title}
                                                </h3>
                                                {user?.is_staff && (
                                                    <span className="text-xs text-purple-400 font-semibold">
                                                        By: @{req.username}
                                                    </span>
                                                )}
                                            </div>
                                            <div className="flex items-center gap-1.5">
                                                {getStatusIcon(req.status)}
                                            </div>
                                        </div>

                                        <p className="text-sm text-slate-400 mb-6 line-clamp-3 min-h-[60px]">
                                            {req.description}
                                        </p>

                                        {/* File download wrapper */}
                                        <div className="p-3 bg-slate-950/50 rounded-2xl flex items-center justify-between gap-4 border border-white/5 mb-6">
                                            <div className="flex items-center gap-2 min-w-0">
                                                <FileText className="w-5 h-5 text-pink-400 shrink-0" />
                                                <span className="text-xs text-slate-300 truncate font-mono">
                                                    {req.file_name}
                                                </span>
                                            </div>
                                            <a 
                                                href={req.file} 
                                                target="_blank" 
                                                rel="noreferrer"
                                                className="p-1.5 hover:bg-[#ff007f]/10 rounded-full text-[#ff007f] transition-all"
                                                title="Open/Download File"
                                            >
                                                <ExternalLink className="w-4 h-4" />
                                            </a>
                                        </div>

                                        {/* Feedback / Admin Notes display */}
                                        {req.admin_notes && (
                                            <div className="p-3 bg-purple-500/5 border border-purple-500/10 rounded-2xl mb-6 text-xs text-slate-300">
                                                <span className="font-semibold text-purple-400 block mb-1">Feedback:</span>
                                                <p className="italic">{req.admin_notes}</p>
                                            </div>
                                        )}

                                        <div className="flex items-center justify-between border-t border-white/5 pt-4">
                                            <span className="text-[10px] text-slate-500 font-mono">
                                                {new Date(req.created_at).toLocaleDateString()}
                                            </span>
                                            
                                            <div className="flex gap-2">
                                                {user?.is_staff && (
                                                    <Button 
                                                        onClick={() => {
                                                            setEditingItem(req);
                                                            setAdminStatus(req.status);
                                                            setAdminNotes(req.admin_notes);
                                                        }}
                                                        variant="ghost" 
                                                        size="sm"
                                                        className="rounded-full px-3 py-1 text-xs"
                                                    >
                                                        Review
                                                    </Button>
                                                )}
                                                {(!user?.is_staff || req.user === user.id) && (
                                                    <button 
                                                        onClick={() => handleDelete(req.id)}
                                                        className="p-2 text-slate-500 hover:text-red-400 hover:bg-red-500/10 rounded-full transition-all"
                                                        title="Delete Submission"
                                                    >
                                                        <Trash2 className="w-4 h-4" />
                                                    </button>
                                                )}
                                            </div>
                                        </div>
                                    </Card>
                                </motion.div>
                            ))}
                        </div>
                    )}
                </div>

                {/* Admin Drawer/Sidebar to update statuses */}
                <AnimatePresence>
                    {editingItem && (
                        <motion.div
                            initial={{ opacity: 0, x: 50 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: 50 }}
                            className="lg:col-span-1"
                        >
                            <Card className="border border-purple-500/30 rounded-[2rem] p-6 shadow-xl shadow-purple-500/5 bg-[#0e0e13]/90 relative">
                                <button 
                                    onClick={() => setEditingItem(null)}
                                    className="absolute right-4 top-4 p-2 text-slate-400 hover:text-white rounded-full hover:bg-white/5 transition-all"
                                >
                                    <X className="w-4 h-4" />
                                </button>

                                <h2 className="text-xl font-bold mb-4 text-white">Review Submission</h2>
                                <div className="mb-6">
                                    <span className="text-[10px] text-slate-500 uppercase tracking-widest block mb-1">Title</span>
                                    <p className="text-sm font-semibold text-slate-200">{editingItem.title}</p>
                                    <span className="text-[10px] text-slate-500 uppercase tracking-widest block mt-3 mb-1">Submitted by</span>
                                    <p className="text-xs text-purple-400 font-semibold">@{editingItem.username}</p>
                                    <span className="text-[10px] text-slate-500 uppercase tracking-widest block mt-3 mb-1">Description</span>
                                    <p className="text-xs text-slate-400 italic line-clamp-4">{editingItem.description}</p>
                                </div>

                                <form onSubmit={handleAdminUpdate} className="space-y-4 border-t border-white/5 pt-4">
                                    <div>
                                        <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 ml-4">
                                            Update Status
                                        </label>
                                        <select
                                            value={adminStatus}
                                            onChange={(e: any) => setAdminStatus(e.target.value)}
                                            className="w-full bg-slate-950 border border-white/10 rounded-full py-2.5 px-4 text-sm text-slate-200 focus:outline-none focus:border-purple-500"
                                        >
                                            <option value="PENDING">Pending Review</option>
                                            <option value="IN_PROGRESS">Under Review</option>
                                            <option value="COMPLETED">Completed</option>
                                            <option value="REJECTED">Rejected</option>
                                        </select>
                                    </div>
                                    <div>
                                        <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 ml-4">
                                            Feedback / Notes
                                        </label>
                                        <textarea
                                            value={adminNotes}
                                            onChange={(e) => setAdminNotes(e.target.value)}
                                            className="w-full bg-slate-950 border border-white/10 rounded-2xl py-3 px-4 text-xs text-slate-200 placeholder-slate-600 focus:outline-none focus:border-purple-500 min-h-[120px]"
                                            placeholder="Write admin notes or review details here..."
                                        />
                                    </div>

                                    <div className="flex gap-2 pt-2">
                                        <Button 
                                            type="button" 
                                            onClick={() => setEditingItem(null)} 
                                            variant="ghost"
                                            className="flex-1 rounded-full text-sm"
                                        >
                                            Cancel
                                        </Button>
                                        <Button 
                                            type="submit"
                                            disabled={updatingAdmin}
                                            variant="primary"
                                            className="flex-1 rounded-full text-sm border-purple-500 text-purple-400 hover:bg-purple-500 hover:text-black shadow-purple-500/20"
                                        >
                                            <Save className="w-4 h-4" />
                                            {updatingAdmin ? 'Saving...' : 'Save Notes'}
                                        </Button>
                                    </div>
                                </form>
                            </Card>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
}
