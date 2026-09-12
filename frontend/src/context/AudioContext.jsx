import {
  createContext,
  useContext
} from "react";


export const AudioAppContext =
  createContext(null);


export function useAudioApp() {

  return useContext(
    AudioAppContext
  );

}