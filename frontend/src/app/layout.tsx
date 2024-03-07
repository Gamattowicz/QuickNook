import type { Metadata } from "next";
import { Roboto_Slab } from "next/font/google";
import "./globals.css";

import Footer from "./components/Footer";
import Header from "./components/Header";

const roboto_slab = Roboto_Slab({
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "E-commerce",
  description: "E-commerce App created by Gamattowicz",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" data-theme="night">
        <body className={roboto_slab.className}>
          <div className="flex flex-col min-h-screen max-h-full">
            <Header />
            <main className="flex-1 grid place-items-center">{children}</main>
            <Footer />
          </div>
        </body>
    </html>
  );
}
