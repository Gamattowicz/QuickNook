"use client";
import React, { useState, useEffect } from "react";
import Message from "@/components/Message";
import PaginationSection from "@/components/PaginationSection";
import Product from "@/components/product/Product";
import { ProductType } from "@/types/productProps";

export default function ProductList() {
  const [products, setProducts] = useState<ProductType[]>([]);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [productOnPage, setProductOnPage] = useState(1);
  const [totalProducts, setTotalProducts] = useState(0);

  async function fetchProduct() {
    try {
      let endpoint = `http://127.0.0.1:8000/product/product?page=${page}&per_page=${productOnPage}`;
      const res = await fetch(endpoint);
      if (!res.ok) {
        const errorData = await res.json();
        console.error("Server response:", errorData);
        throw new Error(errorData.detail);
      }
      const data = await res.json();
      setProducts(data.results);
      setTotalProducts(data.totalItems);
      console.log(data);
    } catch (error: any) {
      setError(error.message);
      console.error("Error fetching products:", error.message);
    }
  }

  const refreshProducts = async (): Promise<void> => {
    fetchProduct();
  };

  const handlePageChange = (pageNumber: number) => {
    setPage(pageNumber);
  };

  useEffect(() => {
    fetchProduct();
    console.log("ProductList rendered");
  }, [page]);

  return (
    <div className="flex flex-col gap-4 min-h-screen items-center justify-center p-4">
      {error && (
        <Message variant="destructive" title="Error" description={error} />
      )}
      <div className="flex flex-wrap justify-center">
        {products && products.length <= 0 && (
          <p className="font-bold text-center text-primary text-2xl">
            No product
          </p>
        )}
        {products &&
          products.map((product: ProductType) => (
            <div className="w-64 m-12 sm:m-2" key={product.id}>
              <Product product={product} onProductDelete={refreshProducts} />
            </div>
          ))}
      </div>
      <PaginationSection
        totalProducts={totalProducts}
        productOnPage={productOnPage}
        currentPage={page}
        setCurrentPage={handlePageChange}
      />
    </div>
  );
}