import React from "react";

const Callout = () => {
  return (
    <section
      id="callout"
      className="w-full h-[95vh] flex justify-center items-center"
    >
      <div className="w-[40vw] flex flex-col justify-center items-center gap-10">
        <h2 className="heading2">
          Take the <span className="text-accent-green">next step</span> in
          discovering your child’s passion
        </h2>
        <p className="text-center leading-7">
          Every child’s journey is unique, and every interest has the potential
          to become a lifelong passion. We help your child explore their
          curiosities, experiment with new experiences, and build the confidence
          to follow what excites them most, transforming everyday moments into
          opportunities for growth and self-discovery.
        </p>
      </div>
    </section>
  );
};

export default Callout;
