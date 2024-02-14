import Link from 'next/link';
import { Form as LoginForm } from './form';

export default function LoginPage() {
  return (
    <div className="h-screen w-screen flex justify-center items-center bg-[#323232]">
      <div className="sm:shadow-xl px-8 pb-8 pt-12 sm:bg-[#1E1E1E] text-white rounded-xl space-y-12">
        <h1 className="text-2xl text-center font-semibold order-2">Log In</h1>
        {/* <div className="bg-[#F3B13F] h-3 w-full order-1"></div> */}
        <LoginForm />
        <p className="text-center">
          Need to create an account?{' '}
          <Link className="text-indigo-500 hover:underline" href="/register">
            Create Account
          </Link>{' '}
        </p>
      </div>
    </div>
  );
}
