"use client";

import axios from "axios";
import { useRouter } from "next/navigation";
import * as z from "zod";
import { Heading } from "@/components/heading";
import { Download, ImageDown } from "lucide-react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod"
import { Form, FormControl, FormField, FormItem } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Card, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Image from "next/image";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";
import { useState } from "react";
import { Empty } from "@/components/empty";
import { Loader } from "@/components/loader";
import { cn } from "@/lib/utils";
import { amountOptions, formSchema, resolutionOptions } from "./constants";
import { useProModal } from "@/hooks/use-pro-modal";

const ThumbnailPage = () => {
  const router = useRouter();
  const [images, setImages] = useState<string[]>([]);
  const proModal = useProModal();

  const form = useForm<z.infer<typeof formSchema>>({
      resolver: zodResolver(formSchema),
      defaultValues: {
          prompt: "",
          amount: "1",
          resolution: "1024x1792"
      }
  });

  const isLoading = form.formState.isSubmitting;

  const onSubmit = async (values: z.infer<typeof formSchema>) => {
      try {
        setImages([]);

        const response = await axios.post("/api/thumbnail", values);

        const urls = response.data.map((image: { url: string }) => image.url);

        setImages(urls);

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
            title="Thumbnail Generation"
            description="Our advanced image generator, turn your idea into a reality."
            icon={ImageDown}
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
                                <FormItem className="col-span-12 lg:col-span-6">
                                    <FormControl className="m-0 p-0">
                                        <Input
                                            className="bg-[#232323] border-0 p-3 focus:outline-none"
                                            disabled={isLoading}
                                            placeholder="Create me a thumbnail for my video about..."
                                            {...field}
                                        />
                                    </FormControl>
                                </FormItem>
                            )}
                        />
                        <FormField
                          control={form.control}
                          name="amount"
                          render={({ field }) => (
                            <FormItem className="col-span-12 lg:col-span-2">
                              <Select disabled={isLoading} onValueChange={field.onChange} value={field.value} defaultValue={field.value}>
                                <FormControl>
                                  <SelectTrigger className="bg-[#232323] border-0 p-3 focus:outline-none">
                                    <SelectValue defaultValue={field.value} />
                                  </SelectTrigger>
                                </FormControl>
                                <SelectContent>
                                  {amountOptions.map((option) => (
                                    <SelectItem key={option.value} value={option.value}>
                                        {option.label}
                                    </SelectItem>  
                                  ))}
                                </SelectContent>
                              </Select>
                            </FormItem>
                          )}
                        />
                        <FormField
                          control={form.control}
                          name="resolution"
                          render={({ field }) => (
                            <FormItem className="col-span-12 lg:col-span-2">
                              <Select disabled={isLoading} onValueChange={field.onChange} value={field.value} defaultValue={field.value}>
                                <FormControl>
                                  <SelectTrigger className="bg-[#232323] border-0 p-3 focus:outline-none">
                                    <SelectValue defaultValue={field.value} />
                                  </SelectTrigger>
                                </FormControl>
                                <SelectContent>
                                  {resolutionOptions.map((option) => (
                                    <SelectItem key={option.value} value={option.value}>
                                        {option.label}
                                    </SelectItem>  
                                  ))}
                                </SelectContent>
                              </Select>
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
                {images.length === 0 && !isLoading && (
                  <Empty /> 
                )}
                <div className="grid grid-cols-1 md:grid-cold-2 lg:grid-cold-3 xl:grid-cols-4 gap-4 mt-8">
                    {images.map((src) => (
                        <Card key={src} className="rounded-lg overflow-hidden">
                          <div className="relative aspect-square">
                            <Image alt="Image" fill src={src} />
                          </div>
                          <CardFooter className="p-2">
                            <Button onClick={() => window.open(src)} variant="secondary" className="w-full">
                              <Download className="h-4 w-4 mr-2" />
                              Download
                            </Button>
                          </CardFooter>
                        </Card>
                    ))}
                </div>
            </div>
        </div>
      </div>
    );
  };
  
  export default ThumbnailPage;