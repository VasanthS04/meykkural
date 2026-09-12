import {
  createPeerConnection
} from "./webrtc";

import {
  startVoipAudio,
  stopMicrophone
} from "../audio/microphone";


export class VoIPManager {

  constructor({
    onCallStart,
    onCallEnd,
    onAudio
  } = {}) {

    this.onCallStart =
      onCallStart;

    this.onCallEnd =
      onCallEnd;

    this.onAudio =
      onAudio;

    this.peerConnection =
      null;

    this.remoteAudioStarted =
      false;

  }


  async create() {

    this.peerConnection =
      createPeerConnection();

    this.remoteAudioStarted =
      false;


    /*
     * When remote VoIP audio
     * arrives, automatically
     * start protection.
     */

    this.peerConnection.ontrack =
      event => {

        console.log(
          "Remote VoIP audio received"
        );


        const stream = event.streams?.[0];
        this.onCallStart?.(event);
        if (
          stream &&
          this.onAudio &&
          !this.remoteAudioStarted
        ) {
          this.remoteAudioStarted =
            true;

          startVoipAudio(stream, this.onAudio).catch(error => {
            this.remoteAudioStarted =
              false;
            console.error("Unable to analyze VoIP audio", error);
          });
        }

      };


    return this.peerConnection;

  }


  end() {

    if (
      this.peerConnection
    ) {

      this.peerConnection.close();

    }


    this.peerConnection =
      null;

    this.remoteAudioStarted =
      false;

    stopMicrophone();


    this.onCallEnd?.();

  }

}