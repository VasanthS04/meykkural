export function percent(
  value
) {

  return `${Math.round(
    Number(value) || 0
  )}%`;

}


export function formatScore(
  value
) {

  return Math.round(
    Number(value) || 0
  );

}