// Archivo JavaScript principal
console.log("TodoDeporte cargado correctamente");

// Alternador de tema - Modo oscuro/claro
(function themeToggle() {
  const body = document.body;
  const toggle = document.querySelector(".theme-toggle");
  const icon = toggle?.querySelector(".theme-icon use");

  // Cargar tema guardado
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {
    body.classList.add("dark-mode");
    icon?.setAttribute(
      "href",
      icon.getAttribute("href").replace("#sun", "#moon")
    );
  }

  // Manejador del alternador
  toggle?.addEventListener("click", () => {
    body.classList.toggle("dark-mode");
    const isDark = body.classList.contains("dark-mode");
    localStorage.setItem("theme", isDark ? "dark" : "light");

    // Actualizar icono
    const currentHref = icon?.getAttribute("href") || "";
    const newIcon = isDark ? "#moon" : "#sun";
    icon?.setAttribute("href", currentHref.replace(/#(sun|moon)/, newIcon));
  });
})();

// Alternador de menú desplegable
document.addEventListener("click", (e) => {
  const toggle = e.target.closest(".dropdown-toggle");
  const anyDropdown = e.target.closest(".dropdown");

  // Cerrar todos los menús al hacer clic fuera
  if (!anyDropdown) {
    document
      .querySelectorAll(".dropdown.open")
      .forEach((d) => d.classList.remove("open"));
  }

  // Alternar menú desplegable específico
  if (toggle) {
    const dd = toggle.closest(".dropdown");
    const isOpen = dd.classList.contains("open");
    document
      .querySelectorAll(".dropdown.open")
      .forEach((d) => d.classList.remove("open"));
    dd.classList.toggle("open", !isOpen);
    toggle.setAttribute("aria-expanded", String(!isOpen));
  }
});

// Carrusel de noticias destacadas
(function carruselDestacados() {
  const slides = Array.from(
    document.querySelectorAll(".carrusel .carrusel-slide")
  );
  const dots = Array.from(
    document.querySelectorAll(".carrusel .carrusel-dots .dot")
  );
  const prev = document.querySelector(".carrusel .carrusel-prev");
  const next = document.querySelector(".carrusel .carrusel-next");
  if (!slides.length) return;
  let idx = slides.findIndex((s) => s.classList.contains("active"));
  if (idx < 0) idx = 0;
  const show = (i) => {
    slides.forEach((s, j) => s.classList.toggle("active", j === i));
    dots.forEach((d, j) => d.classList.toggle("active", j === i));
    idx = i;
  };
  const go = (delta) => {
    const n = (idx + delta + slides.length) % slides.length;
    show(n);
  };
  prev && prev.addEventListener("click", () => go(-1));
  next && next.addEventListener("click", () => go(1));
})();

// Alternador de menú de perfil
(function profileMenu() {
  const profileMenu = document.querySelector(".profile-menu");
  const toggle = document.querySelector(".profile-toggle");
  const guestMenu = document.querySelector(".profile-menu-guest");
  const loggedMenu = document.querySelector(".profile-menu-logged");

  // Verificar estado de sesión desde localStorage (solo demo)
  const isLoggedIn = localStorage.getItem("isLoggedIn") === "true";
  updateMenuState(isLoggedIn);

  function updateMenuState(loggedIn) {
    if (guestMenu && loggedMenu) {
      guestMenu.style.display = loggedIn ? "none" : "block";
      loggedMenu.style.display = loggedIn ? "block" : "none";
    }
  }

  // Alternar menú desplegable
  document.addEventListener("click", (e) => {
    const clickedToggle = e.target.closest(".profile-toggle");
    const clickedInside = e.target.closest(".profile-menu");

    if (!clickedInside) {
      profileMenu?.classList.remove("open");
    }

    if (clickedToggle) {
      profileMenu?.classList.toggle("open");
      const isOpen = profileMenu?.classList.contains("open");
      toggle?.setAttribute("aria-expanded", String(isOpen));
    }
  });

  // Demo: Simular inicio de sesión al hacer clic en "Iniciar Sesión"
  document
    .querySelectorAll(".profile-menu-guest .profile-item")
    .forEach((item) => {
      item.addEventListener("click", (e) => {
        if (item.textContent.includes("Iniciar")) {
          e.preventDefault();
          localStorage.setItem("isLoggedIn", "true");
          updateMenuState(true);
          profileMenu?.classList.remove("open");
          console.log("Demo: Usuario conectado");
        }
      });
    });

  // Demo: Simular cierre de sesión al hacer clic en "Cerrar Sesión"
  document.querySelectorAll(".profile-item-logout").forEach((item) => {
    item.addEventListener("click", (e) => {
      e.preventDefault();
      localStorage.setItem("isLoggedIn", "false");
      updateMenuState(false);
      profileMenu?.classList.remove("open");
      console.log("Demo: Sesión cerrada");
    });
  });
})();
