// Sahifa yuklanishi bilanoq, saqlangan tema (yoki tizim tanlovi) qo'llaniladi.
// Bu <script> teg <head> ichida, CSS'dan OLDIN chaqirilishi kerak -- aks holda
// sahifa bir lahza noto'g'ri rangda "yaltirab" ko'rinadi (FOUC deb ataladi).
(function () {
    const saved = localStorage.getItem("theme");
    const theme = saved || "light";
    document.documentElement.setAttribute("data-theme", theme);
})();

function toggleTheme() {
    const current = document.documentElement.getAttribute("data-theme");
    const next = current === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
    updateToggleIcon(next);
}

function updateToggleIcon(theme) {
    const btn = document.getElementById("themeToggle");
    if (btn) btn.textContent = theme === "dark" ? "☀️" : "🌙";
}

document.addEventListener("DOMContentLoaded", () => {
    const current = document.documentElement.getAttribute("data-theme");
    updateToggleIcon(current);
});