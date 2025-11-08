import React from "react";
import { Logo } from "../../assets/icons/icons";

const Navbar = () => {
  return (
    <nav className="fixed top-0 left-0 w-full h-20 bg-custom-pink z-50 flex items-center justify-between px-10 ">
      <div className="flex items-center gap-2">
        <Logo className="w-7 h-7" />
        <p className="text-[20px] font-bold">
          <span className="text-custom-purple">Touch</span>Grass
        </p>
      </div>

      <ul className="hidden md:flex items-center gap-10 text-[20px]">
        <li>
          <a
            href="#explore"
            className="hover:text-custom-purple transition-colors"
          >
            Explore
          </a>
        </li>
        <li>
          <a
            href="#features"
            className="hover:text-custom-purple transition-colors"
          >
            Features
          </a>
        </li>
        <li>
          <a
            href="#contact"
            className="hover:text-custom-purple transition-colors"
          >
            Contact
          </a>
        </li>
      </ul>

      <div className="flex items-center gap-4">
        <button className="text-[20px] hover:underline">Login</button>
        <button className="rounded-full px-5 py-2 bg-black text-white text-[20px] hover:bg-gray-800 transition-colors">
          Join for free
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
