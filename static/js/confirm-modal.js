// Modal de confirmación personalizado
function showConfirmModal(message, onConfirm, onCancel = null, options = {}) {
  const title = options.title || "¡Atención!";
  const confirmText = options.confirmText || "Confirmar Acción";
  const cancelText = options.cancelText || "Cancelar";

  // Crear el modal
  const modalHtml = `
    <div class="custom-confirm-overlay" id="customConfirmOverlay">
      <div class="custom-confirm-modal">
        <div class="custom-confirm-icon">
          <i class="bi bi-exclamation-triangle-fill"></i>
        </div>
        <h3 class="custom-confirm-title">${title}</h3>
        <p class="custom-confirm-message">${message}</p>
        <div class="custom-confirm-buttons">
          <button class="btn-confirm-cancel" id="btnConfirmCancel">
            ${cancelText}
          </button>
          <button class="btn-confirm-accept" id="btnConfirmAccept">
            ${confirmText}
          </button>
        </div>
      </div>
    </div>
  `;

  // Agregar al body
  document.body.insertAdjacentHTML("beforeend", modalHtml);

  const overlay = document.getElementById("customConfirmOverlay");
  const btnCancel = document.getElementById("btnConfirmCancel");
  const btnAccept = document.getElementById("btnConfirmAccept");

  // Animación de entrada
  setTimeout(() => overlay.classList.add("show"), 10);

  // Función para cerrar el modal
  function closeModal(confirmed) {
    overlay.classList.remove("show");
    setTimeout(() => {
      overlay.remove();
      if (confirmed && onConfirm) {
        onConfirm();
      } else if (!confirmed && onCancel) {
        onCancel();
      }
    }, 300);
  }

  // Event listeners
  btnCancel.addEventListener("click", () => closeModal(false));
  btnAccept.addEventListener("click", () => closeModal(true));
  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) closeModal(false);
  });

  // ESC para cerrar
  document.addEventListener("keydown", function escHandler(e) {
    if (e.key === "Escape") {
      closeModal(false);
      document.removeEventListener("keydown", escHandler);
    }
  });
}

// Función auxiliar para enlaces con confirmación
function confirmDelete(event, message) {
  event.preventDefault();
  const href = event.currentTarget.href;

  showConfirmModal(message, () => {
    window.location.href = href;
  });
}
