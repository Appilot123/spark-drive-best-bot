async function json(url){ return (await fetch(url)).json(); }

document.getElementById("upload").onclick = async () => {
  const file = document.getElementById("csv").files[0];
  if(!file) return alert("Pick a CSV first");
  const fd = new FormData(); fd.append("file", file);
  await fetch("/import/csv", { method: "POST", body: fd });
  await refresh();
};

document.getElementById("route").onclick = async () => {
  const pickup = document.getElementById("pickup").value.trim();
  const dropoffs = document.getElementById("dropoffs").value.trim();
  const res = await json(`/route?pickup=${encodeURIComponent(pickup)}&dropoffs=${encodeURIComponent(dropoffs)}`);
  const a = document.getElementById("maps"); a.href = res.maps_url; a.textContent = res.maps_url;
};

async function refresh(){
  const s = await json("/stats");
  document.getElementById("stats").innerHTML = `
    <h3>Stats</h3>
    <p>Deliveries: <strong>${s.deliveries}</strong></p>
    <p>Hours: ${s.hours.toFixed(2)} | Miles: ${s.miles.toFixed(1)}</p>
    <p>Earnings: $${s.earnings_usd.toFixed(2)} (Tips $${s.tips_usd.toFixed(2)})</p>
    <p>$ / hour: $${s.per_hour.toFixed(2)} | $ / mile: $${s.per_mile.toFixed(2)}</p>
  `;

  const adv = await json("/advice");
  const hoursUl = document.getElementById("best-hours");
  hoursUl.innerHTML = (adv.by_hour.slice(0,5) || []).map(([h,v]) => `<li>${h}:00 — $${v.toFixed(2)}/hr</li>`).join("");
  const daysUl = document.getElementById("best-days");
  const names = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"];
  daysUl.innerHTML = (adv.by_weekday.slice(0,5) || []).map(([d,v]) => `<li>${names[d]} — $${v.toFixed(2)}/hr</li>`).join("");

  const tbody = document.querySelector("#tbl tbody");
  const rows = await json("/deliveries?limit=50");
  tbody.innerHTML = rows.map(r => `
    <tr>
      <td>${new Date(r.ts).toLocaleString()}</td>
      <td>${r.zone}</td>
      <td>${r.order_type}</td>
      <td>${r.miles.toFixed(1)}</td>
      <td>${r.duration_min.toFixed(0)}</td>
      <td>$${(r.payout_usd).toFixed(2)}</td>
      <td>$${(r.tips_usd).toFixed(2)}</td>
    </tr>
  `).join("");
}

refresh();
