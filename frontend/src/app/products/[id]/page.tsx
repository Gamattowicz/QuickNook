import React from "react";
import ProductDetail from "@/components/product/ProductDetail";
import { PageProps } from "@/types/pageProps";

export default function page({ params }: PageProps) {
  console.log(params.id);
  return <ProductDetail productId={params.id} />;
}
