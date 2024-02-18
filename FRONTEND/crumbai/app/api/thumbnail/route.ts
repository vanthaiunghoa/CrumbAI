import { NextResponse } from "next/server";
import { OpenAI } from "openai";
import { increaseApiLimit, checkApiLimit }  from "@/lib/api-limit";

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
});

export async function POST(req: Request) {
    try {
        const body = await req.json();
        const { prompt, amount = 1, resolution="256x256" } = body;

        if (!openai.apiKey) {
            return new NextResponse("OpenAI API Key not configured", { status: 500 });
        }

        if (!prompt) {
            return new NextResponse("Prompts are required", { status: 400 });
        }

        const freeTrial = await checkApiLimit();
        if (!freeTrial) {
            return new NextResponse("You have exceeded the free trial limit", { status: 403 });
        }

        const response = await openai.images.generate({
            model: "dall-e-2",
            prompt,
            size: resolution,
            n: parseInt(amount),
        });

        await increaseApiLimit();

        return NextResponse.json(response.data);
    } catch (error) {
        console.log("Thumbnail Error", error);
        return new NextResponse("Internal Error", { status: 500 });
    }
}
