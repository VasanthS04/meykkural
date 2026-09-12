export function createPeerConnection(
  config = {}
) {

  return new RTCPeerConnection({

    iceServers:
      config.iceServers ||
      [
        {
          urls:
            "stun:stun.l.google.com:19302"
        }
      ]

  });

}