import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({
    status: "ok",
    pipeline: "active",
    timestamp: new Date().toISOString(),
    repo: "KennyGeee123/fullstack-app",
    deploy: "vercel",
  });
}
