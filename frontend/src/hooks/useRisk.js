import {
  useMemo
} from "react";


export function useRisk(
  risk = 0
) {

  return useMemo(() => {

    if (risk >= 70) {
      return "HIGH";
    }

    if (risk >= 30) {
      return "MEDIUM";
    }

    return "LOW";

  }, [risk]);

}