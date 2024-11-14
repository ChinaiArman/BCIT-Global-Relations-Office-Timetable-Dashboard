// components/MessageDisplay.jsx
import React from 'react';
import { AlertCircle, CheckCircle2 } from 'lucide-react';

const MessageDisplay = ({ message }) => {
  if (!message.text) return null;

  return (
    <div className={`p-4 rounded-lg flex items-start space-x-3 ${
      message.type === 'error' ? 'bg-red-500/10 text-red-400' : 'bg-green-500/10 text-green-400'
    }`}>
      {message.type === 'error' ? (
        <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
      ) : (
        <CheckCircle2 className="w-5 h-5 flex-shrink-0 mt-0.5" />
      )}
      <div>
        <p className="font-medium">{message.text}</p>
        {message.details && (
          <p className="text-sm mt-1 opacity-80">{message.details}</p>
        )}
      </div>
    </div>
  );
};

export default MessageDisplay;