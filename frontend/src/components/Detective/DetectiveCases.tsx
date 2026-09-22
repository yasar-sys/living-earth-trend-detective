import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { api } from "@/services/api";
import type { DetectiveCase } from "@/types";

export default function DetectiveCases() {
  const [cases, setCases] = useState<DetectiveCase[]>([]);
  const [openId, setOpenId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .getDetectiveCases()
      .then(setCases)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <p className="text-slate-muted text-sm">Loading cases…</p>;
  }

  return (
    <div className="max-w-3xl mx-auto px-6 py-16 space-y-6">
      <div className="mb-8">
        <p className="text-caption tracking-widest text-slate-muted uppercase mb-3">
          Detective Cases
        </p>
        <h1 className="font-serif text-heading-lg mb-3">
          Same process. Opposite outcomes. Here's why.
        </h1>
        <p className="text-body-lg text-offwhite-text/75">
          A trend can run one way in one region and the opposite way in another, even when a
          single global process drives both. These are two real paradoxes worth investigating.
        </p>
      </div>

      {cases.map((c) => {
        const open = openId === c.id;
        return (
          <motion.div
            key={c.id}
            layout
            className="bg-space-card border border-space-border rounded-2xl p-6 cursor-pointer"
            onClick={() => setOpenId(open ? null : c.id)}
          >
            <div className="flex items-start justify-between gap-4">
              <h2 className="font-serif text-xl font-semibold">{c.title}</h2>
              <span className="text-slate-muted text-sm shrink-0">{open ? "−" : "+"}</span>
            </div>
            <p className="text-sm text-offwhite-text/75 mt-2">{c.narrative}</p>

            {open && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                className="mt-4 pt-4 border-t border-space-border space-y-3"
              >
                <div>
                  <p className="text-xs uppercase tracking-wide text-slate-muted mb-1">
                    Mechanism
                  </p>
                  <p className="text-sm text-offwhite-text/85">{c.explanation}</p>
                </div>
                <div className="text-xs text-amber-warm">{c.key_mechanism}</div>
                <div className="flex flex-wrap gap-2 pt-2">
                  {c.comparison_years.map((y) => (
                    <span
                      key={y}
                      className="text-xs px-2 py-1 rounded-md bg-space-elevated border border-space-border text-slate-muted"
                    >
                      {y}
                    </span>
                  ))}
                </div>
              </motion.div>
            )}
          </motion.div>
        );
      })}
    </div>
  );
}
