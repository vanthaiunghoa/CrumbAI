import { AlertTriangle, CheckCircle } from "lucide-react";

export const SubscriptionStatus = ({ 
    isUnlimited = false
}: {
    isUnlimited: boolean;
}) => (
    <div className={`text-sm font-semibold px-4 py-2 rounded-lg ${isUnlimited ? 'bg-green-200 text-green-800' : 'bg-yellow-200 text-yellow-800'} inline-flex items-center space-x-2`}>
        <span>{isUnlimited ? "Current Plan: UNLIMITED" : "Current Plan: FREE TRIAL"}</span>
        {isUnlimited ? <CheckCircle className="w-5 h-5" /> : <AlertTriangle className="w-5 h-5" />}
    </div>
);