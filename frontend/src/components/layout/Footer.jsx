import React from "react";
import { Logo } from "@/assets/icons/icons"; // adjust path if needed

const Footer = () => {
  return (
    <footer className="bg-[#0d0b42] text-white py-12 px-6 flex flex-col items-center justify-center gap-6">
      {/* Brand logo */}
      <div className="flex items-center gap-2">
        <Logo className="w-7 h-7 text-white" />
        <p className="text-[20px] font-bold">
          <span className="text-custom-purple">Touch</span>Grass
        </p>
      </div>

      {/* Contact info */}
      <section
        id="contact"
        className="flex flex-col items-center text-gray-300 mt-2 font-subheading"
      >
        <p>📞 +82 10-1234-5678</p>
        <p>✉️ hello@touchgrass.com</p>
      </section>

      {/* Divider line */}
      <div className="w-[90vw] h-[1px] bg-gray-700 mt-6" />

      {/* Copyright */}
      <p className="text-gray-400 text-sm font-subheading text-center mt-3">
        © {new Date().getFullYear()} TouchGrass. All rights reserved.
      </p>
    </footer>
  );
};

export default Footer;
