import {
  useEffect,
  useRef,
  useState
} from "react";


export function useWebSocket(
  url
) {

  const socketRef =
    useRef(null);


  const [
    connected,
    setConnected
  ] = useState(false);


  useEffect(() => {

    if (!url) {
      return;
    }


    const socket =
      new WebSocket(url);


    socketRef.current =
      socket;


    socket.onopen = () => {

      setConnected(true);

    };


    socket.onclose = () => {

      setConnected(false);

    };


    return () => {

      socket.close();

    };

  }, [url]);


  return {

    socket:
      socketRef,

    connected

  };

}