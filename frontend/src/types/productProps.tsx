export type ProductProps = {
  product: {
    category_id: number;
    description: string;
    id: number;
    image: string | null;
    name: string;
    price: number;
    thumbnail: string | null;
  };
};
