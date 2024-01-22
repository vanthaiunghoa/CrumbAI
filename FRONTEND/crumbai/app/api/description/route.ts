import { NextResponse } from "next/server";
import { OpenAI } from "openai";

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
});

export async function POST(req: Request) {
    try {
        const body = await req.json();
        const { messages } = body;

        if (!openai.apiKey) {
            return new NextResponse("OpenAI API Key not configured", { status: 500 });
        }

        if (!messages) {
            return new NextResponse("Messages are required", { status: 400 });
        }

        const descriptionContext = {
            role: 'system',
            content: "You are an AI trained to generate a short appealing description and tags for there video based off the information they give you. It must be a maximum of 50 words."
        };

        const updatedMessages = [descriptionContext, ...messages];

        const response = await openai.chat.completions.create({
            model: "gpt-3.5-turbo",
            messages: updatedMessages
        });

        return NextResponse.json(response.choices[0].message);
    } catch (error) {
        console.log("Description Error", error);
        return new NextResponse("Internal Error", { status: 500 });
    }
}
