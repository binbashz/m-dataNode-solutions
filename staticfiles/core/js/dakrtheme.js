const toggleDarkMode = () => {
    const body = document.querySelector("body");
    const modeSwitch = document.querySelector(".switch .base");

    // Cambiar al tema oscuro
    if (!body.classList.contains("dark-theme")) {
        body.classList.add("dark-theme");
        modeSwitch.classList.add("dark");
        localStorage.setItem("theme", "dark");
    } else {  // Cambiar al tema claro
        body.classList.remove("dark-theme");
        modeSwitch.classList.remove("dark");
        localStorage.setItem("theme", "light");
    }
}

// Agregar evento de clic al botón de cambio de modo
const modeSwitchButton = document.querySelector(".modo-oscuro .switch");
modeSwitchButton.addEventListener("click", toggleDarkMode);

// Cargar el tema guardado al cargar la página
document.addEventListener("DOMContentLoaded", () => {
    const theme = localStorage.getItem("theme");
    if (theme === "dark") {
        const body = document.querySelector("body");
        const modeSwitch = document.querySelector(".switch .base");
        body.classList.add("dark-theme");
        modeSwitch.classList.add("dark");
    }
});