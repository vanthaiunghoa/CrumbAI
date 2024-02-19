import React from "react";
import { Heading } from "@/components/heading";
import { SubscriptionStatus } from "@/components/subscription-status";
import { SubscriptionButton } from "@/components/subscription-button";
import { checkSubscription } from "@/lib/subscription";
import { Settings } from "lucide-react";
import { getServerSession } from "next-auth";

const SettingsPage = async () => {
  const isUnlimited = await checkSubscription();
  const session = await getServerSession();

  return (
    <div className="space-y-8">
      <Heading
        title="Settings"
        description="View & Manager your account."
        icon={Settings}
        iconColor="#F3B13F"
        bgColor="bg-violet-500/10"
      />
      <div className="px-4 space-y-4 lg:px-8">
        <SubscriptionStatus isUnlimited={isUnlimited} />
        <br></br>
        <SubscriptionButton isUnlimited={isUnlimited} />

        <h2 className="text-lg font-semibold">
          Email:{" "}
          <span className="text-sm text-gray-400">{session?.user?.email}</span>
        </h2>
      </div>
    </div>
  );
};

export default SettingsPage;
