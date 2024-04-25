import axios from "axios";
import { getServerSession } from "next-auth";
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

  const queryString = req.url.split('?')[1]; 
  const searchParams = new URLSearchParams(queryString); 
  const unique_id = searchParams.get('unique_id'); 

  try {
    const response = await axios.post(
      "https://api.crumbai.com/delete",
      {
        video_id: unique_id,
        user_id: userEmail,
      },
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer "+process.env.BEARER_TOKEN,
        },
      }
    );
    return new NextResponse(JSON.stringify(response.data));
  } catch (error) {
    console.error("Error fetching videos:", error);
    return new NextResponse(
      JSON.stringify({ error: "Error fetching videos" }),
      {
        status: 500,
      }
    );
  }
}
