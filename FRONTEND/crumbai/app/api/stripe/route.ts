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
            try {
                console.log("TESTING 123");
                const stripeSession = await stripe.checkout.sessions.create({
                    success_url: settingsUrl,
                    cancel_url: settingsUrl,
                    payment_method_types: ["card"],
                    mode: "subscription",
                    billing_address_collection: "auto",
                    customer_email: userEmail,
                    line_items: [{
                        price_data: {
                            currency: "USD",
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
                        userEmail,
                    },
                });
                console.log("TESTING 456");


                return new NextResponse(JSON.stringify({ url: stripeSession.url }));
            }  catch (error) {
                console.error("Error creating Stripe session:", error);
                return new NextResponse(JSON.stringify({error: "Failed to create Stripe session"}), {status: 500});
            }
        }
    } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'An unknown error occurred with stripe';
        return new NextResponse(JSON.stringify({error: errorMessage}), {status: 500});
        }
}
