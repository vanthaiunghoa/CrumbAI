import NextAuth from "next-auth"

declare module "next-auth" {
  interface User {
    id: int;
  }

  interface Session {
    user: User;
  }
}
