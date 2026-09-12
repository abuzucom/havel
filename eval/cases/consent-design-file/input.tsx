export function ConsentBanner() {
  return (
    <div className="banner">
      <label><input type="checkbox" defaultChecked /> Analytics</label>
      <label><input type="checkbox" defaultChecked /> Marketing</label>
      <button className="primary" onClick={acceptAll}>Accept all</button>
      <a className="tiny-link" href="/cookie-settings">Manage</a>
    </div>
  );
}
