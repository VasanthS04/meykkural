import {
  useCallback,
  useState
} from "react";

import {
  startMicrophone,
  stopMicrophone
} from "../audio/microphone";


export function useMicrophone(
  sendAudio
) {

  const [
    active,
    setActive
  ] = useState(false);


  const start =
    useCallback(
      async () => {

        await startMicrophone(
          sendAudio
        );

        setActive(true);

      },
      [sendAudio]
    );


  const stop =
    useCallback(() => {

      stopMicrophone();

      setActive(false);

    }, []);


  return {

    active,

    start,

    stop

  };

}