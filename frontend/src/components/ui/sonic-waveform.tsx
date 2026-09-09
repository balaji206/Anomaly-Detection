"use client";

import { useEffect, useRef } from "react";

// Optimized Sonic Waveform Canvas Background Component
export const SonicWaveformCanvas = ({ className = "" }: { className?: string }) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d", { alpha: true });
    if (!ctx) return;

    let animationFrameId: number;
    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let time = 0;

    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    const draw = () => {
      const width = canvas.width;
      const height = canvas.height;
      const centerY = height / 2;

      ctx.fillStyle = "rgba(11, 12, 14, 0.25)";
      ctx.fillRect(0, 0, width, height);

      const lineCount = 20;
      const segmentCount = 44;

      for (let i = 0; i < lineCount; i++) {
        ctx.beginPath();
        const progress = i / lineCount;
        const colorIntensity = Math.sin(progress * Math.PI);
        // Linear Indigo & Sky Blue waveform palette
        const alpha = colorIntensity * 0.55 + 0.15;
        ctx.strokeStyle = i % 2 === 0 
          ? `rgba(129, 140, 248, ${alpha})` 
          : `rgba(99, 102, 241, ${alpha * 0.9})`;
        ctx.lineWidth = 1.5;

        for (let j = 0; j <= segmentCount; j++) {
          const x = (j / segmentCount) * width;
          const distToMouse = Math.abs(x - mouseX);
          const mouseEffect = Math.max(0, 1 - distToMouse / 400);

          // Wave calculation
          const noise = Math.sin(j * 0.1 + time + i * 0.12) * 12;
          const spike = Math.cos(j * 0.18 + time + i * 0.08) * Math.sin(j * 0.05 + time) * 28;
          const y = centerY + noise + spike * (1 + mouseEffect * 1.5);

          if (j === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
        }
        ctx.stroke();
      }

      time += 0.012;
      animationFrameId = requestAnimationFrame(draw);
    };

    let ticking = false;
    const handleMouseMove = (event: MouseEvent) => {
      if (!ticking) {
        requestAnimationFrame(() => {
          mouseX = event.clientX;
          mouseY = event.clientY;
          ticking = false;
        });
        ticking = true;
      }
    };

    window.addEventListener("resize", resizeCanvas, { passive: true });
    window.addEventListener("mousemove", handleMouseMove, { passive: true });

    resizeCanvas();
    draw();

    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener("resize", resizeCanvas);
      window.removeEventListener("mousemove", handleMouseMove);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className={`fixed inset-0 z-0 pointer-events-none w-full h-full transform-gpu ${className}`}
      style={{ willChange: "transform" }}
    />
  );
};

export default SonicWaveformCanvas;

