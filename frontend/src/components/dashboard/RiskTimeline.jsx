export default function RiskTimeline({
  values = []
}) {

  const data =
    values.length
      ? values
      : Array(20).fill(0);


  return (

    <div className="card timeline">

      <div className="card-title">

        <span>
          RISK TIMELINE
        </span>

        <small>
          LIVE
        </small>

      </div>


      <div className="bars">

        {data.map(
          (value, index) => {

            const className =
              value >= 70
                ? "danger"
                : value >= 30
                  ? "warning"
                  : "";


            return (

              <i
                key={index}
                className={className}
                style={{
                  height:
                    `${Math.max(
                      3,
                      value
                    )}%`
                }}
              />

            );

          }
        )}

      </div>

    </div>

  );

}