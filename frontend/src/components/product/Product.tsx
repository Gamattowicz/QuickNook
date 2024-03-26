import React from "react";
import Link from "next/link";

import { ProductProps } from "@/types/productProps";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge, badgeVariants } from "@/components/ui/badge";
import { ShoppingCart } from "lucide-react";
import Image from "next/image";

function filePathToUrl(filePath: string) {
  const fileName = filePath.split("\\").pop();
  return `http://127.0.0.1:8000/thumbnails/${fileName}`;
}

export default function Product({ product }: ProductProps) {
  return (
    <Card>
      <CardHeader className="text-center">
        <CardTitle>{product.name}</CardTitle>
        <CardDescription>{product.description}</CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col items-center justify-center">
        {product.thumbnail ? (
          <Image
            src={filePathToUrl(product.thumbnail)}
            alt={product.name}
            width={128}
            height={128}
            priority
            className="self-center"
          />
        ) : (
          <div className="flex items-center justify-center w-32 h-32 text-sm">
            <p>No image available</p>
          </div>
        )}
        <div className="flex justify-between mt-4 w-full">
          <Link
            href={`/${product.category_name}`}
            className={badgeVariants({ variant: "muted" })}
          >
            {product.category_name}
          </Link>
          <Badge variant="outline">{product.price}PLN</Badge>
        </div>
      </CardContent>
      <CardFooter className="flex items-center justify-center">
        <Button asChild variant="default" size="lg">
          <Link href="/login">
            BUY <ShoppingCart className="ml-5 h-5 w-5" />
          </Link>
        </Button>
      </CardFooter>
    </Card>
  );
}
