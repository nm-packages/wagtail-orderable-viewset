import Sortable from "https://cdn.jsdelivr.net/npm/sortablejs@1.15.0/+esm";

document.addEventListener('DOMContentLoaded', function () {
    const orderableList = document.getElementById('orderable-list');
    const saveStatus = document.getElementById('save-status');
    if (!orderableList) return;
    let isSaving = false;

    // Function to show status message
    function showStatus(message, type) {
        saveStatus.innerHTML = `
          <div class="messages">
            <div class="message ${type}">
              <a href="#" class="icon icon-${type === 'success' ? 'success' : 'warning'}"></a>
              <p>${message}</p>
            </div>
          </div>
        `;
        saveStatus.style.display = 'block';

        // Hide after 3 seconds
        setTimeout(() => {
            saveStatus.style.display = 'none';
        }, 3000);
    }

    // Function to save the order
    function saveOrder() {
        if (isSaving) return; // Prevent multiple simultaneous saves

        const items = orderableList.querySelectorAll("li");
        const order = Array.from(items).map((item) => item.getAttribute("data-id"));

        isSaving = true;

        // Extract CSRF token from hidden form field
        const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
        const csrfToken = csrfInput ? csrfInput.value : undefined;

        // Prepare headers, only set X-CSRFToken if token is found
        const headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
        };
        if (csrfToken) {
            headers["X-CSRFToken"] = csrfToken;
        }
        const formData = new URLSearchParams();
        order.forEach((id) => formData.append('object_ids[]', id));

        const updateUrl = orderableList.dataset.updateUrl;
        fetch(updateUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                "X-CSRFToken": csrfToken,
            },
            body: formData,
            credentials: 'same-origin',
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showStatus("Order saved successfully", "success");
                } else {
                    console.error("Error saving order:", data.error || "Unknown error");
                    showStatus("Error saving order: " + (data.error || "Unknown error"), "error");
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showStatus("Error saving order", "error");
            })
            .finally(() => {
                isSaving = false;
            });
    }

    // Function to update button visibility based on position
    function updateButtonVisibility() {
        const items = orderableList.querySelectorAll("li");

        items.forEach((item, index) => {
            const moveFirstBtn = item.querySelector('.move-first');
            const moveLastBtn = item.querySelector('.move-last');

            // Hide/show Move First button
            if (index === 0) {
                moveFirstBtn.style.display = 'none';
            } else {
                moveFirstBtn.style.display = 'inline-flex';
            }

            // Hide/show Move Last button
            if (index === items.length - 1) {
                moveLastBtn.style.display = 'none';
            } else {
                moveLastBtn.style.display = 'inline-flex';
            }
        });
    }

    // Function to move item to specific position
    function moveItem(itemId, position) {
        const item = orderableList.querySelector(`li[data-id="${itemId}"]`);
        if (!item) return;

        if (position === 'first') {
            orderableList.insertBefore(item, orderableList.firstChild);
            // Scroll to top of the list
            setTimeout(() => {
                orderableList.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 100);
        } else if (position === 'last') {
            orderableList.appendChild(item);
            // Scroll to bottom of the list
            setTimeout(() => {
                orderableList.scrollIntoView({ behavior: 'smooth', block: 'end' });
            }, 100);
        }

        // Update button visibility after moving
        updateButtonVisibility();

        // Save the new order
        saveOrder();
    }

    // Add event listeners for Move First/Last buttons
    orderableList.addEventListener('click', function (e) {
        e.preventDefault();

        if (e.target.closest('.move-first')) {
            const itemId = e.target.closest('.move-first').getAttribute('data-id');
            moveItem(itemId, 'first');
        } else if (e.target.closest('.move-last')) {
            const itemId = e.target.closest('.move-last').getAttribute('data-id');
            moveItem(itemId, 'last');
        }
    });

    // Initialize Sortable with auto-save on end
    const sortable = Sortable.create(orderableList, {
        handle: ".listing__item__drag-handle",
        animation: 150,
        ghostClass: "sortable-ghost",
        chosenClass: "sortable-chosen",
        dragClass: "sortable-drag",
        onEnd: function () {
            // Update button visibility after drag ends
            updateButtonVisibility();
            // Auto-save when drag ends
            saveOrder();
        }
    });

    // Initial button visibility setup
    updateButtonVisibility();
});
