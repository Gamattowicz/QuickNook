import { configureStore } from "@reduxjs/toolkit";

import productListReducer from "./features/product/slices/productListSlice";
import productDetailSlice from "./features/product/slices/productDetailSlice";

export const store = configureStore({
  reducer: {
    productsList: productListReducer,
    productDetail: productDetailSlice,
  },
});

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>;
// Inferred type: {posts: PostsState, comments: CommentsState, users: UsersState}
export type AppDispatch = typeof store.dispatch;
