import type { NextAuthOptions } from 'next-auth'
import GitHubProvider from 'next-auth/providers/github'
import CredentialsProvider from 'next-auth/providers/credentials'
import { prisma } from '@/lib/prisma'

export const options: NextAuthOptions = {
    providers: [
        GitHubProvider({
            clientId: process.env.GITHUB_ID as string,
            clientSecret: process.env.GITHUB_SECRET as string
        }),
        CredentialsProvider({
            name: "CrumbAI",
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

                const user = { id: "42", email: "hamizarif17@gmail.com", password: "nextauth"}

                if (credentials?.email === user.email && credentials?.password === user.password) {
                    return user
                } else {
                    return null
                }
            }
        })
    ],
}