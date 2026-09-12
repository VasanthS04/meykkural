let audioContext = null;

let processor = null;

let source = null;

let activeStream = null;


function startAudioStream(
  mediaStream,
  onAudio,
  onLevel,
  onSampleRate
) {
  audioContext = new (
    window.AudioContext ||
    window.webkitAudioContext
  )();

  return audioContext.resume().then(() => {
    onSampleRate?.(audioContext.sampleRate);
    source = audioContext.createMediaStreamSource(mediaStream);
    const analyser = audioContext.createAnalyser();
    analyser.fftSize = 128;
    const frequencyData = new Uint8Array(analyser.frequencyBinCount);
    source.connect(analyser);

    const updateLevel = () => {
      if (!audioContext || audioContext.state === "closed") {
        return;
      }
      analyser.getByteFrequencyData(frequencyData);
      const average = frequencyData.reduce((sum, value) => sum + value, 0) /
        frequencyData.length;
      onLevel?.({
        level: average / 255,
        frequencies: Array.from(frequencyData)
      });
      window.requestAnimationFrame(updateLevel);
    };
    updateLevel();
    processor = audioContext.createScriptProcessor(4096, 1, 1);

    processor.onaudioprocess = event => {
      const input = event.inputBuffer.getChannelData(0);
      const pcm = new Int16Array(input.length);

      for (let index = 0; index < input.length; index += 1) {
        const sample = Math.max(-1, Math.min(1, input[index]));
        pcm[index] = sample < 0 ? sample * 32768 : sample * 32767;
      }

      onAudio(pcm.buffer);
    };

    source.connect(processor);
    processor.connect(audioContext.destination);
  });
}


export async function startMicrophone(
  onAudio,
  onLevel,
  onSampleRate
) {

  if (
    !navigator.mediaDevices ||
    !navigator.mediaDevices.getUserMedia
  ) {

    throw new Error(
      "Browser does not support microphone access"
    );

  }


  const stream = await navigator.mediaDevices.getUserMedia({

      audio: {

        echoCancellation: true,

        noiseSuppression: true,

        autoGainControl: true

      }

    });


  activeStream = stream;

  await startAudioStream(stream, onAudio, onLevel, onSampleRate);

  stream.getTracks().forEach(track => {
    track.addEventListener("ended", stopMicrophone, { once: true });
  });

  return stream;
}


export async function startVoipAudio(
  mediaStream,
  onAudio,
  onLevel,
  onSampleRate
) {
  if (!mediaStream) {
    throw new Error("VoIP audio stream is unavailable");
  }

  return startAudioStream(mediaStream, onAudio, onLevel, onSampleRate);
}


export function stopMicrophone() {

  if (processor) {

    processor.disconnect();

    processor.onaudioprocess =
      null;

  }


  if (source) {

    source.disconnect();

  }

  if (activeStream) {
    activeStream.getTracks().forEach(track => track.stop());
  }


  if (audioContext) {

    audioContext.close();

  }


  processor = null;

  source = null;

  activeStream = null;

  audioContext = null;

}