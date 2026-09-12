const getWebSocketUrl = () => {
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  return `${protocol}//${window.location.host}/ws/audio`;
};

export function connectAnalysisSocket({
  onOpen,
  onMessage,
  onError,
  onClose,
  sampleRate = 16000,
  source = "browser"
  } = {}) {
  const socket = new WebSocket(getWebSocketUrl());

  socket.binaryType = "arraybuffer";

  socket.onopen = () => {
    console.log("Meykkural WebSocket connected");

    socket.send(
      JSON.stringify({
        type: "start_analysis",
        source,
        sample_rate: sampleRate
      })
    );

    if (onOpen) {
      onOpen(socket);
    }
  };

  socket.onmessage = (event) => {
    try {
      if (typeof event.data === "string") {
        const data = JSON.parse(event.data);

        if (onMessage) {
          onMessage(data);
        }
      }
    } catch (error) {
      console.error("Invalid WebSocket message:", error);
    }
  };

  socket.onerror = (error) => {
    console.error("Meykkural WebSocket error:", error);

    if (onError) {
      onError(error);
    }
  };

  socket.onclose = (event) => {
    console.log("Meykkural WebSocket disconnected");

    if (onClose) {
      onClose(event);
    }
  };

  return socket;
}

export function sendAudioChunk(socket, audioData) {
  if (!socket) {
    return false;
  }

  if (socket.readyState !== WebSocket.OPEN) {
    return false;
  }

  socket.send(audioData);
  return true;
}

export function closeAnalysisSocket(socket) {
  if (!socket) {
    return;
  }

  if (
    socket.readyState === WebSocket.OPEN ||
    socket.readyState === WebSocket.CONNECTING
  ) {
    socket.close();
  }
}