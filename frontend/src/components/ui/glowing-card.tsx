import { cn } from "@/lib/utils";
import React from "react";

interface GlowingCardProps {
  label: string;
  value: React.ReactNode;
  subtitle?: React.ReactNode;
  icon?: React.ReactNode;
  valueColor?: string;
  className?: string;
  children?: React.ReactNode;
}

export function GlowingCard({
  label,
  value,
  subtitle,
  icon,
  valueColor = "text-teal-400",
  className,
  children,
}: GlowingCardProps) {
  return (
    <div className={cn("outer relative group rounded-xl p-[1px] overflow-hidden glass-liquid glass-liquid-hover shadow-xl", className)}>
      {/* Internal Card Body */}
      <div className="card relative z-10 rounded-xl bg-slate-950/40 backdrop-blur-xl p-4 flex flex-col justify-between h-full overflow-hidden">
        {/* Soft Background Ray Glow */}
        <div className="ray pointer-events-none opacity-20 group-hover:opacity-40 transition-opacity" />

        {/* Card Header */}
        <div className="flex items-center justify-between text-slate-400 text-xs font-medium relative z-20">
          <span>{label}</span>
          {icon && <div className="p-1 rounded-md bg-slate-900 border border-slate-800">{icon}</div>}
        </div>

        {/* Main Value Readout */}
        <div className="mt-2.5 relative z-20">
          <div className={cn("font-mono text-2xl font-bold tracking-tight", valueColor)}>
            {value}
          </div>
          {subtitle && (
            <div className="text-[11px] text-slate-400 mt-1 font-sans truncate">
              {subtitle}
            </div>
          )}
        </div>

        {children}

        {/* Corner Accent Lines */}
        <div className="line topl pointer-events-none" />
        <div className="line leftl pointer-events-none" />
        <div className="line bottoml pointer-events-none" />
        <div className="line rightl pointer-events-none" />
      </div>
    </div>
  );
}

export default GlowingCard;
