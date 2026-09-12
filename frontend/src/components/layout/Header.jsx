export default function Header({
  title,
  connected = false,
  onMenu
}) {

  return (

    <header className="topbar">

      <button
        className="icon-btn mobile-menu"
        onClick={onMenu}
      >
        ☰
      </button>


      <div>

        <span className="eyebrow">
          VOICE SECURITY CENTER
        </span>

        <h1>
          {title}
        </h1>

      </div>


      <span
        className={
          `connection ${
            connected
              ? "online"
              : ""
          }`
        }
      >

        <span />

        {connected
          ? "LIVE"
          : "STANDBY"}

      </span>

    </header>

  );

}