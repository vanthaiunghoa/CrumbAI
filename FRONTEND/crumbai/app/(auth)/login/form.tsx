'use client';

import { Alert } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { getProviders, signIn } from 'next-auth/react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useState, useEffect } from 'react';

export const Form = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const callbackUrl = searchParams.get('callbackUrl') || '/dashboard';
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [providers, setProviders] = useState(null);

  useEffect(() => {
    const fetchProviders = async () => {
      const fetchedProviders = await getProviders();
      setProviders(fetchedProviders);
    };

    fetchProviders();
  }, []);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await signIn('credentials', {
        redirect: false,
        email,
        password,
        callbackUrl,
      });
      console.log('Res', res);
      if (!res?.error) {
        router.push("/dashboard"); // removed callbackurl
      } else {
        setError('Invalid email or password');
      }
    } catch (err: any) {}
  };

  return (
    <>
    <form onSubmit={onSubmit} className="space-y-12 w-full sm:w-[400px]">
      <div className="grid w-full items-center gap-1.5">
        <Label htmlFor="email">Email:</Label>
        <Input
          className="w-full bg-[#232323] border-0"
          placeholder="example@gmail.com"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          id="email"
          type="email"
        />
      </div>
      <div className="grid w-full items-center gap-1.5">
        <Label htmlFor="password">Password:</Label>
        <Input
          className="w-full bg-[#232323] border-0"
          placeholder="*********"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          id="password"
          type="password"
        />
      </div>
      {error && <Alert>{error}</Alert>}
      <div className="w-full">
        <Button className="w-full" size="lg" variant={'crumbai'}>
          Sign In
        </Button>
      </div>
    </form>
    <div className="mt-4">
      <p className="text-center">Or sign in with:</p>
      <div className="flex justify-center space-x-4 mt-2">
        {providers &&
          Object.values(providers).map((provider) => (
            <div key={provider.name} style={{ marginBottom: 0 }}>
              <button onClick={() =>  signIn(provider.id, { callbackUrl: '/dashboard' })}>
                {provider.name}
              </button>
            </div>
          ))}
      </div>
    </div>
        </>
  );
};
