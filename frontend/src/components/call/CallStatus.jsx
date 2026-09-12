export default function CallStatus({
  active = false
}) {

  return (

    <span
      className={
        `connection ${
          active
            ? "online"
            : ""
        }`
      }
    >

      <span />

      {
        active
          ? "PROTECTED CALL"
          : "NO ACTIVE CALL"
      }

    </span>

  );

}