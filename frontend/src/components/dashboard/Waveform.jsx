import { useEffect, useRef } from "react";

export default function Waveform({
  values = []
}) {

  const canvasRef =
    useRef(null);


  useEffect(() => {

    const canvas =
      canvasRef.current;

    if (!canvas) {
      return;
    }


    const ctx =
      canvas.getContext("2d");


    const ratio =
      window.devicePixelRatio || 1;


    canvas.width =
      canvas.clientWidth * ratio;

    canvas.height =
      canvas.clientHeight * ratio;


    ctx.clearRect(
      0,
      0,
      canvas.width,
      canvas.height
    );


    const data =
      values.length
        ? values
        : Array.from(
            { length: 40 },
            (_, i) =>
              Math.sin(i * 0.7) *
              20
          );


    ctx.beginPath();


    data.forEach(
      (value, index) => {

        const x =
          index /
          (data.length - 1 || 1) *
          canvas.width;


        const y =
          canvas.height / 2 +
          value *
          2;


        if (index === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }

      }
    );


    ctx.strokeStyle =
      "#55e6ff";

    ctx.lineWidth =
      2 * ratio;

    ctx.stroke();

  }, [values]);


  return (

    <div className="card waveform-card">

      <div className="card-title">

        <span>
          LIVE AUDIO SIGNATURE
        </span>

        <span className="pulse">
          ●
        </span>

      </div>


      <canvas
        ref={canvasRef}
      />

    </div>

  );

}