document.addEventListener("DOMContentLoaded", () => {
  const burger = document.getElementById("burger");
  const nav = document.getElementById("site-nav");
  if (!burger || !nav) return;

  burger.addEventListener("click", () => {
    const isOpen = document.body.classList.toggle("nav-open");
    burger.setAttribute("aria-expanded", isOpen ? "true" : "false");
  });
});
