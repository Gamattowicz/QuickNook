"use client";
import React, { useState, useEffect } from "react";
import { createProduct } from "@/redux/features/product/actions/productActions";
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
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import Link from "next/link";
import Message from "@/components/Message";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useAppDispatch, useAppSelector } from "@/redux/hooks";

const MAX_FILE_SIZE = 5 * 1024 * 1024;
const ACCEPTED_IMAGE_MIME_TYPES = ["image/jpeg", "image/jpg", "image/png"];

export const formSchema = z
  .object({
    name: z.string(),
    description: z.string(),
    price: z.coerce
      .number({ invalid_type_error: "Price must be a decimal number" })
      .min(0.1, { message: "Price must be 0.1 or higher" }),
    category_id: z.coerce
      .number({ invalid_type_error: "Category ID must be an integer number" })
      .int()
      .min(1, { message: "Category ID must be at least 1" }),
    image: z
      .any()
      .refine((files) => {
        return files?.[0]?.size <= MAX_FILE_SIZE;
      }, `Max image size is 5MB.`)
      .refine(
        (files) => ACCEPTED_IMAGE_MIME_TYPES.includes(files?.[0]?.type),
        "Only .jpg, .jpeg and .png formats are supported."
      )
      .optional(),
  })
  .refine(
    (data) => {
      const decimalPart = data.price.toString().split(".")[1];
      return !decimalPart || decimalPart.length <= 2;
    },
    { message: "Price can have at most 2 decimal places", path: ["price"] }
  );

export default function ProductForm() {
  const [categories, setCategories] = useState<{ name: string; id: number }[]>(
    []
  );
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const dispatch = useAppDispatch();
  const productDetail = useAppSelector((state: any) => state.productDetail);
  const { loading, error, success } = productDetail;

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
  });

  async function fetchCategories() {
    try {
      const res = await fetch("http://127.0.0.1:8000/category/category");
      const categoryData = await res.json();
      setCategories(categoryData.results);
    } catch (error) {
      console.error("Error fetching products:", error);
    }
  }

  const onSubmit = async (values: z.infer<typeof formSchema>) => {
    try {
      await dispatch(createProduct(values)).unwrap();
    } catch (error: any) {
      console.error("Error creating product:", error.message);
    }
  };

  useEffect(() => {
    fetchCategories();
  }, []);

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
          <CardTitle>Create Product</CardTitle>
          <CardDescription>Create New Product</CardDescription>
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
                    <FormLabel>Product Name</FormLabel>
                    <FormControl>
                      <Input placeholder="Product name" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="description"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Product Description</FormLabel>
                    <FormControl>
                      <Input placeholder="Product description" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="price"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Product Price</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="Product Price"
                        type="number"
                        step={0.01}
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="category_id"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Category</FormLabel>
                    <FormControl>
                      <Select onValueChange={field.onChange}>
                        <SelectTrigger>
                          <SelectValue placeholder="Select category" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectGroup>
                            <SelectLabel>Categories</SelectLabel>
                            {categories.map((category) => (
                              <SelectItem
                                key={category.id}
                                value={String(category.id)}
                              >
                                {category.name}
                              </SelectItem>
                            ))}
                          </SelectGroup>
                        </SelectContent>
                      </Select>
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="image"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Product Image</FormLabel>
                    <FormControl>
                      <Input
                        type="file"
                        onChange={(e) => {
                          field.onChange(e.target.files);
                          setSelectedImage(e.target.files?.[0] || null);
                        }}
                        ref={field.ref}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <Button type="submit">Create</Button>
            </form>
          </Form>
        </CardContent>
        <CardFooter className="justify-between">
          <small>Do you want to create category first?</small>
          <Button asChild variant="outline" size="sm">
            <Link href="/category">Create Category</Link>
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
}
