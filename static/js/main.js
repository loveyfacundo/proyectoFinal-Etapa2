// Archivo JavaScript principal
console.log("TodoDeporte cargado correctamente");

// Auto-ocultar notificaciones después de 5 segundos
(function autoHideMessages() {
  const messages = document.querySelectorAll('.msg');
  if (messages.length > 0) {
    messages.forEach(msg => {
      setTimeout(() => {
        msg.style.transition = 'opacity 0.5s ease-out, transform 0.5s ease-out';
        msg.style.opacity = '0';
        msg.style.transform = 'translateY(-20px)';
        setTimeout(() => msg.remove(), 500);
      }, 5000);
    });
  }
})();

// Menú móvil desplegable
(function mobileMenu() {
  const menuToggle = document.querySelector(".mobile-menu-toggle");
  const mobileMenu = document.querySelector(".mobile-menu");
  const body = document.body;

  console.log("Menú móvil inicializado:", { menuToggle, mobileMenu });

  if (!menuToggle || !mobileMenu) {
    console.warn("No se encontraron elementos del menú móvil");
    return;
  }

  const menuIcon = menuToggle.querySelector(".menu-icon use");

  // Abrir/cerrar menú
  menuToggle.addEventListener("click", () => {
    const isOpen = mobileMenu.classList.contains("open");
    mobileMenu.classList.toggle("open");
    menuToggle.classList.toggle("open");
    menuToggle.setAttribute("aria-expanded", String(!isOpen));
    body.style.overflow = !isOpen ? "hidden" : "";

    // Cambiar icono
    if (menuIcon) {
      const currentHref = menuIcon.getAttribute("href") || "";
      const newIcon = !isOpen ? "#x" : "#menu";
      menuIcon.setAttribute("href", currentHref.replace(/#(menu|x)/, newIcon));
    }
  });

  // Cerrar menú al hacer clic fuera
  mobileMenu.addEventListener("click", (e) => {
    if (e.target === mobileMenu) {
      mobileMenu.classList.remove("open");
      menuToggle.classList.remove("open");
      menuToggle.setAttribute("aria-expanded", "false");
      body.style.overflow = "";

      // Restaurar icono
      if (menuIcon) {
        const currentHref = menuIcon.getAttribute("href") || "";
        menuIcon.setAttribute(
          "href",
          currentHref.replace(/#(menu|x)/, "#menu")
        );
      }
    }
  });

  // Submenu toggle
  const dropdownToggles = document.querySelectorAll(".mobile-dropdown-toggle");
  dropdownToggles.forEach((toggle) => {
    toggle.addEventListener("click", (e) => {
      e.preventDefault();
      const parent = toggle.closest(".mobile-dropdown");
      const isOpen = parent.classList.contains("open");

      // Cerrar otros submenus
      document.querySelectorAll(".mobile-dropdown.open").forEach((dd) => {
        if (dd !== parent) dd.classList.remove("open");
      });

      parent.classList.toggle("open", !isOpen);
    });
  });

  // Cerrar menú al hacer clic en un enlace
  const mobileLinks = mobileMenu.querySelectorAll(
    ".mobile-nav-link:not(.mobile-dropdown-toggle), .mobile-submenu-link"
  );
  mobileLinks.forEach((link) => {
    link.addEventListener("click", () => {
      mobileMenu.classList.remove("open");
      menuToggle.classList.remove("open");
      menuToggle.setAttribute("aria-expanded", "false");
      body.style.overflow = "";

      // Restaurar icono
      if (menuIcon) {
        const currentHref = menuIcon.getAttribute("href") || "";
        menuIcon.setAttribute(
          "href",
          currentHref.replace(/#(menu|x)/, "#menu")
        );
      }
    });
  });
})();

// Alternador de tema - Modo oscuro/claro
(function themeToggle() {
  const body = document.body;
  const toggles = document.querySelectorAll(".theme-toggle");

  // Cargar tema guardado
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {
    body.classList.add("dark-mode");
    toggles.forEach(toggle => {
      const icon = toggle.querySelector(".theme-icon use");
      if (icon) {
        icon.setAttribute(
          "href",
          icon.getAttribute("href").replace("#sun", "#moon")
        );
      }
    });
  }

  // Manejador del alternador para todos los botones
  toggles.forEach(toggle => {
    toggle.addEventListener("click", () => {
      body.classList.toggle("dark-mode");
      const isDark = body.classList.contains("dark-mode");
      localStorage.setItem("theme", isDark ? "dark" : "light");

      // Actualizar icono en TODOS los botones de tema
      toggles.forEach(btn => {
        const icon = btn.querySelector(".theme-icon use");
        if (icon) {
          const currentHref = icon.getAttribute("href") || "";
          const newIcon = isDark ? "#moon" : "#sun";
          icon.setAttribute("href", currentHref.replace(/#(sun|moon)/, newIcon));
        }
      });
    });
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
  // document
  //   .querySelectorAll(".profile-menu-guest .profile-item")
  //   .forEach((item) => {
  //     item.addEventListener("click", (e) => {
  //       if (item.textContent.includes("Iniciar")) {
  //         e.preventDefault();
  //         localStorage.setItem("isLoggedIn", "true");
  //         updateMenuState(true);
  //         profileMenu?.classList.remove("open");
  //         console.log("Demo: Usuario conectado");
  //       }
  //     });
  //   });

  // Demo: Simular cierre de sesión al hacer clic en "Cerrar Sesión"
  // document.querySelectorAll(".profile-item-logout").forEach((item) => {
  //   item.addEventListener("click", (e) => {
  //     e.preventDefault();
  //     localStorage.setItem("isLoggedIn", "false");
  //     updateMenuState(false);
  //     profileMenu?.classList.remove("open");
  //     console.log("Demo: Sesión cerrada");
  //   });
  // });
})();
