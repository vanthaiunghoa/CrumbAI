import type { NextAuthOptions } from 'next-auth'
import GitHubProvider from 'next-auth/providers/github'
import GoogleProvider from "next-auth/providers/google";
import CredentialsProvider from 'next-auth/providers/credentials'
import { prisma } from '@/lib/prisma'
import { compare } from 'bcrypt'

export const options: NextAuthOptions = {
    pages: {
        signIn: '/login'
    },
    session: {
        strategy: 'jwt'
    },
    providers: [
        GitHubProvider({
            clientId: process.env.GITHUB_ID as string,
            clientSecret: process.env.GITHUB_SECRET as string
        }),
        GoogleProvider({
            clientId: process.env.GOOGLE_ID as string,
            clientSecret: process.env.GOOGLE_SECRET as string,
            authorization: {
                params: {
                    prompt: "consent",
                    access_type: "offline",
                    response_type: "code"
                }
            }
        }),
        CredentialsProvider({
            name: "",
            credentials: {
                email: {
                    label: "Email:",
                    type: "email",
                    placeholder: "johndoe@crumbai.com"
                },
                password: {
                    label: "Password:",
                    type: "password",
                    placeholder: "********"
                }
            },
            async authorize(credentials) {
                if (!credentials?.email || !credentials.password) {
                    return null
                }

                const user = await prisma.user.findUnique({
                    where: {
                        email: credentials.email
                    }
                })

                if (!user) {
                    return null
                }

                const isPasswordValid = await compare(
                    credentials.password,
                    user.password
                )

                if (!isPasswordValid) {
                    return null
                }

                return {
                    id: user.id + '',
                    email: user.email,
                    name: user.name,
                    randomKey: 'Hey cool'
                }
            }
        })
    ],
    // callbacks: {
    //     session: ({ session, token }) => {
    //       console.log('Session Callback', { session, token })
    //       return {
    //         ...session,
    //         user: {
    //           ...session.user,
    //           id: token.id,
    //           randomKey: token.randomKey
    //         }
    //       }
    //     },
    //     // session({ session, token }) {
    //     //     session.user.id = token.id

    //     //     return session
    //     // },
    //     jwt: ({ token, user }) => {
    //       console.log('JWT Callback', { token, user })
    //       if (user) {
    //         const u = user as unknown as any
    //         return {
    //           ...token,
    //           id: u.id,
    //           randomKey: u.randomKey
    //         }
    //       }
    //       return token
    //     }
    //     // jwt({ token, account, user }) {
    //     //     if (account) {
    //     //         token.accessToken = account.access_token
    //     //         token.id = user?.id
    //     //     }
    //     //     return token
    //     // }
    // }
    callbacks: {
        async jwt({ token, user }) {
          if (user) {
            token.id = user.id;
          }
          return token;
        },
        async session({ session, token }) {
          session.user.id = token.id;
          return session;
        },
      },
}