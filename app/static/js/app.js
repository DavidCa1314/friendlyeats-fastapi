document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("restaurant-form");
  const messageEl = document.getElementById("message");

  // Control del Formulario (Crear y Editar)
  if (form) {
    form.addEventListener("submit", async (event) => {
      event.preventDefault();

      if (messageEl) {
        messageEl.textContent = "Guardando...";
        messageEl.className = "text-center mt-4 font-semibold text-sm text-slate-500";
      }

      // 1. Extraer los datos del formulario
      const formData = Object.fromEntries(new FormData(form));
      formData.price = Number(formData.price);

      if (!formData.photoUrl) {
        formData.photoUrl = null;
      }

      // 2. Identificar si estamos Editando o Creando
      const restaurantId = form.dataset.id;
      const isEdit = Boolean(restaurantId && restaurantId.trim() !== "");

      // Usamos el prefijo /api/v1/restaurants exactamente como está en tu main.py y restaurants.py
      const url = isEdit ? `/api/v1/restaurants/${restaurantId}` : "/api/v1/restaurants";
      const method = isEdit ? "PATCH" : "POST";

      try {
        const response = await fetch(url, {
          method: method,
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(formData)
        });

        if (response.ok) {
          if (messageEl) {
            messageEl.textContent = isEdit ? "¡Restaurante actualizado correctamente!" : "¡Restaurante creado correctamente!";
            messageEl.className = "text-center mt-4 font-semibold text-sm text-emerald-600";
          }

          setTimeout(() => {
            window.location.href = isEdit ? `/restaurants/${restaurantId}` : "/";
          }, 1000);

        } else {
          const error = await response.json();
          if (messageEl) {
            messageEl.textContent = error.detail || "Error al guardar el restaurante";
            messageEl.className = "text-center mt-4 font-semibold text-sm text-red-600";
          }
        }
      } catch (err) {
        if (messageEl) {
          messageEl.textContent = "Error de conexión con el servidor";
          messageEl.className = "text-center mt-4 font-semibold text-sm text-red-600";
        }
      }
    });
  }
});

// Función global para Eliminar (invocada desde el modal de la vista de detalle)
async function deleteRestaurant(id) {
  try {
    const response = await fetch(`/api/v1/restaurants/${id}`, {
      method: "DELETE"
    });

    if (response.ok) {
      window.location.href = "/";
    } else {
      const error = await response.json();
      alert(error.detail || "Error al eliminar el restaurante");
    }
  } catch (err) {
    alert("Error de conexión al intentar eliminar");
  }
}