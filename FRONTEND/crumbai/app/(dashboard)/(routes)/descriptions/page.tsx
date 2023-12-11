"use client";

import * as z from "zod";
import { Heading } from "@/components/heading";
import { ScrollText } from "lucide-react";
import { useForm } from "react-hook-form";
import { formSchema } from "./constants";
import { zodResolver } from "@hookform/resolvers/zod"
import { Form, FormControl, FormField, FormItem } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

const DescriptionPage = () => {
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            prompt: ""
        }
    });

    const isLoading = form.formState.isSubmitting;

    const onSubmit = async (values: z.infer<typeof formSchema>) => {
        console.log(values);
    };

    return (
      <div>
        <Heading 
            title="Description"
            description="Our most advanced description model"
            icon={ScrollText}
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
                                            placeholder="Create me a description and tags for my tiktok video about..."
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
                Test

            </div>
        </div>
      </div>
    );
  };
  
  export default DescriptionPage;