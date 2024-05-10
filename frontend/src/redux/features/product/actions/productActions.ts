"use client";

import { createAsyncThunk } from "@reduxjs/toolkit";

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
