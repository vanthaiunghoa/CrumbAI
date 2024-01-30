import { getSession } from "next-auth/react";
import { getServerSession } from 'next-auth';

import { prisma } from '@/lib/prisma';
import { MAX_FREE_COUNTS } from '@/constants';

export const increaseApiLimit = async () => {
    const session = await getServerSession();
    console.log("Test: ", session);
    if (session) {
        const userEmail = session?.user?.email;
        console.log("Test: ", userEmail);

        const userApiLimit = await prisma.userApiLimit.findUnique({
            where: {
                userEmail: userEmail!
            }
        });

        if (userApiLimit) {
            await prisma.userApiLimit.update({
                where: {
                    userEmail: userEmail!
                },
                data: {
                    count: userApiLimit.count + 1
                }
            });
        } else {
            await prisma.userApiLimit.create({
                data: {
                    userEmail: userEmail!,
                    count: 1
                }
            });
        }
    }
};

export const checkApiLimit = async () => {
    const session = await getServerSession();
    console.log("Test: ", session);
    if (session) {
        const userEmail = session?.user?.email;
        console.log("Test: ", userEmail);

        const userApiLimit = await prisma.userApiLimit.findUnique({
            where: {
                userEmail: userEmail!
            }
        });

        if (!userApiLimit || userApiLimit.count < MAX_FREE_COUNTS) {
            return true;
        } else {
            return false;
        }
    }
}