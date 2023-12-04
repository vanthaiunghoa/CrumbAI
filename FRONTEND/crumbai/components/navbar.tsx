import { Button } from "@/components/ui/button";
import Link from "next/link";
import MobileSidebar from "@/components/mobile-sidebar";

const Navbar = () => {
    return (
        <div className="flex items-center p-4">
            <MobileSidebar />
            <div className="flex w-full justify-end">
                <Link href="/api/auth/signout"><Button>Sign Out</Button></Link>
            </div>
        </div>
    )
}

export default Navbar;