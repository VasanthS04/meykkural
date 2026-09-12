const features = [

  ["mfcc", "MFCC"],

  ["mel", "Mel-Spectrogram"],

  ["lfcc", "LFCC"],

  ["cqcc", "CQCC"],

  ["pitch", "Pitch"],

  ["energy", "Energy"],

  ["harmonics", "Harmonics"],

  ["pauses", "Pauses"]

];


export default function FeatureCards({
  data = {}
}) {

  return (

    <div className="feature-grid">

      {features.map(
        ([key, label]) => {

          const value =
            Number(
              data[key] || 0
            );


          return (

            <div
              className="feature"
              key={key}
            >

              <span>
                {label}
              </span>

              <b>
                {Math.round(value)}%
              </b>


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