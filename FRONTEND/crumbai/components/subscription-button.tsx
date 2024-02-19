"use client";

import axios from "axios";
import { useState } from "react";
import { Zap } from "lucide-react";
import { Button } from "@/components/ui/button";

export const SubscriptionButton = ({
    isUnlimited = false
}: {
    isUnlimited: boolean;
}) => {
  const [loading, setLoading] = useState(false);

  const onClick = async () => {
    try {
      setLoading(true);

      const response = await axios.get("/api/stripe");

      window.location.href = response.data.url;
    } catch (error) { 
      console.log("Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Button variant={isUnlimited ? "success" : "crumbai"} disabled={loading} onClick={onClick} >
      {isUnlimited ? "Manage Subscription" : "Upgrade Now"}
      {!isUnlimited && <Zap className="w-4 h-4 ml-2" />}
    </Button>
  )
};