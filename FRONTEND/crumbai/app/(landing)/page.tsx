"use client";

import { Montserrat } from "next/font/google";
import Image from "next/image"
import Link from "next/link"

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

import TypewriterComponent from "typewriter-effect";

import { User } from "lucide-react";

import {
  Avatar,
  AvatarFallback,
  AvatarImage,
} from "@/components/ui/avatar"

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"


const font = Montserrat({ weight: '700', subsets: ['latin'] });

const LandingPage = () => {
  return (
    <>
      <nav className="p-4 bg-[#1e1e1e] flex items-center justify-between">
        <Link href="/" className="flex items-center">
          <div className="relative h-8 w-8 mr-4">
            <Image fill alt="Logo" src="/logo.png" />
          </div>
        </Link>
        <div className="flex items-center gap-x-2 ">
          <Link href="">
            <Button variant="link" className="text-white">
              Customer Stories
            </Button>
          </Link>
          <Link href="">
            <Button variant="link" className="text-white">
              Features
            </Button>
          </Link>
          <Link href="">
            <Button variant="link" className="text-white">
              Pricing
            </Button>
          </Link>
          <Link href="">
            <Button variant="link" size="icon" className="text-white">
              <User className="h-4 w-4" />
            </Button>
          </Link>
        </div>

      </nav>

      <div className="bg-[#1e1e1e] text-white font-bold py-36 text-center space-y-5">
        <div className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl space-y-5 font-extrabold">
          <h1>Unlock Creativity with AI-Powered</h1>
          <div className="text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-yellow-400">
            <TypewriterComponent
              options={{
                strings: [
                  "Short Generation.",
                  "Description Generation.",
                  "Thumbnail Generation.",
                  "Soundtrack Generation.",
                  "Auto Uploading."
                ],
                autoStart: true,
                loop: true,
              }}
            />
          </div>
        </div>
        <div className="text-sm md:text-xl font-light text-zinc-400">
          Create content 10x faster with CrumbAI.
        </div>
        <div>
          <Link href="">
            <Button variant="crumbai" className="md:text-lg p-4 md:p-6 rounded-full font-semibold">
              Start Free Trial
            </Button>
          </Link>
        </div>
      </div>

    </>
  )
}

export default LandingPage;