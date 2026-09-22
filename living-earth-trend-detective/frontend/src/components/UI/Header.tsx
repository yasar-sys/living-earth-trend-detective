import { NavLink } from "react-router-dom";

const linkClass = ({ isActive }: { isActive: boolean }) =>
  `text-sm font-medium transition-colors ${
    isActive ? "text-violet-primary" : "text-offwhite-text/70 hover:text-offwhite-text"
  }`;

export default function Header() {
  return (
    <header className="sticky top-0 z-40 flex items-center justify-between px-6 py-4 bg-space-base/80 backdrop-blur-md border-b border-space-border">
      <NavLink to="/" className="font-serif text-lg font-bold">
        Living Earth
      </NavLink>
      <nav className="flex items-center gap-6">
        <NavLink to="/map" className={linkClass}>
          Globe
        </NavLink>
        <NavLink to="/detective" className={linkClass}>
          Detective Cases
        </NavLink>
      </nav>
    </header>
  );
}
