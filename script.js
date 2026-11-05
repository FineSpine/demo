const counter = document.getElementById("counter");
let clicks = 0;
counter.addEventListener("click", () => {
    clicks++;
    counter.textContent = `Clicked ${clicks} time${clicks === 1 ? "" : "s"}`;
});

const themeKey = "demo-theme";
if (localStorage.getItem(themeKey) === "dark") {
    document.body.classList.add("dark");
}
document.getElementById("theme").addEventListener("click", () => {
    const dark = document.body.classList.toggle("dark");
    localStorage.setItem(themeKey, dark ? "dark" : "light");
});

document.getElementById("loaded-at").textContent = new Date().toLocaleString();
