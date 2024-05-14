"use client";

import { createSlice } from "@reduxjs/toolkit";
import {
  detailProduct,
  deleteProduct,
  createProduct,
  updateProduct,
} from "../actions/productActions";

type initialStateType = {
  product: any;
  loading: boolean;
  error: Error | null;
  success: boolean | null | string;
};

const initialState: initialStateType = {
  product: null,
  loading: false,
  error: null,
  success: null,
};

const productDetailSlice = createSlice({
  name: "product",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(detailProduct.pending, (state) => {
        state.loading = true;
        state.product = null;
        state.error = null;
        state.success = null;
      })
      .addCase(detailProduct.fulfilled, (state, action) => {
        state.loading = false;
        state.product = action.payload;
        state.success = true;
      })
      .addCase(detailProduct.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as Error;
      })
      .addCase(deleteProduct.pending, (state) => {
        state.loading = true;
        state.product = null;
        state.error = null;
        state.success = null;
      })
      .addCase(deleteProduct.fulfilled, (state) => {
        state.loading = false;
        state.product = null;
        state.success = true;
      })
      .addCase(deleteProduct.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as Error;
      })
      .addCase(createProduct.pending, (state) => {
        state.loading = true;
        state.product = null;
      })
      .addCase(createProduct.fulfilled, (state, action) => {
        state.loading = false;
        state.product = action.payload;
        state.success = "Product created successfully!";
      })
      .addCase(createProduct.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as Error;
      })
      .addCase(updateProduct.pending, (state) => {
        state.loading = true;
        state.product = null;
      })
      .addCase(updateProduct.fulfilled, (state, action) => {
        state.loading = false;
        state.product = action.payload;
        state.success = "Product updated successfully!";
      })
      .addCase(updateProduct.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as Error;
      });
  },
});

export default productDetailSlice.reducer;
