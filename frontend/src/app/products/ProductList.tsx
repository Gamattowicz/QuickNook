"use client";
import React, { useState, useEffect } from "react";
import Message from "@/components/Message";
import Product from "@/components/Product";
import { ProductProps } from "@/types/productProps";

export default function ProductList() {
  const [products, setProducts] = useState([]);
  const [error, setError] = useState(null);

  async function fetchProduct() {
    try {
      let endpoint = `http://127.0.0.1:8000/product/product`;
      const res = await fetch(endpoint);
      if (!res.ok) {
        const errorData = await res.json();
        console.error("Server response:", errorData);
        throw new Error(errorData.detail);
      }
      const data = await res.json();
      setProducts(data.results);
      console.log(data);
    } catch (error: any) {
      setError(error.message);
      console.error("Error fetching products:", error.message);
    }
  }
  async function fetchProduct2() {
    try {
      let endpoint = `http://127.0.0.1:8000/product/product`;
      const res = await fetch(endpoint);
      const data = await res.json();
      setProducts(data.results);
      console.log(data);
    } catch (error: any) {
      console.error("Error fetching products:", error.message);
    }
  }
  useEffect(() => {
    fetchProduct();
    console.log("ProductList rendered");
  }, []);

  return (
    <div className="flex flex-col gap-4 min-h-screen items-center justify-center p-4">
      {error && (
        <Message variant="destructive" title="Error" description={error} />
      )}
      <div className="flex flex-wrap">
        {products && products.length <= 0 && (
          <p className="font-bold text-center text-primary text-2xl">
            No product
          </p>
        )}
        {/* {products[0] && (
        <Product
          key={(products[0] as ProductProps["product"]).id}
          product={products[0] as ProductProps["product"]}
        />
      )} */}
        {products &&
          products.map((product: ProductProps["product"]) => (
            <div
              className="w-full sm:w-1/2 md:w-1/3 lg:w-1/4 xl:w-1/5 p-1"
              key={product.id}
            >
              <Product key={product.id} product={product} />
            </div>
          ))}
      </div>
    </div>
  );
}
