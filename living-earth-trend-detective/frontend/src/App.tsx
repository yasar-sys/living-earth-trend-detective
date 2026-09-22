import { Route, Routes } from "react-router-dom";
import LandingPage from "@/components/Landing/LandingPage";
import Header from "@/components/UI/Header";
import DetectiveView from "@/pages/DetectiveView";
import GlobeView from "@/pages/GlobeView";

export default function App() {
  return (
    <div className="min-h-screen bg-space-base text-offwhite-text">
      <Header />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/map" element={<GlobeView />} />
        <Route path="/detective" element={<DetectiveView />} />
      </Routes>
    </div>
  );
}
