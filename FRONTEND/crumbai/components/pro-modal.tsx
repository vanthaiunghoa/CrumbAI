"use client"

import { useProModal } from "@/hooks/use-pro-modal"
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "./ui/dialog"
import { Badge } from "./ui/badge";
import { Check, Zap } from "lucide-react";
import { Button } from "./ui/button";
import axios from "axios";
import { useState } from "react";

export const ProModal = () => {
    const proModal = useProModal();
    const [loading, setLoading] = useState(false);

    const onSubscribe = async () => {
        try {
            setLoading(true);
            const response = await axios.get("/api/stripe");
            window.location.href = response.data.url;
        } catch (error) {
            console.log(error, "Stripe client error");
        } finally {
            setLoading(false);
        }
    }

    return (
<Dialog open={proModal.isOpen} onOpenChange={proModal.onClose}>
    <DialogContent>
        <DialogHeader>
            <DialogTitle className="flex justify-center items-center flex-col gap-y-4">
                <div className="flex items-center font-bold py-2">
                    Upgrade to CrumbAI 
                    <Badge className="text-sm py-1 ml-2" variant={"crumbai"}>
                        UNLIMITED
                    </Badge>
                </div>
            </DialogTitle>
        </DialogHeader>
        <div className="p-2">
            <DialogDescription className="text-center pt-2 space-y-2 text-zinc-900 font-medium">
                <ul className="space-y-4">
                    <li className="flex items-start">
                        <div className="flex-shrink-0">
                            <Check className="h-6 w-6 text-green-500" aria-hidden="true" />
                        </div>
                        <p className="ml-3 text-base text-gray-500">
                            Unlimited Short Generations
                        </p>
                    </li>
                    <li className="flex items-start">
                        <div className="flex-shrink-0">
                            <Check className="h-6 w-6 text-green-500" aria-hidden="true" />
                        </div>
                        <p className="ml-3 text-base text-gray-500">
                            Unlimited Description Generations
                        </p>
                    </li>
                    <li className="flex items-start">
                        <div className="flex-shrink-0">
                            <Check className="h-6 w-6 text-green-500" aria-hidden="true" />
                        </div>
                        <p className="ml-3 text-base text-gray-500">
                            Unlimited Thumbnail Generations
                        </p>
                    </li>
                    <li className="flex items-start">
                        <div className="flex-shrink-0">
                            <Check className="h-6 w-6 text-green-500" aria-hidden="true" />
                        </div>
                        <p className="ml-3 text-base text-gray-500">
                            Unlimited Soundtrack Generations
                        </p>
                    </li>
                    <li className="flex items-start">
                        <div className="flex-shrink-0">
                            <Check className="h-6 w-6 text-green-500" aria-hidden="true" />
                        </div>
                        <p className="ml-3 text-base text-gray-500">
                            Auto Uploading
                        </p>
                    </li>
                </ul>
            </DialogDescription>
        </div>
        <DialogFooter>
            <Button onClick={onSubscribe} size="lg" variant={"crumbai"} className="w-full mt-4">
                Upgrade
                <Zap className="w-4 h-4 ml-2" />
            </Button>
        </DialogFooter>
    </DialogContent>
</Dialog>
    )
}