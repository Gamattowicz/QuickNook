export type ProductType = {
  category_name: string;
  description: string;
  id: number;
  image: string | null;
  name: string;
  price: number;
  thumbnail: string | null;
};

export interface ProductProps {
  product: ProductType;
  onProductDelete: () => Promise<void>;
}
