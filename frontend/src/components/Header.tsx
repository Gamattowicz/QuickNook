"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import Logo from "@/components/Logo";
import { LinkedInLogoIcon, GitHubLogoIcon } from "@radix-ui/react-icons";
import { ThemeToggle } from "@/components/ui/theme-toggle";
import "../app/fonts.css";

export default function Header() {
  const [isScrolling, setIsScrolling] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolling(window.scrollY > 0);
    };

    window.addEventListener("scroll", handleScroll);

    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);
  return (
    <header
      className={`w-full p-2 sm:p-5 sm:px-10 flex items-center justify-between ${
        isScrolling ? "scrolling" : ""
      }`}
    >
      <Logo />
      <nav className="space-x-1 sm:space-x-4">
        <Link
          href="/"
          className="hover-underline text-xs sm:text-md md:text-2xl font-anders"
        >
          Home
        </Link>
        <Link
          href="/products"
          className="hover-underline text-xs sm:text-md md:text-2xl font-anders"
        >
          Products
        </Link>
        <Link
          href="/orders"
          className="hover-underline text-xs sm:text-md md:text-2xl font-anders"
        >
          Orders
        </Link>
        <Link
          href="/sign-up"
          className="hover-underline text-xs sm:text-md md:text-2xl font-anders"
        >
          Sign Up
        </Link>
        <Link
          href="/login"
          className="hover-underline text-xs sm:text-md md:text-2xl font-anders"
        >
          Login
        </Link>
      </nav>
      <div className="flex items-center justify-center align-center space-x-2 sm:space-x-4">
        <div className="flex items-center justify-center align-center space-x-2 sm:space-x-4">
          <Link
            href="https://linkedin.com/in/przemysław-romańczuk"
            target="_blank"
            rel="noopener noreferrer"
            className="transform transition-all duration-500 hover:scale-125 hover:text-primary"
          >
            <LinkedInLogoIcon className="h-[1rem] w-[1rem] sm:h-[1.2rem] sm:w-[1.2rem]" />
          </Link>
          <Link
            href="https://github.com/Gamattowicz"
            target="_blank"
            rel="noopener noreferrer"
            className="transform transition-all ease-in-out duration-500 hover:scale-125 hover:text-primary"
          >
            <GitHubLogoIcon className="sh-[1rem] w-[1rem] sm:h-[1.2rem] sm:w-[1.2rem]" />
          </Link>
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}
