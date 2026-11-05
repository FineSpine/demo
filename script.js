const logEl = document.getElementById("cpu-log");
const logStatus = document.getElementById("log-status");
const lastUpdatedEl = document.getElementById("last-updated");
const latestPanel = document.getElementById("latest-panel");
const latestProcess = document.getElementById("latest-process");
const latestPid = document.getElementById("latest-pid");
const latestCpu = document.getElementById("latest-cpu");
const latestSummary = document.getElementById("latest-summary");
const latestInvoker = document.getElementById("latest-invoker");

function renderLog(data) {
  const entries = data.entries ?? [];
  if (!entries.length) {
    logStatus.textContent = "No samples yet. The agent adds one every ~2 minutes.";
    return;
  }

  logStatus.textContent = `${entries.length} sample(s) on record`;
  lastUpdatedEl.textContent = data.lastUpdated ?? entries[entries.length - 1].timestamp;

  const latest = entries[entries.length - 1];
  latestPanel.hidden = false;
  latestProcess.textContent = latest.process;
  latestPid.textContent = String(latest.pid);
  latestCpu.textContent = `${latest.cpuPercent}%`;
  latestInvoker.textContent =
    latest.agentInvokerPid != null ? String(latest.agentInvokerPid) : "—";
  latestSummary.textContent = latest.summary;

  logEl.replaceChildren(
    ...[...entries].reverse().map((entry) => {
      const li = document.createElement("li");
      li.innerHTML = `
        <time>${entry.timestamp}</time>
        <strong>${entry.process}</strong>
        <span class="tag">PID ${entry.pid}</span>
        <span class="tag">${entry.cpuPercent}% CPU</span>
        ${
          entry.agentInvokerPid != null
            ? `<span class="tag">scheduler PID ${entry.agentInvokerPid}</span>`
            : ""
        }
        <p>${entry.summary}</p>
      `;
      return li;
    })
  );
}

async function loadLog() {
  try {
    const res = await fetch(`cpu-log.json?ts=${Date.now()}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    renderLog(await res.json());
  } catch (err) {
    logStatus.textContent = `Could not load cpu-log.json (${err.message}).`;
  }
}

document.getElementById("theme").addEventListener("click", () => {
  document.body.classList.toggle("dark");
});

loadLog();
