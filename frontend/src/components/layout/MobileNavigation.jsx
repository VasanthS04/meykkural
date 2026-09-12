export default function MobileNavigation({
  navigation,
  activePage,
  onNavigate
}) {

  return (

    <div className="mobile-navigation">

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

    </div>

  );

}