export default function Sidebar({
  navigation = [],
  activePage,
  onNavigate
}) {

  return (

    <aside className="sidebar">

      <nav>

        {navigation.map(
          ([id, label, Icon]) => (

            <button
              key={id}
              className={
                activePage === id
                  ? "active"
                  : ""
              }
              onClick={() =>
                onNavigate(id)
              }
            >

              <Icon size={18} />

              <span>
                {label}
              </span>

            </button>

          )
        )}

      </nav>

    </aside>

  );

}