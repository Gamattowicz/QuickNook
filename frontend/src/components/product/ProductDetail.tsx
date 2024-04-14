"use client";
import React, { useState, useEffect } from "react";
import Message from "@/components/Message";
import { PageProps } from "@/types/pageProps";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  CardFooter,
} from "@/components/ui/card";
import { ProductType } from "@/types/productProps";
import { Badge, badgeVariants } from "@/components/ui/badge";
import Image from "next/image";
import Link from "next/link";

interface ProductDetailProps {
  productId: PageProps["params"]["id"];
}

function filePathToUrl(filePath: string) {
  const fileName = filePath.split("\\").pop();
  return `http://127.0.0.1:8000/images/${fileName}`;
}

export default function ProductDetail({ productId }: ProductDetailProps) {
  const [product, setProduct] = useState<ProductType | null>(null);
  const [error, setError] = useState(null);

  async function fetchProduct() {
    try {
      let endpoint = `http://127.0.0.1:8000/product/${productId}`;
      const res = await fetch(endpoint);
      if (!res.ok) {
        const errorData = await res.json();
        console.error("Server response:", errorData);
        throw new Error(errorData.detail);
      }
      const data = await res.json();
      setProduct(data);
      console.log(data);
    } catch (error: any) {
      setError(error.message);
      console.error("Error fetching products:", error.message);
    }
  }

  useEffect(() => {
    fetchProduct();
    console.log("ProductDetail fetched");
    console.log(product);
  }, []);

  return (
    <div className="flex flex-col gap-4 min-h-screen items-center justify-center p-4">
      {error && (
        <Message variant="destructive" title="Error" description={error} />
      )}
      <Card className="w-full max-w-sm shadow-lg shadow-primary">
        <CardHeader className="text-center">
          {product && <CardTitle>{product.name}dw</CardTitle>}
          <CardDescription></CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col items-center justify-center">
          {product?.image ? (
            <Image
              src={filePathToUrl(product.image)}
              alt={product.name}
              width={1500}
              height={1500}
              sizes="75vw, 33vw"
              style={{ height: "auto", width: "auto", maxHeight: "33vh" }}
              className="self-center"
            />
          ) : (
            <div className="flex items-center justify-center w-32 h-32 text-sm">
              <p>No image available</p>
            </div>
          )}
          <CardDescription>{product?.description}</CardDescription>
        </CardContent>
        <CardFooter className="flex items-center justify-center">
          <CardContent className="flex justify-between mt-4 w-full">
            <Link
              href={`/${product?.category_name}`}
              className={badgeVariants({ variant: "muted" })}
            >
              {product?.category_name}
            </Link>

            <Badge variant="outline">{product?.price}PLN</Badge>
          </CardContent>
        </CardFooter>
      </Card>
    </div>
  );
}
