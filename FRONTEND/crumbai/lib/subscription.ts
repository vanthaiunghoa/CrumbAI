import { prisma } from "@/lib/prisma"
import { getServerSession } from 'next-auth';

const DAY_IN_MS = 86_400_400;

export const checkSubscription = async () => {
    const session = await getServerSession();
    const userEmail = session?.user?.email;

    if (!userEmail) {
        return false;
    }

    const userSubscription = await prisma.userSubscription.findUnique
    ({
        where: {
            userEmail: userEmail
        },
        select: {
            stripeSubscriptionId: true,
            stripeCurrentPeriodEnd: true,
            stripeCustomerId: true,
            stripePriceId: true,
        },
    });

    if (!userSubscription) {
        return false;
    }

    const isValid = userSubscription.stripePriceId && userSubscription.stripeCurrentPeriodEnd?.getTime()! + DAY_IN_MS > Date.now();

    return !!isValid; // !! makes sure its a boolean
}