export function drawWaveform(
  canvas,
  samples = []
) {

  if (!canvas) {
    return;
  }


  const context =
    canvas.getContext("2d");


  const ratio =
    window.devicePixelRatio || 1;


  const width =
    canvas.clientWidth *
    ratio;


  const height =
    canvas.clientHeight *
    ratio;


  canvas.width =
    width;

  canvas.height =
    height;


  context.clearRect(
    0,
    0,
    width,
    height
  );


  if (
    samples.length === 0
  ) {

    return;

  }


  context.beginPath();


  samples.forEach(
    (value, index) => {

      const x =
        index /
        (samples.length - 1 || 1) *
        width;


      const y =
        height / 2 +
        value *
        height *
        0.35;


      if (index === 0) {

        context.moveTo(
          x,
          y
        );

      }

      else {

        context.lineTo(
          x,
          y
        );

      }

    }
  );


  context.strokeStyle =
    "#55e6ff";

  context.lineWidth =
    2 * ratio;

  context.stroke();

}