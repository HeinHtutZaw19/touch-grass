import React from "react";
import Card from "../components/common/Card";
import {
  design,
  development,
  fitness,
  it,
  music,
  photography,
} from "../assets/icons/icons.js";

const Hobbies = () => {
  return (
    <section
      id="hobbies"
      className="bg-custom-purple flex items-center justify-center h-[130vh]"
    >
      <div className="grid grid-cols-3 gap-8">
        {/* Left column (lowered) */}
        <div className="flex flex-col gap-8 translate-y-[6rem]">
          <Card
            bgColor="bg-card-pink"
            imgSrc={design}
            title="Design"
            subtitle="Shape ideas into visuals — from layouts to lifestyles."
          />
          <Card
            bgColor="bg-card-yellow"
            imgSrc={development}
            title="Development"
            subtitle="Build, debug, and bring imagination to life with code."
          />
        </div>

        {/* Middle column (higher) */}
        <div className="flex flex-col gap-8">
          <Card
            bgColor="bg-card-skyblue"
            imgSrc={fitness}
            title="Fitness"
            subtitle="Move with purpose — strength, energy, and discipline."
          />
          <Card
            bgColor="bg-card-lilac"
            imgSrc={it}
            title="Tech & Innovation"
            subtitle="Explore systems, solve problems, and stay curious."
          />
        </div>

        {/* Right column (lowered) */}
        <div className="flex flex-col gap-8 translate-y-[6rem]">
          <Card
            bgColor="bg-card-yellow"
            imgSrc={music}
            title="Music"
            subtitle="Feel the rhythm — where creativity meets emotion."
          />
          <Card
            bgColor="bg-card-pink"
            imgSrc={photography}
            title="Photography"
            subtitle="Capture moments, light, and stories through your lens."
          />
        </div>
      </div>
    </section>
  );
};

export default Hobbies;
