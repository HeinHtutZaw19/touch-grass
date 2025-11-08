import React from "react";
import hero from "../assets/images/hero.png";

const Hero = () => {
  return (
    <section className="w-full h-[90vh] flex justify-center items-center bg-custom-pink px-10 gap-30">
      <div className="max-w-lg">
        <h1 className="font-display text-9xl leading-tight">
          <span className="text-custom-purple">Learning</span> Without Limits
        </h1>
        <div className="flex gap-4 mt-6">
          <button className="rounded-full px-6 py-3 text-white bg-black hover:bg-gray-800 transition">
            Join for free
          </button>
          <button className="rounded-full px-6 py-3 border-2 border-black hover:bg-black hover:text-white transition">
            Explore
          </button>
        </div>
      </div>

      <div className="w-1/2 flex justify-center">
        <img className="object-contain max-w-full" src={hero} alt="Hero" />
      </div>
    </section>
  );
};

export default Hero;
