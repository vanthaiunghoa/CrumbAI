import { NextResponse } from "next/server";
import { prisma } from '@/lib/prisma';
import { stripe } from "@/lib/stripe";
import { absoluteUrl } from "@/lib/utils";
import { getServerSession } from 'next-auth';

const settingsUrl = absoluteUrl("/settings");

export async function GET() {
    try {
        const session = await getServerSession();
        const userEmail = session?.user?.email ?? '';

        if (!userEmail) {
            console.log("Not Authorized");
            return new NextResponse(JSON.stringify({error: "User not authorized"}), {status: 401});
        }

        const userSubscription = await prisma.userSubscription.findUnique({
            where: {
                userEmail: userEmail
            }
        });

        if (userSubscription && userSubscription.stripeCustomerId) {
            const stripeSession = await stripe.billingPortal.sessions.create({
                customer: userSubscription.stripeCustomerId,
                return_url: settingsUrl
            });

            return new NextResponse(JSON.stringify({ url: stripeSession.url }));
        } else {
            const stripeSession = await stripe.checkout.sessions.create({
                success_url: settingsUrl,
                cancel_url: settingsUrl,
                payment_method_types: ["card"],
                mode: "subscription",
                billing_address_collection: "auto",
                customer_email: userEmail,
                line_items: [{
                    price_data: {
                        currency: "EUR",
                        product_data: {
                            name: "CrumbAI Unlimited",
                            description: "Unlimited Generations",
                        },
                        unit_amount: 2000,
                        recurring: {
                            interval: "month"
                        }
                    },
                    quantity: 1,
                }],
                metadata: {
                    userEmail: userEmail
                },
            });

            return new NextResponse(JSON.stringify({ url: stripeSession.url }));
        }
    } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'An unknown error occurred with stripe';
        return new NextResponse(JSON.stringify({error: errorMessage}), {status: 500});
        }
}
