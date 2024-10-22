import Stripe from "stripe"
import { headers } from "next/headers"
import { NextResponse } from "next/server"
import { prisma } from "@/lib/prisma"
import { stripe } from "@/lib/stripe"
import { SubresourceIntegrityPlugin } from "next/dist/build/webpack/plugins/subresource-integrity-plugin"

export async function POST(req: Request) {
    const body = await req.text();
    const signature = headers().get("Stripe-Signature") as string;

    let event: Stripe.Event;

    try {
        event = stripe.webhooks.constructEvent(
            body,
            signature,
            process.env.STRIPE_WEBHOOK_SECRET!
        )
    } catch (error: any) {
        return new NextResponse(`Webhook Error: $(error.message)` , { status:400 });
    }

    const session = event.data.object as Stripe.Checkout.Session;

    // Handle the checkout.session.completed event
    if (event.type === "checkout.session.completed") {
        const subscription = await stripe.subscriptions.retrieve(
            session.subscription as string
        );

        if (!session?.metadata?.userEmail) {
            return new NextResponse("User Email not found", { status:400 } )
        }

        // Create a new userSubscription record in the database
        await prisma.userSubscription.create({
            data: {
                userEmail: session?.metadata?.userEmail,
                stripeSubscriptionId: subscription.id,
                stripeCustomerId: subscription.customer as string,
                stripePriceId: subscription.items.data[0].price.id,
                stripeCurrentPeriodEnd: new Date(
                    subscription.current_period_end * 1000
                ),
            },
        });
    }

    if (event.type === "invoice.payment_succeeded") {
        const subscription = await stripe.subscriptions.retrieve(
            session.subscription as string
        );

        // Update the userSubscription record with the new subscription details
        await prisma.userSubscription.update({
            where: {
              stripeSubscriptionId: subscription.id  
            },
            data: {
                stripePriceId: subscription.items.data[0].price.id,
                stripeCurrentPeriodEnd: new Date(
                    subscription.current_period_end * 1000
                ),
            },
        });
    }

    return new NextResponse(null, { status:200 })
}