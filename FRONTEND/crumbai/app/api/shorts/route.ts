import axios from "axios";
import { getServerSession } from "next-auth";
import { useSearchParams } from "next/navigation";
import { useRouter } from "next/router";
import { NextResponse } from "next/server";
import { increaseApiLimit, checkApiLimit }  from "@/lib/api-limit";

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

  const freeTrial = await checkApiLimit();

  if (!freeTrial) {
      return new NextResponse("You have exceeded the free trial limit", { status: 403 });
  }

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
    const faceDetection = searchParams.get('face_detection');
    const subtitles = searchParams.get('subtitles');
    const halfGameplay = searchParams.get('half_gameplay');
    var enabledGameplay = "true";
    
    if (halfGameplay == "none") {
      enabledGameplay = "false";
    }
    
    const response = await axios.post(
      "http://194.163.180.166:8000/create",
      {
        user_id: userEmail,
        youtube_url: youtubeUrl,
        settings: {
          face_detection: faceDetection,
          subtitles: subtitles,
          gameplay: {
            enabled: enabledGameplay,
            type: halfGameplay
          }
        },
      },
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer test",
        },
      }
    );

    await increaseApiLimit();

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
