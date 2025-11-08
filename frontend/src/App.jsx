import Navbar from "./components/layout/navbar";
import Wrapper from "./components/layout/wrapper";
import Features from "./sections/Features";
import Hero from "./sections/Hero";
import Explore from "./sections/explore";

const App = () => {
  return (
    <>
      <Navbar />
      <Hero />
      <Explore />
      <Features />
    </>
  );
};

export default App;
