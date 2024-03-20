"use client";

import { Montserrat } from "next/font/google";
import Image from "next/image"
import Link from "next/link"

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

import TypewriterComponent from "typewriter-effect";

import { User, LogIn, Heart } from "lucide-react";

import {
  Avatar,
  AvatarFallback,
  AvatarImage,
} from "@/components/ui/avatar"

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { getSession } from "next-auth/react"


const font = Montserrat({ weight: '700', subsets: ['latin'] });

const LandingPage = () => {
  const isLoggedIn = false;

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
          {isLoggedIn ? (
            <Link href="/dashboard">
              <Button variant="link" className="text-white">
                Dashboard
              </Button>
            </Link>
          ) : (
            <Link href="/login">
              <Button variant="link" size="icon" className="text-white">
                <User className="h-4 w-4" />
              </Button>
            </Link>
          )}
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
          <Link href="/dashboard">
            <Button variant="crumbai" className="md:text-lg p-4 md:p-6 rounded-full font-semibold">
              Start Free Trial
            </Button>
          </Link>
        </div>
      </div>
      <div className="bg-[#232323] px-10 pb-20">
        <h2 className="text-center text-4xl text-white font-extrabold mb-10 pt-10">Customer Stories</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          <Card className="bg-[#1e1e1e] border-none text-white">
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <div>
                  <p className="text-lg">Mike</p>
                  <p className="text-zinc-400 text-sm">Podcast Host</p>
                </div>
                <Avatar>
                  <AvatarImage src="https://i1.sndcdn.com/avatars-twM1pq6gSk4YzN4F-N4zKuw-t240x240.jpg" alt="@shadcn" />
                </Avatar>
              </CardTitle>

              <CardContent className="pt-4 px-0">
                Crumbai's AI effortlessly turns my long interviews into captivating shorts, highlighting the best moments. It's boosted my online presence remarkably!              </CardContent>
            </CardHeader>
          </Card>
          <Card className="bg-[#1e1e1e] border-none text-white">
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <div>
                  <p className="text-lg">Emma</p>
                  <p className="text-zinc-400 text-sm">Youtube Tech Reviewer</p>
                </div>
                <Avatar>
                  <AvatarImage src="https://i1.sndcdn.com/avatars-twM1pq6gSk4YzN4F-N4zKuw-t240x240.jpg" alt="@shadcn" />
                </Avatar>
              </CardTitle>
              <CardContent className="pt-4 px-0">
                Crumbai is a lifesaver for creating engaging shorts from my lengthy tech reviews, making my content more accessible and shareable.              </CardContent>
            </CardHeader>
          </Card>
          <Card className="bg-[#1e1e1e] border-none text-white">
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <div>
                  <p className="text-lg">Carlos</p>
                  <p className="text-zinc-400 text-sm">TikTok Influencer</p>
                </div>
                <Avatar>
                  <AvatarImage src="https://i1.sndcdn.com/avatars-twM1pq6gSk4YzN4F-N4zKuw-t240x240.jpg" alt="@shadcn" />
                </Avatar>
              </CardTitle>
              <CardContent className="pt-4 px-0">
                Crumbai transforms my daily vlogs into viral TikTok shorts. It intuitively picks the highlights, skyrocketing my engagement!              </CardContent>
            </CardHeader>
          </Card>
        </div>
      </div>

      <div className="bg-[#1e1e1e] px-10 pb-20">
        <h2 className="text-center text-4xl text-white font-extrabold mb-10 pt-10">Features</h2>
        <div className="grid">
          <Tabs defaultValue="1" className="w-full">
            <TabsList className="flex flex-wrap justify-center gap-y-5 bg-[#1e1e1e] text-white" loop={true}>
              <TabsTrigger value="1" className="mx-2">Subtitle Generation</TabsTrigger>
              <TabsTrigger value="2" className="mx-2">Active Speaker Generation</TabsTrigger>
              <TabsTrigger value="3" className="mx-2">Detect Viral Moments</TabsTrigger>

              <TabsTrigger value="4" className="mx-2">Auto Crop</TabsTrigger>
              <TabsTrigger value="5" className="mx-2">Description/Tags Generation</TabsTrigger>
              <TabsTrigger value="6" className="mx-2">Seamless Uploading</TabsTrigger>
            </TabsList>
            <div className="text-[#F3B13F] text-center mt-8">
              <TabsContent value="1">Instantly transform dialogue into text with our AI-driven subtitles, enhancing accessibility and boosting engagement.</TabsContent>
              <TabsContent value="2">Never miss a beat – our system pinpoints who's speaking, keeping your content sharp and audience tuned in.</TabsContent>
              <TabsContent value="3">Spot potential viral hits with our detecting feature, ready to catapult your content into the spotlight.</TabsContent>
              <TabsContent value="4">Frame your shots to perfection. Our auto-crop adapts to the main action, ensuring your content always looks its best.</TabsContent>
              <TabsContent value="5">Craft compelling descriptions and tags effortlessly, driving discoverability and connecting with your target audience.</TabsContent>
              <TabsContent value="6">Upload your masterpiece with ease. Our seamless integration means your content goes from edit to live in a flash.</TabsContent>
            </div>
          </Tabs>
        </div>
      </div>

      <div className="bg-[#232323] px-10 pb-10">
            <p className="text-white text-center pt-5">Made with ❤️ by Hamiz & Daniel | <span className="text-[#F3B13F]">© CrumbAI 2024</span> </p>
      </div>

    </>
  )
}

export default LandingPage;