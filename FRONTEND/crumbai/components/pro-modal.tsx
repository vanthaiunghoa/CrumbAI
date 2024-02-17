"use client"

import { useProModal } from "@/hooks/use-pro-modal"
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "./ui/dialog"
import { Badge } from "./ui/badge";
import { Check, Zap } from "lucide-react";
import { Button } from "./ui/button";

export const ProModal = () => {
    const proModal = useProModal();

    return (
        <Dialog open={proModal.isOpen} onOpenChange={proModal.onClose}>
            <DialogContent>
                <DialogHeader>
                    <DialogTitle className="flex justify-center items-center flex-col gap-y-4 pb-2">
                        <div className="flex items-center font-bold py-2">
                            Upgrade to CrumbAI 
                            <Badge className="text-sm py-1 ml-2" variant={"crumbai"}>
                                UNLIMITED
                            </Badge>
                        </div>
                    </DialogTitle>
                    <DialogDescription className="text-center pt-2 space-y-2 text-zinc-900 font-medium">
                        <Check /> Unlimited Short Generation
                    </DialogDescription>
                </DialogHeader>
                <DialogFooter>
                    <Button size="lg" variant={"crumbai"} className="w-full">
                        Upgrade
                        <Zap className="w-4 h-4 ml-2" />
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    )
}