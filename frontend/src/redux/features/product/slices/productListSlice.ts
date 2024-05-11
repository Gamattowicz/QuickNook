"use client";

import { createSlice } from "@reduxjs/toolkit";
import { listProducts } from "../actions/productActions";

type initialStateType = {
  productsList: any[];
  loading: boolean;
  error: Error | null;
};

const initialState: initialStateType = {
  productsList: [],
  loading: false,
  error: null,
};

const productListSlice = createSlice({
  name: "productsList",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(listProducts.pending, (state) => {
        state.loading = true;
        state.productsList = [];
      })
      .addCase(listProducts.fulfilled, (state, action) => {
        state.loading = false;
        state.productsList = action.payload;
      })
      .addCase(listProducts.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as Error;
      });
  },
});

export default productListSlice.reducer;
