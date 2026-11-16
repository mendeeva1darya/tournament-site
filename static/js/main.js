// Мобильное меню-бургер (адаптив из UI-kit: 768 px и ниже)
document.addEventListener("DOMContentLoaded", function () {
    const burger = document.getElementById("burger");
    const nav = document.getElementById("site-nav");

    if (burger && nav) {
        burger.addEventListener("click", function () {
            const isOpen = nav.classList.toggle("open");
            burger.classList.toggle("open", isOpen);
            burger.setAttribute("aria-expanded", String(isOpen));
            burger.setAttribute(
                "aria-label",
                isOpen ? "Закрыть меню" : "Открыть меню"
            );
        });
    }
});
