export default function SpeakerCard({
  score = 0
}) {

  return (

    <div className="card speaker-card">

      <div className="card-title">

        <span>
          SPEAKER INTEGRITY
        </span>

      </div>


      <div className="speaker-value">

        <strong>
          {Math.round(score)}%
        </strong>

      </div>


      <div className="progress">

        <i
          style={{
            width:
              `${score}%`
          }}
        />

      </div>


      <div className="model-tag">

        ECAPA-TDNN

      </div>

    </div>

  );

}