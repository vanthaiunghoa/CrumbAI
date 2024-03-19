export { default } from "next-auth/middleware"

export const config = { matcher: ["/dashboard", "/clips", "/shorts", "/thumbnails", "/descriptions", "/audio", "/settings"] }