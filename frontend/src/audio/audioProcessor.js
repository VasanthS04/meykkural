export function pcm16ToFloat32(
  buffer
) {

  const pcm =
    new Int16Array(
      buffer
    );


  const output =
    new Float32Array(
      pcm.length
    );


  for (
    let i = 0;
    i < pcm.length;
    i++
  ) {

    output[i] =
      pcm[i] / 32768;

  }


  return output;

}


export function calculateRMS(
  samples
) {

  if (
    !samples ||
    samples.length === 0
  ) {

    return 0;

  }


  let sum = 0;


  for (
    const sample of samples
  ) {

    sum +=
      sample * sample;

  }


  return Math.sqrt(
    sum / samples.length
  );

}