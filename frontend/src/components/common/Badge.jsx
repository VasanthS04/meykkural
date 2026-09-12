export default function Badge({
  children,
  type = "safe"
}) {

  return (

    <span
      className={`badge ${type}`}
    >

      {children}

    </span>

  );

}