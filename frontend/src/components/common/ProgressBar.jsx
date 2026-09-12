export default function ProgressBar({
  value = 0
}) {

  const safeValue =
    Math.max(
      0,
      Math.min(
        100,
        Number(value) || 0
      )
    );


  return (

    <div className="progress">

      <i
        style={{
          width:
            `${safeValue}%`
        }}
      />

    </div>

  );

}