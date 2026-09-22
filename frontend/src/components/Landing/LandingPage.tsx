import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import Starfield from "./Starfield";

export default function LandingPage() {
  return (
    <div className="relative min-h-[calc(100vh-64px)] flex items-center justify-center overflow-hidden">
      <Starfield />
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7 }}
        className="relative z-10 max-w-2xl text-center px-6"
      >
        <p className="text-caption tracking-widest text-slate-muted uppercase mb-4">
          NASA Space Apps 2026 &middot; Be An Earth System Trend Detective!
        </p>
        <h1 className="font-serif text-heading-xl mb-6">
          Change is everywhere.
          <br />
          Is it real, or just noise?
        </h1>
        <p className="text-body-lg text-offwhite-text/80 mb-10">
          Explore NASA-measured environmental variables on an interactive 3D globe, and
          uncover cases where the same global process drives opposite trends in different
          regions, with the statistics to prove it.
        </p>
        <div className="flex items-center justify-center gap-4">
          <Link to="/map" className="btn-primary">
            Start Investigating
          </Link>
          <Link to="/detective" className="btn-secondary">
            See Detective Cases
          </Link>
        </div>
      </motion.div>
    </div>
  );
}
