export const CallState =
  Object.freeze({

    IDLE: "idle",

    RINGING: "ringing",

    ACTIVE: "active",

    ENDED: "ended"

  });


export class CallManager {

  constructor({
    onStateChange
  } = {}) {

    this.state =
      CallState.IDLE;

    this.onStateChange =
      onStateChange;

  }


  setState(state) {

    this.state =
      state;

    this.onStateChange?.(
      state
    );

  }


  incoming() {

    this.setState(
      CallState.RINGING
    );

  }


  answer() {

    this.setState(
      CallState.ACTIVE
    );

  }


  end() {

    this.setState(
      CallState.ENDED
    );

  }

}