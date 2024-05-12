"use client";

import { createSlice } from "@reduxjs/toolkit";
import { detailProduct, deleteProduct } from "../actions/productActions";

type initialStateType = {
  product: any;
  loading: boolean;
  error: Error | null;
  success: boolean | null;
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
      });
  },
});

export default productDetailSlice.reducer;
