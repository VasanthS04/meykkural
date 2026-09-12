const models = [

  ["aasist", "AASIST"],

  ["wav2vec2", "wav2vec2"],

  ["rawnet2", "RawNet2"],

  ["conformer", "Conformer"],

  ["xlsr", "XLS-R"],

  ["ecapa", "ECAPA-TDNN"]

];


export default function ModelCards({
  scores = {}
}) {

  return (

    <div className="model-grid">

      {models.map(
        ([key, name]) => {

          const value =
            Number(
              scores[key] || 0
            );


          return (

            <div
              className="model-card"
              key={key}
            >

              <div className="model-info">

                <b>
                  {name}
                </b>

                <small>
                  AI analysis
                </small>

              </div>


              <strong>
                {Math.round(value)}%
              </strong>


              <div className="progress">

                <i
                  style={{
                    width:
                      `${value}%`
                  }}
                />

              </div>

            </div>

          );

        }
      )}

    </div>

  );

}