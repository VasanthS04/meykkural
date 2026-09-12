import {
  useState
} from "react";


export function useVoIP() {

  const [
    callActive,
    setCallActive
  ] = useState(false);


  const start = () => {

    setCallActive(true);

  };


  const end = () => {

    setCallActive(false);

  };


  return {

    callActive,

    start,

    end

  };

}