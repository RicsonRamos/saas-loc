import { useRef, useState, type PointerEvent } from "react";

import { Button } from "@/components/ui/Button";

interface SignaturePadProps {
  onAssinaturaPronta: (blob: Blob) => void;
  largura?: number;
  altura?: number;
}

export function SignaturePad({ onAssinaturaPronta, largura = 320, altura = 160 }: SignaturePadProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const desenhando = useRef(false);
  const [temTraco, setTemTraco] = useState(false);

  function posicao(event: PointerEvent<HTMLCanvasElement>) {
    const rect = event.currentTarget.getBoundingClientRect();
    return { x: event.clientX - rect.left, y: event.clientY - rect.top };
  }

  function aoPressionar(event: PointerEvent<HTMLCanvasElement>) {
    desenhando.current = true;
    const ctx = canvasRef.current?.getContext("2d");
    if (!ctx) return;
    const { x, y } = posicao(event);
    ctx.beginPath();
    ctx.moveTo(x, y);
  }

  function aoMover(event: PointerEvent<HTMLCanvasElement>) {
    if (!desenhando.current) return;
    const ctx = canvasRef.current?.getContext("2d");
    if (!ctx) return;
    const { x, y } = posicao(event);
    ctx.strokeStyle = "#0f172a";
    ctx.lineWidth = 2;
    ctx.lineCap = "round";
    ctx.lineTo(x, y);
    ctx.stroke();
    setTemTraco(true);
  }

  function aoSoltar() {
    desenhando.current = false;
  }

  function limpar() {
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext("2d");
    if (canvas && ctx) ctx.clearRect(0, 0, canvas.width, canvas.height);
    setTemTraco(false);
  }

  function salvar() {
    canvasRef.current?.toBlob((blob) => {
      if (blob) onAssinaturaPronta(blob);
    }, "image/png");
  }

  return (
    <div>
      <canvas
        ref={canvasRef}
        width={largura}
        height={altura}
        className="touch-none rounded-md border border-slate-300 bg-white"
        onPointerDown={aoPressionar}
        onPointerMove={aoMover}
        onPointerUp={aoSoltar}
        onPointerLeave={aoSoltar}
      />
      <div className="mt-2 flex gap-2">
        <Button type="button" variante="secundaria" onClick={limpar}>
          Limpar
        </Button>
        <Button type="button" onClick={salvar} disabled={!temTraco}>
          Salvar assinatura
        </Button>
      </div>
    </div>
  );
}
