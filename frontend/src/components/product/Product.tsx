"use client";
import React from "react";
import Link from "next/link";
import { deleteProduct } from "@/redux/features/product/actions/productActions";

import { ProductProps } from "@/types/productProps";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge, badgeVariants } from "@/components/ui/badge";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { ShoppingCart, Trash2, SquarePenIcon } from "lucide-react";
import Image from "next/image";
import { useAppDispatch, useAppSelector } from "@/redux/hooks";

function filePathToUrl(filePath: string) {
  const fileName = filePath.split("\\").pop();
  return `http://127.0.0.1:8000/thumbnails/${fileName}`;
}

export default function Product({ product, onProductDelete }: ProductProps) {
  const dispatch = useAppDispatch();
  const productDetail = useAppSelector((state: any) => state.productDetail);
  const { loading, error } = productDetail;

  const deleteHandler = async () => {
    dispatch(deleteProduct({ productId: product.id, onProductDelete }));
  };
  return (
    <Card className="shadow-lg shadow-primary">
      <CardHeader className="text-center">
        <CardTitle>
          <Link href={`/products/${product.id}/`}>{product.name}</Link>
        </CardTitle>
        <CardDescription>{product.description}</CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col items-center justify-center">
        {product.thumbnail ? (
          <Image
            src={filePathToUrl(product.thumbnail)}
            alt={product.name}
            width={128}
            height={128}
            priority
            className="self-center"
          />
        ) : (
          <div className="flex items-center justify-center w-32 h-32 text-sm">
            <p>No image available</p>
          </div>
        )}
        <div className="flex justify-between mt-4 w-full">
          <Link
            href={`/${product.category_name}`}
            className={badgeVariants({ variant: "muted" })}
          >
            {product.category_name}
          </Link>
          <Link
            href={`/products/${product.id}/update/`}
            className="link link-hover link-primary text-shadow-lg"
          >
            <Button variant="ghost">
              <SquarePenIcon className="text-success" />
            </Button>
          </Link>
          <AlertDialog>
            <AlertDialogTrigger asChild>
              <Button variant="ghost">
                <Trash2 className="text-destructive" />
              </Button>
            </AlertDialogTrigger>
            <AlertDialogContent>
              <AlertDialogHeader>
                <AlertDialogTitle>Delete Product</AlertDialogTitle>
                <AlertDialogDescription>
                  Are you sure you want to delete the product &quot;
                  {product.name}&quot;? This action cannot be undone.
                </AlertDialogDescription>
              </AlertDialogHeader>
              <AlertDialogFooter>
                <AlertDialogCancel>Cancel</AlertDialogCancel>
                <AlertDialogAction onClick={deleteHandler}>
                  Continue
                </AlertDialogAction>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialog>
          <Badge variant="outline">{product.price}PLN</Badge>
        </div>
      </CardContent>
      <CardFooter className="flex items-center justify-center">
        <Button asChild variant="default" size="lg">
          <Link href="/login">
            BUY <ShoppingCart className="ml-5 h-5 w-5" />
          </Link>
        </Button>
      </CardFooter>
    </Card>
  );
}
