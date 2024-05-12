"use client";

import { createAsyncThunk } from "@reduxjs/toolkit";
import { ProductType } from "@/types/productProps";

export const listProducts = createAsyncThunk(
  "products/list",
  async (_, { rejectWithValue }) => {
    try {
      const res = await fetch(
        "http://127.0.0.1:8000/product/product?page=1&per_page=10"
      );
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail);
      }
      const data = await res.json();
      return data;
    } catch (error) {
      return rejectWithValue((error as Error).message);
    }
  }
);

export const detailProduct = createAsyncThunk<ProductType, number>(
  "products/detail",
  async (productId, { rejectWithValue }) => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/product/${productId}/`, {
        method: "GET",
        headers: {
          Accept: "application/json",
        },
      });
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail);
      }
      const data: ProductType = await res.json();
      return data;
    } catch (error) {
      return rejectWithValue((error as Error).message);
    }
  }
);

export const deleteProduct = createAsyncThunk<
  void,
  { productId: number; onProductDelete: () => void }
>(
  "product/delete",
  async ({ productId, onProductDelete }, { rejectWithValue }) => {
    try {
      const token = localStorage.getItem("jwt");
      if (!token) {
        throw new Error(
          "You are not authenticated. Please log in and try again."
        );
      }

      const res = await fetch(`http://127.0.0.1:8000/product/${productId}/`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!res.ok) {
        const errorData = await res.json();
        console.error("Server response:", errorData);
        throw new Error(errorData.detail);
      }
      onProductDelete();
    } catch (error) {
      console.error("Error fetching products:", (error as Error).message);
      return rejectWithValue((error as Error).message);
    }
  }
);
