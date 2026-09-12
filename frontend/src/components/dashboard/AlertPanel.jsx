export default function AlertPanel({
  risk = 0,
  message = ""
}) {

  const level =
    risk >= 70
      ? "HIGH"
      : risk >= 35
        ? "MEDIUM"
        : "LOW";


  return (

    <div
      className={
        `card alert-panel ${
          level.toLowerCase()
        }`
      }
    >

      <div className="alert-icon">

        ⚠

      </div>


      <div>

        <span className="eyebrow">
          SECURITY STATUS
        </span>

        <h3>

          {
            level === "HIGH"
              ? "Potential voice-cloning attack detected"
              : level === "MEDIUM"
                ? "Suspicious voice characteristics"
                : "Voice currently appears low risk"
          }

        </h3>


        <p>
          {
            message ||
            "மெய்க்குரல் is monitoring the voice stream."
          }
        </p>

      </div>


      <div className="alert-right">

        <b>
          {level}
        </b>

        <small>
          Dynamic risk engine
        </small>

      </div>

    </div>

  );

}