import React from "react";
import Link from "next/link";
import ProductList from "@/app/products/ProductList";
import { Button } from "@/components/ui/button";

export default function page() {
  return (
    <div className="flex flex-col items-center justify-center">
      <Button asChild variant="accent" size="lg" className="mt-4">
        <Link href="/products/create">Create Product</Link>
      </Button>
      <ProductList />
    </div>
  );
}
