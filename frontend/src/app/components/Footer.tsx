import Link from "next/link";
import React from "react";
import { FaLinkedin, FaGithub, FaEnvelope } from "react-icons/fa";

export default function Footer() {
  return (
    <React.Fragment>
      <footer className="w-full footer items-center p-6 bg-neutral text-neutral-content mt-4">
        <aside className="items-center grid-flow-col">
          <p>© 2024 Copyright | Designed by Przemysław Romańczuk</p>
        </aside>
        <nav className="grid-flow-col gap-4 md:place-self-center md:justify-self-end">
          <div className="flex space-x-4 ml-32">
            <Link
              href="https://linkedin.com/in/przemysław-romańczuk"
              className="transform transition-all ease-in-out duration-1000 hover:scale-125 hover:text-primary hover:scale-x-[-1]"
            >
              <FaLinkedin className="h-4 w-4" />
            </Link>
            <Link
              href="https://github.com/Gamattowicz"
              className="transform transition-all ease-in-out duration-1000 hover:scale-125 hover:text-primary hover:scale-x-[-1]"
            >
              <FaGithub className="h-4 w-4" />
            </Link>
            <Link
              href="mailto: p.romanczuk31@gmail.com"
              className="transform transition-all ease-in-out duration-1000 hover:scale-125 hover:text-primary hover:scale-x-[-1]"
            >
              <FaEnvelope className="h-4 w-4" />
            </Link>
          </div>
        </nav>
      </footer>
    </React.Fragment>
  );
}
