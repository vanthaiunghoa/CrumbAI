import Link from 'next/link';
import Image from 'next/image';
import { Form as LoginForm } from './form';

export default function LoginPage() {
  return (
    <div className="h-screen w-screen flex flex-col justify-center items-center bg-[#323232]">
      <div className="mb-8">
        <Link href="/" className='flex items-center justify-center'>
            <Image src="/logo.png" alt="Logo" width={50} height={50} />
            <span className="text-white text-lg font-semibold ml-2 pt-4">CrumbAI</span>
        </Link>
      </div>
      <div className="sm:shadow-xl px-8 pb-8 pt-12 sm:bg-[#1E1E1E] text-white rounded-xl space-y-12">
        <h1 className="text-2xl text-center font-semibold">Log In</h1>
        <LoginForm />
        <p className="text-center">
          Need to create an account?{' '}
          <Link className="text-indigo-500 hover:underline" href="/register">
            Create Account
          </Link>
        </p>
      </div>
    </div>
  );
}
