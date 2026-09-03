import { NextResponse } from "next/server";
import type { ApiResponse } from "./schema";

export function jsonOk<T>(data: T, status = 200) {
  const body: ApiResponse<T> = { data, error: null };
  return NextResponse.json(body, { status });
}

export function jsonError(
  status: number,
  code: string,
  message: string,
  details?: unknown,
) {
  const body: ApiResponse<null> = {
    data: null,
    error: { code, message, details },
  };
  return NextResponse.json(body, { status });
}
