import axios from "axios";
import { getServerSession } from "next-auth";
import { useSearchParams } from "next/navigation";
import { useRouter } from "next/router";
import { NextResponse } from "next/server";

export async function GET(
    req: any,
  res: {
    status: (arg0: number) => {
      (): any;
      new (): any;
      json: { (arg0: { error: any }): void; new (): any };
    };
  }
) {
  const session = await getServerSession();
  const userEmail = session?.user?.email ?? "";

  if (!userEmail) {
    console.log("Not Authorized");
    return new NextResponse(JSON.stringify({ error: "User not authorized" }), {
      status: 401,
    });
  }

  try {
    const queryString = req.url.split('shorts?')[1]; 
    const searchParams = new URLSearchParams(queryString);
    const youtubeUrl = searchParams.get('youtube_url');
    
    console.log("YouTube URL:", youtubeUrl);
    
    const response = await axios.post(
      "http://161.97.88.202:8000/create",
      {
        user_id: userEmail,
        youtube_url: youtubeUrl,
        settings: [],
      },
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer test",
        },
      }
    );
    return new NextResponse(JSON.stringify(response.data));
  } catch (error) {
    console.error("Error generating shorts:", error);
    return new NextResponse(
      JSON.stringify({ error: "Error generating shorts" }),
      {
        status: 500,
      }
    );
  }
}
