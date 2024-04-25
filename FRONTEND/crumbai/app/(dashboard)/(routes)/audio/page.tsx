"use client";

import axios from "axios";
import { useRouter } from "next/navigation";
import * as z from "zod";
import { Heading } from "@/components/heading";
import { Music } from "lucide-react";
import { useForm } from "react-hook-form";
import { formSchema } from "./constants";
import { zodResolver } from "@hookform/resolvers/zod"
import { Form, FormControl, FormField, FormItem } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { ChatCompletionMessageParam } from "openai/resources/chat/completions";
import { Empty } from "@/components/empty";
import { Loader } from "@/components/loader";
import { useProModal } from "@/hooks/use-pro-modal";

const AudioPage = () => {
    const router = useRouter();
    const [music, setMusic] = useState<string>();
    const proModal = useProModal();

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            prompt: ""
        }
    });

    const isLoading = form.formState.isSubmitting;

    const onSubmit = async (values: z.infer<typeof formSchema>) => {
        try {
          setMusic(undefined);

          const response = await axios.post("/api/audio", values);

          setMusic(response.data.audio);
          form.reset();
        } catch (error: any) {
            if (error?.response?.status === 403) {
                proModal.onOpen();
            }
        } finally {
            router.refresh();
        }
    };

    return (
      <div>
        <Heading 
            title="Audio Generation"
            description="Our most advanced audio model"
            icon={Music}
            iconColor="#F3B13F"
            bgColor="bg-violet=500/10"
        />
        <div className="px-4 lg:px-8">
            <div>
                <Form {...form}>
                    <form onSubmit={form.handleSubmit(onSubmit)}
                          className="rounded-lg border-0 bg-[#323232] w-full p-4 px-3 md:px-6 focus-within:shadow-sm grid grid-cols-12 gap-2">
                        <FormField 
                            name="prompt"
                            render={({ field }) => (
                                <FormItem className="col-span-12 lg:col-span-10">
                                    <FormControl className="m-0 p-0">
                                        <Input
                                            className="bg-[#232323] border-0 p-3 focus:outline-none"
                                            disabled={isLoading}
                                            placeholder="Create me a piano elevator music..."
                                            {...field}
                                        />
                                    </FormControl>
                                </FormItem>
                            )}
                        />
                        <Button variant="crumbai" className="col-span-12 lg:col-span-2 w-full" disabled={isLoading}>Generate</Button>
                    </form>
                </Form>
            </div>
            <div className="space-y-4 mt-4">
                {isLoading && (
                    <div className="p-8 rounded-lg w-full flex items-center justify-center bg-[#323232]">
                        <Loader />
                    </div>
                )}
                {!music && !isLoading && (
                  <Empty /> 
                )}
                {music && (
                  <audio controls className="w-full mt-8">
                    <source src={music} />
                  </audio>
                )}
            </div>
        </div>
      </div>
    );
  };
  
  export default AudioPage;