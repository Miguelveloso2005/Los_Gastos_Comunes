document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const tableBody = document.querySelector("table tbody");
    const messageContainer = document.querySelector("#message-container");
    const selectAllCheckbox = document.querySelector("#select-all");
    const markAllButton = document.querySelector("#mark-all-paid");

    // Obtener el token CSRF
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Lógica para el formulario
    form.addEventListener("submit", async function (event) {
        event.preventDefault(); // Previene el envío tradicional del formulario

        const formData = new FormData(form);

        try {
            // Realizar la solicitud al backend
            const response = await fetch(form.action, {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": csrfToken,
                    "X-Requested-With": "XMLHttpRequest",
                },
            });

            if (response.ok) {
                const data = await response.json();

                // Crear una nueva fila en la tabla
                const newRow = document.createElement("tr");
                newRow.innerHTML = `
                    <td><input type="checkbox" class="select-gasto" data-id="${data.id}"></td>
                    <td>${data.id}</td>
                    <td>${data.descripcion}</td>
                    <td>${data.monto}</td>
                    <td>${data.fecha_creacion}</td>
                    <td>
                        <button class="btn-mark-paid" data-id="${data.id}" data-departamento="${data.departamento}" data-periodo="${data.periodo}">
                            Marcar como Pagado
                        </button>
                    </td>
                `;

                // Agregar la nueva fila al principio del tbody
                tableBody.prepend(newRow);

                // Limpiar el formulario
                form.reset();

                // Mensaje de éxito
                alert("Gasto generado exitosamente.");
            } else {
                const errorData = await response.json();
                alert("Error al agregar el gasto: " + errorData.error);
            }
        } catch (error) {
            console.error("Error al procesar la solicitud:", error);
            alert("Hubo un error al procesar la solicitud. Por favor, intenta de nuevo.");
        }
    });

    // Evento para marcar un gasto como pagado
    document.querySelector(".table-container table tbody").addEventListener("click", async function (event) {
        if (event.target.classList.contains("btn-mark-paid")) {
            const gastoId = event.target.dataset.id;
            const departamento = event.target.dataset.departamento;
            const periodo = event.target.dataset.periodo;

            if (confirm(`¿Está seguro que desea marcar el gasto del Departamento ${departamento} en el período ${periodo} como pagado?`)) {
                try {
                    const response = await fetch(`/gasto/pagado/${gastoId}/`, {
                        method: "POST",
                        headers: {
                            "X-CSRFToken": csrfToken,
                            "X-Requested-With": "XMLHttpRequest",
                        },
                    });

                    if (response.ok) {
                        // Eliminar la fila de la tabla
                        const row = event.target.closest("tr");
                        row.remove(); // Eliminar la fila "tr" del DOM

                        // Mostrar el mensaje de éxito
                        showMessage("Gasto Común Pagado Exitosamente");
                    } else {
                        alert("Error al marcar el gasto como pagado");
                    }
                } catch (error) {
                    console.error("Error al procesar la solicitud:", error);
                }
            }
        }
    });

    // Evento para marcar todos los gastos seleccionados como pagados
    markAllButton.addEventListener("click", async function () {
        const selectedGastos = document.querySelectorAll(".select-gasto:checked");

        if (selectedGastos.length === 0) {
            alert("Por favor, selecciona al menos un gasto.");
            return;
        }

        const gastoIds = Array.from(selectedGastos).map(checkbox => checkbox.dataset.id);

        try {
            const response = await fetch(`/gasto/pagado/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "X-Requested-With": "XMLHttpRequest",
                },
                body: JSON.stringify({ gasto_ids: gastoIds }), // Enviar los IDs seleccionados
            });

            if (response.ok) {
                selectedGastos.forEach(checkbox => {
                    const row = checkbox.closest('tr');
                    row.remove();
                });
                showMessage("Gastos marcados como pagados exitosamente.");
            } else {
                alert("Error al marcar los gastos como pagados.");
            }
        } catch (error) {
            console.error("Error al procesar la solicitud:", error);
            alert("Hubo un error al procesar la solicitud.");
        }
    });

    // Función para mostrar el mensaje de éxito
    function showMessage(message) {
        messageContainer.textContent = message;
        messageContainer.style.display = "block";
        setTimeout(() => {
            messageContainer.style.display = "none";
        }, 3000);
    }

    // Evento para seleccionar todos los checkboxes
    selectAllCheckbox.addEventListener("change", function () {
        const checkboxes = document.querySelectorAll(".select-gasto");
        checkboxes.forEach(checkbox => {
            checkbox.checked = selectAllCheckbox.checked;
        });
    });
});
