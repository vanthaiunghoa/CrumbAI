import { Button } from "@/components/ui/button";
import { Menu } from "lucide-react";
import Link from "next/link";

const Navbar = () => {
    return (
        <div className="flex items-center p-4">
            <Button variant="ghost" size="icon" className="md:hidden">
                <Menu />
            </Button>
            <div className="flex w-full justify-end">
                <Link href="/api/auth/signout"><Button>Sign Out</Button></Link>
            </div>
        </div>
    )
}

export default Navbar;