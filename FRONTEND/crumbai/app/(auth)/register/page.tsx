import Link from 'next/link'
import Image from 'next/image';
import { RegisterForm } from './form'

export default function RegisterPage() {
  return (
    <div className="h-screen w-screen flex flex-col justify-center items-center bg-[#323232]">
      <div className="mb-8">
        <Link href="/" className='flex items-center justify-center'>
            <Image src="/logo.png" alt="Logo" width={50} height={50} />
            <span className="text-white text-lg font-semibold ml-2 pt-4">CrumbAI</span>
        </Link>
      </div>
      <div className="sm:shadow-xl px-8 pb-8 pt-12 sm:bg-[#1E1E1E] text-white rounded-xl space-y-12">
        <h1 className="font-semibold text-2xl text-center">Start your journey today</h1>
        <RegisterForm />
        <p className="text-center">
          Have an account?{' '}
          <Link className="text-indigo-500 hover:underline" href="/login">
            Sign in
          </Link>{' '}
        </p>
      </div>
    </div>
  )
}