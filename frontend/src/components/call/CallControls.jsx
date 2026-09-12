export default function CallControls({
  active,
  onStart,
  onStop
}) {

  return (

    <div className="hero-actions">

      {!active ? (

        <button
          className="primary-btn"
          onClick={onStart}
        >

          Start Protected Call

        </button>

      ) : (

        <button
          className="danger-btn"
          onClick={onStop}
        >

          End Protection

        </button>

      )}

    </div>

  );

}