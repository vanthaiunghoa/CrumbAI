import type { NextAuthOptions } from 'next-auth'
import GitHubProvider from 'next-auth/providers/github'
import CredentialsProvider from 'next-auth/providers/credentials'
import { prisma } from '@/lib/prisma'
import { compare } from 'bcrypt'

export const options: NextAuthOptions = {
    session: {
        strategy: 'jwt'
    },
    providers: [
        GitHubProvider({
            clientId: process.env.GITHUB_ID as string,
            clientSecret: process.env.GITHUB_SECRET as string
        }),
        CredentialsProvider({
            name: "Sign In",
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
                // Need to verify credentials in database
                // https://next-auth.js.org/configuration/providers/credentials

                // const user = { id: "42", email: "hamizarif17@gmail.com", password: "nextauth"}

                // if (credentials?.email === user.email && credentials?.password === user.password) {
                //     return user
                // } else {
                //     return null
                // }

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
    callbacks: {
        session: ({ session, token }) => {
          console.log('Session Callback', { session, token })
          return {
            ...session,
            user: {
              ...session.user,
              id: token.id,
              randomKey: token.randomKey
            }
          }
        },
        jwt: ({ token, user }) => {
          console.log('JWT Callback', { token, user })
          if (user) {
            const u = user as unknown as any
            return {
              ...token,
              id: u.id,
              randomKey: u.randomKey
            }
          }
          return token
        }
      } 
}