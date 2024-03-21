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

export default function Product({ product }: ProductProps) {
  return (
    <Card>
      <CardHeader className="text-center">
        <CardTitle>{product.name}</CardTitle>
        <CardDescription>Sign up for a new account</CardDescription>
      </CardHeader>
      <CardContent className="flex justify-between">
        <Link
          href={`/${product.category_id}`}
          className={badgeVariants({ variant: "muted" })}
        >
          Badge
        </Link>
        <Badge variant="outline">{product.price}PLN</Badge>
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
