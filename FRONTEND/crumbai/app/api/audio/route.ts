import { NextResponse } from "next/server";
import Replicate from "replicate";
import { increaseApiLimit, checkApiLimit }  from "@/lib/api-limit";

const replicate = new Replicate({
    auth: process.env.REPLICATE_API_TOKEN
});

export async function POST(req: Request) {
    try {
        const body = await req.json();
        const { prompt } = body;

        // Check if prompt is provided
        if (!prompt) {
            return new NextResponse("Prompt are required", { status: 400 });
        }

        // Check if user has exceeded the free trial limit
        const freeTrial = await checkApiLimit();
        if (!freeTrial) {
            return new NextResponse("You have exceeded the free trial limit", { status: 403 });
        }

        // Call the Replicate API
        const response = await replicate.run(
            "riffusion/riffusion:8cf61ea6c56afd61d8f5b9ffd14d7c216c0a93844ce2d82ac1c9ecc9c7f24e05",
            {
            input: {
                prompt_a: prompt
            }
            }
        );

        // Increase the API limit
        await increaseApiLimit();

        return NextResponse.json(response);
    } catch (error) {
        console.log("Audio Error", error);
        return new NextResponse("Internal Error", { status: 500 });
    }
}
