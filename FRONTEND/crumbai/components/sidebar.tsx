"use client";

import Link from "next/link";
import Image from "next/image";
import { Inter } from "next/font/google";
import { cn } from "@/lib/utils";
import { LayoutDashboard, Video, ListVideo, ImageDown, ScrollText, Music, TrendingUp, Settings } from "lucide-react";
import { FreeCounter } from "./free-counter";
import { ModeToggle } from "./theme-toggle";

const inter = Inter({subsets: ["latin"]});

const routes = [
    {
        label: "Dashboard",
        icon: LayoutDashboard,
        href: "/dashboard",
        color: "#F3B13F",
    },
    {
        label: "Your Clips",
        icon: ListVideo,
        href: "/clips",
        color: "#F3B13F",
    },
    {
        label: "Generate Shorts",
        icon: Video,
        href: "/shorts",
        color: "#F3B13F",
    },
    {
        label: "Generate Descriptions & Tags",
        icon: ScrollText,
        href: "/descriptions",
        color: "#F3B13F",
    },
    {
        label: "Generate Thumbnails",
        icon: ImageDown,
        href: "/thumbnails",
        color: "#F3B13F",
    },
    {
        label: "Generate Audio",
        icon: Music,
        href: "/audio",
        color: "#F3B13F",
    },
    {
        label: "Tips/Trends",
        icon: TrendingUp,
        href: "/tips",
        color: "#F3B13F",
    },
    {
        label: "Settings",
        icon: Settings,
        href: "/settings",
        color: "#F3B13F",
    },
]

interface SidebarProps {
    apiLimitCount: number;
    isUnlimited: boolean;
};

const Sidebar = ({
    apiLimitCount = 0,
    isUnlimited = false
}) => {
    return (
        <div className="space-y-4 py-4 flex flex-col h-full bg-[#1E1E1E] text-white">
            <div className="px-3 py-2 flex-1">
                <Link href="/" className="flex items-center pl-3 mb-14">
                    <div className="relative w-12 h-12 mr-4">
                        <Image
                            fill
                            alt="Logo"
                            src="/logo.png"
                        />
                    </div>
                    <h1 className={cn("pt-4 text-2xl font-bold", inter.className)}>
                        CrumbAI
                    </h1>
                </Link>
                <div className="space-y-1">
                    {routes.map((route) => (
                        <Link href={route.href} key={route.href} className="text-sm group flex p-3 w-full justify-start font-medium cursor-pointer hover:text-white hover:bg-white/10 rounded-lg">
                            <div className="flex items-center flex-1">
                                <route.icon className={cn("h-5 w-5 mr-3")} style={{ color: route.color }} />
                                {route.label}
                            </div>
                        </Link>
                    ))}
                </div>
            </div>
            <FreeCounter
                isUnlimited={isUnlimited}
                apiLimitCount={apiLimitCount}
            />
        </div>
    )
}

export default Sidebar;