"use client";
import React, { useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import Message from "@/components/Message";

const formSchema = z.object({
  name: z.string(),
});

export default function CategoryForm() {
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState("");

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
  });

  const onSubmit = async (values: z.infer<typeof formSchema>) => {
    try {
      const token = localStorage.getItem("jwt");
      if (!token) {
        throw new Error(
          "You are not authenticated. Please log in and try again."
        );
      }

      const formData = new FormData();
      for (const key in values) {
        formData.append(key, String(values[key as keyof typeof values]));
      }

      const res = await fetch("http://127.0.0.1:8000/category/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(values),
      });
      if (!res.ok) {
        const errorData = await res.json();
        console.error("Server response:", errorData);
        throw new Error(errorData.detail);
      }
      const data = await res.json();
      console.log(data);
      setSuccess("Category created successfully!");
    } catch (error: any) {
      setError(error.message);
      console.error("Error creating category:", error.message);
    }
  };
  return (
    <div className="flex flex-col gap-4 min-h-screen items-center justify-center p-4">
      {error && (
        <Message variant="destructive" title="Error" description={error} />
      )}
      {success && (
        <Message variant="success" title="Success" description={success} />
      )}
      <Card className="w-full max-w-sm">
        <CardHeader className="text-center">
          <CardTitle>Create Category</CardTitle>
          <CardDescription>
            Enter the details below to create a new category
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Form {...form}>
            <form
              onSubmit={form.handleSubmit(onSubmit)}
              className="flex flex-col gap-2"
            >
              <FormField
                control={form.control}
                name="name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Enter Category Name</FormLabel>
                    <FormControl>
                      <Input placeholder="Category name" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <Button type="submit" className="mt-4">
                Create
              </Button>
            </form>
          </Form>
        </CardContent>
        {/* <CardFooter className="justify-between">
          <small>Do you want to create category first?</small>
          <Button asChild variant="outline" size="sm">
            <Link href="/category">Create Category</Link>
          </Button>
        </CardFooter> */}
      </Card>
    </div>
  );
}
