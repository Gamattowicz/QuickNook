"use client";

import { createAsyncThunk } from "@reduxjs/toolkit";
import { z } from "zod";
import { formSchema as formLoginSchema } from "@/components/LoginForm";

type LoginValues = z.infer<typeof formLoginSchema>;

export const login = createAsyncThunk<void, LoginValues>(
  "user/login",
  async (values, { rejectWithValue }) => {
    try {
      const formData = new FormData();
      for (const key in values) {
        formData.append(key, values[key as keyof typeof values]);
      }

      const res = await fetch("http://127.0.0.1:8000/user/token", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(values),
      });
      if (!res.ok) {
        const errorData = await res.json();
        console.error("Server response:", errorData);
        throw new Error(errorData.detail);
      }
      const data = await res.json();
      const token = data.access_token;
      localStorage.setItem("jwt", token);
      console.log(data);
    } catch (error) {
      console.error("Error fetching products:", (error as Error).message);
      return rejectWithValue((error as Error).message);
    }
  }
);
