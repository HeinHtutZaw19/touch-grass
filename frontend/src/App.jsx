import Footer from "./components/layout/Footer";
import Navbar from "./components/layout/navbar";
import Wrapper from "./components/layout/wrapper";
import Features from "./sections/Features";
import Hero from "./sections/Hero";
import Hobbies from "./sections/Hobbies";
import Callout from "./sections/callout";
import Explore from "./sections/explore";

const App = () => {
  return (
    <>
      <Navbar />
      <Hero />
      <Explore />
      <Features />
      <Callout />
      <Hobbies />
      <Footer />
    </>
  );
};

export default App;
