import React from "react";

const Card = ({ bgColor, imgSrc, title, subtitle }) => {
  return (
    <div
      className={`card ${bgColor} flex flex-col text-center p-8 rounded-2xl shadow-lg`}
    >
      <img
        src={imgSrc}
        alt={title || "icon"}
        className="w-36 h-36 mb-6 object-contain"
      />
      {title && (
        <>
          <h3 className="font-subheading font-semibold text-5xl">{title}</h3>
          {subtitle && (
            <p className="font-subheading text-3xl mt-3">{subtitle}</p>
          )}
        </>
      )}
    </div>
  );
};

export default Card;
