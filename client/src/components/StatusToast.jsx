import { useEffect } from 'react';
import { CheckCircle2, AlertCircle, X } from 'lucide-react';

const StatusToast = ({ status, onClose }) => {
    if (!status.message) return null;

    useEffect(() => {
        if (status.message) {
            const timer = setTimeout(() => {
                onClose();
            }, 2000);
            return () => clearTimeout(timer);
        }
    }, [status.message, onClose]);

    return (
        <div className="fixed top-4 left-1/2 -translate-x-1/2 z-50 transition-opacity duration-300">
            <div className={`w-96 p-4 rounded-md flex items-center justify-between shadow-lg ${
                status.type === 'success' ? 'bg-green-900/90 text-green-400' : 'bg-red-900/90 text-red-400'
            }`}>
                <div className="flex items-center space-x-2">
                    {status.type === 'success' ? 
                        <CheckCircle2 className="shrink-0" size={20} /> : 
                        <AlertCircle className="shrink-0" size={20} />
                    }
                    <span className="text-sm font-medium">{status.message}</span>
                </div>
                <button 
                    onClick={onClose}
                    className="shrink-0 hover:opacity-75 transition-opacity"
                >
                    <X size={20} />
                </button>
            </div>
        </div>
    );
};

export default StatusToast;