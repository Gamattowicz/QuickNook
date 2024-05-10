"use client";
import React, { useState, useEffect } from "react";
import { listProducts } from "@/redux/features/product/actions/productActions";
import { InputFiltering } from "@/components/InputFiltering";
import Message from "@/components/Message";
import PaginationSection from "@/components/PaginationSection";
import SelectSorting from "@/components/SelectSorting";
import Product from "@/components/product/Product";
import { ProductType } from "@/types/productProps";
import { useAppDispatch, useAppSelector } from "@/redux/hooks";

export default function ProductList() {
  const [products, setProducts] = useState<ProductType[]>([]);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [productOnPage, setProductOnPage] = useState(7);
  const [totalProducts, setTotalProducts] = useState(0);
  const [sortOption, setSortOption] = useState("");
  const [sortDirection, setSortDirection] = useState("ascending");
  const [filters, setFilters] = useState({
    name: "",
    price: "",
  });
  const dispatch = useAppDispatch();
  const productList = useAppSelector((state: any) => state.productsList);
  const { productsList, loading } = productList;

  async function fetchProduct() {
    try {
      let endpoint = `http://127.0.0.1:8000/product/product?page=${page}&per_page=${productOnPage}`;
      if (sortOption) {
        const prefix = sortDirection === "descending" ? "-" : "";
        endpoint += `&sort=${prefix}${sortOption}`;
      }
      Object.entries(filters).forEach(([key, value]) => {
        if (value) {
          endpoint += `&${key}=${value}`;
        }
      });
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
    console.log(filters);
  }, [page, sortDirection, sortOption, filters]);

  useEffect(() => {
    dispatch(listProducts());
  }, [dispatch]);

  return (
    <div className="flex flex-col gap-4 min-h-screen items-center justify-center p-4 w-full">
      {error && (
        <Message variant="destructive" title="Error" description={error} />
      )}
      <div className="flex justify-between space-x-4">
        <SelectSorting
          placeholder="Sort by..."
          options={["name", "price"]}
          onValueChange={setSortOption}
        />
        <SelectSorting
          placeholder="Ascending/Descending"
          options={["ascending", "descending"]}
          onValueChange={setSortDirection}
        />
      </div>
      <div className="flex justify-between space-x-4">
        <InputFiltering
          placeholder="Product name"
          value={filters.name}
          filterType="text"
          onChange={(e) =>
            setFilters((prev) => ({ ...prev, name: e.target.value }))
          }
        />
        <InputFiltering
          placeholder="Product price"
          value={filters.price}
          filterType="number"
          onChange={(e) =>
            setFilters((prev) => ({ ...prev, price: e.target.value }))
          }
        />
      </div>
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
