import "./globals.css";
import { Roboto_Slab, Lato } from "next/font/google";
import Footer from "@/components/Footer";
import Header from "@/components/Header";
import { cn } from "@/lib/utils";
import Providers from "@/redux/StoreProvider";

const roboto_slab = Roboto_Slab({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-roboto-slab",
});

const lato = Lato({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-lato",
  weight: "400",
});

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={cn(roboto_slab.variable, lato.variable, "dark")}>
        <Providers>
          <Header />
          <main>{children}</main>
          <Footer />
        </Providers>
      </body>
    </html>
  );
}
