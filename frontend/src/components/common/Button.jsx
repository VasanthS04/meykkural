export default function Button({
  children,
  className = "",
  ...props
}) {

  return (

    <button
      className={`primary-btn ${className}`}
      {...props}
    >

      {children}

    </button>

  );

}