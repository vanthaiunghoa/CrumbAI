import { Heading } from '@/components/heading';
import { SubscriptionButton } from '@/components/subscription-button';
import { checkSubscription } from '@/lib/subscription';
import { Settings } from "lucide-react";

const SettingsPage = async () => {
    const isUnlimited = await checkSubscription();
    return (
        <div>
            <Heading
                title="Settings"
                description="Manage your account settings"
                icon={Settings}
                iconColor="#F3B13F"
                bgColor="bg-violet=500/10"
            />
            <div className='px-4 lg:px-8 space-y-4'>
                <div className="text-white text-sm">
                    {isUnlimited ? "Current Plan: UNLIMITED." : "Current Plan: FREE TRIAL."}
                </div>
                <SubscriptionButton isUnlimited={isUnlimited} />
            </div>
        </div>
    );
}

export default SettingsPage;