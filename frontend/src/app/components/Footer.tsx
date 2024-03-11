import Link from "next/link";
import React from "react";
import {
  LinkedInLogoIcon,
  GitHubLogoIcon,
  EnvelopeClosedIcon,
} from "@radix-ui/react-icons";

export default function Footer() {
  return (
    <footer className="w-full footer items-center p-6 bg-secondary text-neutral-content mt-4 bottom-0 flex justify-between">
      <aside className="items-center grid-flow-col">
        <p>© 2024 Copyright | Designed by Przemysław Romańczuk</p>
      </aside>
      <nav className="grid-flow-col gap-4 md:place-self-center md:justify-self-end">
        <div className="flex space-x-4">
          <Link
            href="https://linkedin.com/in/przemysław-romańczuk"
            className="transform transition-all ease-in-out duration-1000 hover:scale-125 hover:text-primary hover:scale-x-[-1]"
          >
            <LinkedInLogoIcon className="h-[1rem] w-[1rem] sm:h-[1.2rem] sm:w-[1.2rem]" />
          </Link>
          <Link
            href="https://github.com/Gamattowicz"
            className="transform transition-all ease-in-out duration-1000 hover:scale-125 hover:text-primary hover:scale-x-[-1]"
          >
            <GitHubLogoIcon className="sh-[1rem] w-[1rem] sm:h-[1.2rem] sm:w-[1.2rem]" />
          </Link>
          <Link
            href="mailto: p.romanczuk31@gmail.com"
            className="transform transition-all ease-in-out duration-1000 hover:scale-125 hover:text-primary hover:scale-x-[-1]"
          >
            <EnvelopeClosedIcon className="sh-[1rem] w-[1rem] sm:h-[1.2rem] sm:w-[1.2rem]" />
          </Link>
        </div>
      </nav>
    </footer>
  );
}
