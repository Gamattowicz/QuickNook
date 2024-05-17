"use client";

import { createSlice } from "@reduxjs/toolkit";
import { login } from "@/redux/features/user/actions/userActions";

type initialStateType = {
  userInfo: string | null;
  loading: boolean;
  error: Error | null;
  success: boolean | null | string;
};

const initialState: initialStateType = {
  userInfo: localStorage.getItem("jwt"),
  loading: false,
  error: null,
  success: null,
};

const userDetailSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    logout: (state) => {
      localStorage.removeItem("jwt");
      state.userInfo = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state) => {
        state.loading = true;
      })
      .addCase(login.fulfilled, (state, action) => {
        state.loading = false;
        console.log(action.payload);
        state.userInfo = action.payload !== undefined ? action.payload : null;
        state.success = "Login successful!";
      })
      .addCase(login.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as Error;
      });
  },
});

export const { logout } = userDetailSlice.actions;
export default userDetailSlice.reducer;
