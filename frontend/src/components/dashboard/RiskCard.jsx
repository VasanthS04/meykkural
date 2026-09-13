export default function RiskCard({
  risk = 0
}) {

  const level =
    risk >= 70
      ? "HIGH"
      : risk >= 30
        ? "MEDIUM"
        : "LOW";


  return (

    <div className="card risk-card">

      <div className="card-title">

        <span>
          AUTHENTICITY RISK
        </span>

        <span
          className={
            `badge ${
              level === "HIGH"
                ? "danger"
                : level === "MEDIUM"
                  ? "warning"
                  : "safe"
            }`
          }
        >

          {level}

        </span>

      </div>


      <div className="risk-center">

        <div
          className="risk-ring"
          style={{
            "--p":
              `${risk * 3.6}deg`
          }}
        >

          <div>

            <strong>
              {Math.round(risk)}
            </strong>

            <small>
              /100
            </small>

            <label>
              RISK SCORE
            </label>

          </div>

        </div>

      </div>

    </div>

  );

}