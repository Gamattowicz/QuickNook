import Link from "next/link";
import React from "react";

export default function Logo() {
  const letters = ["Q", "u", "i", "c", "k", "N", "o", "o", "k"];

  return (
    <Link
      href="/"
      className="flex items-center space-x-4 transform transition duration-500 ease-in-out hover:scale-110 hover:text-primary mr-2 md:mr-4"
    >
      <div className="glitch">
        {letters.map((letter, index) => (
          <span
            key={index}
            className={`uppercase text-xs sm:text-md md:text-xl font-morena-bold glitch-span-${
              index + 1
            }`}
          >
            {letter}
          </span>
        ))}
      </div>
    </Link>
  );
}
