import Image from "next/image";
import Link from "next/link";

export default function Home() {
  return (
    <div className="h-3/4 screen flex w-4/5">
      <div className="w-3/5 flex flex-col justify-between p-10 m-4">
        <div className="flex flex-col items-start">
          <span className="text-2xl font-black uppercase italic tracking-wide mb-1">
            Connecting Shoppers
          </span>
          <span className="text-2xl font-black uppercase italic tracking-wide mb-1 self-center">
            &amp;
          </span>
          <span className="text-2xl font-black uppercase italic tracking-wide self-end mr-4">
            Sellers Seamlessly
          </span>
        </div>

        <button className="btn btn-primary btn-xs sm:btn-sm md:btn-md lg:btn-lg font-black py-2 px-4 rounded mx-auto tracking-wide m-4">
          <Link href="/sign-up" className="cursor-pointer">
            Sign up
          </Link>
        </button>

        <div className="text-2xl font-extrabold text-left uppercase italic tracking-wide mb-2">
          Crafting Deals
        </div>

        <div className="text-xl font-semibold text-right flex flex-col items-end m-4">
          <button className="btn btn-accent btn-xs sm:btn-sm md:btn-md lg:btn-lg font-black py-2 px-4 rounded tracking-wide mr-2">
            <Link href="/products" className="cursor-pointer">
              See Products
            </Link>
          </button>
          <div className="text-2xl font-extrabold text-right uppercase italic tracking-wide m-4">
            Delivering Delight
          </div>
        </div>
      </div>
    </div>
  );
}
