export function getRiskLevel(
  risk
) {

  if (risk >= 70) {
    return "HIGH";
  }

  if (risk >= 35) {
    return "MEDIUM";
  }

  return "LOW";

}


export function getRiskClass(
  risk
) {

  if (risk >= 70) {
    return "danger";
  }

  if (risk >= 35) {
    return "warning";
  }

  return "safe";

}