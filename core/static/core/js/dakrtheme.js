const toggleDarkMode = () => {
    const body = document.querySelector("body");
    const dlIcon = document.getElementById("dl-icon");

    // Cambiar al tema oscuro
    if (!body.classList.contains("dark-theme")) {
        body.classList.add("dark-theme");
        dlIcon.classList.remove("fa-moon");
        dlIcon.classList.add("fa-sun");
    } else {  // Cambiar al tema claro
        body.classList.remove("dark-theme");
        dlIcon.classList.remove("fa-sun");
        dlIcon.classList.add("fa-moon");
    }
}
