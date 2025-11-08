import Footer from "./Footer";
import Navbar from "./navbar";

const Wrapper = ({ children }) => {
  return (
    <div className="bg-custom-pink">
      <Navbar />
      <main className="relative overflow-hidden">{children}</main>
      <Footer />
    </div>
  );
};

export default Wrapper;
