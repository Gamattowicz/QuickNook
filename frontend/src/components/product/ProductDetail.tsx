import { PageProps } from "@/types/pageProps";
import React from "react";

interface ProductDetailProps {
  productId: PageProps["params"]["id"];
}

export default function ProductDetail({ productId }: ProductDetailProps) {
  return <div>ProductDetail: {productId}</div>;
}
