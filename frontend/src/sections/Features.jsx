import React from "react";
import rectangle from "../assets/images/rectangle.png";

const Features = () => {
  return (
    <section
      id="features"
      className="w-full h-fit flex flex-col justify-center"
    >
      <div className="w-full flex justify-center items-center">
        <h2 className="text-6xl font-inter font-bold my-25">
          How <span className="text-custom-purple">Touch</span>Grass Works
        </h2>
      </div>
      <div className="flex flex-col items-center gap-15">
        <div className="feature-container">
          <div className="feature-text">
            <h3 className="feature-title">Feature 1</h3>
            <p className="feature-description">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla
              sollicitudin justo a scelerisque efficitur. Sed efficitur orci ac
              nisi euismod sollicitudin.{" "}
            </p>
          </div>
          <img src={rectangle} alt="rectangle" className="w-[40vw]" />
        </div>

        <div className="feature-container">
          <img src={rectangle} alt="rectangle" className="w-[40vw]" />
          <div className="feature-text">
            <h3 className="feature-title">Feature 1</h3>
            <p className="feature-description">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla
              sollicitudin justo a scelerisque efficitur. Sed efficitur orci ac
              nisi euismod sollicitudin.{" "}
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Features;
