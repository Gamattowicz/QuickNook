import { configureStore } from "@reduxjs/toolkit";

import productListReducer from "./features/product/slices/productListSlice";
import productDetailSlice from "./features/product/slices/productDetailSlice";
import userDetailReducer from "./features/user/slices/userDetailSlice";

export const store = configureStore({
  reducer: {
    productsList: productListReducer,
    productDetail: productDetailSlice,
    userDetail: userDetailReducer,
  },
});

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>;
// Inferred type: {posts: PostsState, comments: CommentsState, users: UsersState}
export type AppDispatch = typeof store.dispatch;
