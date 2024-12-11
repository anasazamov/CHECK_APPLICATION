// ===============================
// Modal Elements
// ===============================

// Modals for Apps, Docker Apps, and Domains
const modalApp = document.getElementById("myModalApp");
const modalDockerApp = document.getElementById("myModalDockerApp");
const modalDomain = document.getElementById("myModalDomain");

// Forms for Apps, Docker Apps, and Domains
const appForm = document.getElementById("serverForm");
const dockerAppForm = document.getElementById("serverFormDockerApp");
const domainForm = document.getElementById("serverFormDomain");

// Close buttons for modals
const closeButtons = document.querySelectorAll(".close");

// ===============================
// Open and Close Modal Functions
// ===============================

// Function to open a modal
function openModal(modal) {
    modal.style.display = "block";
}

// Function to close a modal
function closeModal(modal) {
    modal.style.display = "none";
}

// Event listeners for opening modals
document.getElementById("openFormBtnApp").onclick = () => openModal(modalApp);
document.getElementById("openFormBtnDockerApp").onclick = () => openModal(modalDockerApp);
document.getElementById("openFormBtnDomain").onclick = () => openModal(modalDomain);

// Event listeners for closing modals
closeButtons.forEach(button => {
    button.addEventListener("click", () => {
        closeModal(modalApp);
        closeModal(modalDockerApp);
        closeModal(modalDomain);
    });
});

// Close modals when clicking outside the modal content
window.addEventListener("click", (e) => {
    if (e.target === modalApp) closeModal(modalApp);
    if (e.target === modalDockerApp) closeModal(modalDockerApp);
    if (e.target === modalDomain) closeModal(modalDomain);
});

// ===============================
// Handle Form Submissions with PUT for Updates
// ===============================

function handleFormSubmission(form, modal) {
    form.onsubmit = function (e) {
        e.preventDefault();

        // Determine if it's an update (PUT) or a new submission (POST)
        const isUpdate = form.action.includes("/update/");
        const xhr = new XMLHttpRequest();
        xhr.open(isUpdate ? "PUT" : "POST", form.action, true);

        // For PUT requests, send JSON data
        if (isUpdate) {
            xhr.setRequestHeader("Content-Type", "application/json");

            const formData = new FormData(form);
            const jsonData = {};
            formData.forEach((value, key) => {
                jsonData[key] = value;
            });
            xhr.send(JSON.stringify(jsonData));
        } else {
            // For POST requests, send FormData directly
            xhr.send(new FormData(form));
        }

        xhr.onload = function () {
            if (xhr.status === 200 || xhr.status === 201) {
                alert("Operation successful");
                form.reset();
                closeModal(modal);
                location.reload();
            } else {
                alert("Operation failed");
            }
        };

        xhr.onerror = function () {
            alert("An error occurred");
        };
    };
}

// Attach form submission handlers
handleFormSubmission(appForm, modalApp);
handleFormSubmission(dockerAppForm, modalDockerApp);
handleFormSubmission(domainForm, modalDomain);

// ===============================
// Update and Delete Functionality
// ===============================

// Function to handle fetching data and opening update modal
function openUpdateModal(type, id) {
    let modal, form, fetchUrl, updateUrl;

    if (type === "app") {
        modal = modalApp;
        form = appForm;
        fetchUrl = `/app/${id}/`;
        updateUrl = `/apps/${id}/update/`;
    } else if (type === "docker") {
        modal = modalDockerApp;
        form = dockerAppForm;
        fetchUrl = `/docker-apps/${id}/`;
        updateUrl = `/docker-apps/${id}/update/`;
    } else if (type === "domain") {
        modal = modalDomain;
        form = domainForm;
        fetchUrl = `/domains/${id}/`;
        updateUrl = `/domains/${id}/update/`;
    }

    // Fetch existing data and populate the form
    fetch(fetchUrl)
        .then(response => response.json())
        .then(data => {
            form.action = updateUrl;

            // Populate form fields based on type
            if (type === "app") {
                form.querySelector('input[name="name_run_on_server"]').value = data.name_run_on_server;
                form.querySelector('input[name="port"]').value = data.port;
            } else if (type === "docker") {
                form.querySelector('input[name="name_run_on_docker"]').value = data.name_run_on_docker;
                form.querySelector('input[name="container_name"]').value = data.container_name;
                form.querySelector('input[name="port"]').value = data.port;
            } else if (type === "domain") {
                form.querySelector('input[name="domain"]').value = data.domain;
            }

            openModal(modal);
        })
        .catch(error => {
            console.error("Error fetching data:", error);
            alert("Error fetching data.");
        });
}

// Attach update event listeners
document.querySelectorAll(".update-btn").forEach(button => {
    button.addEventListener("click", () => {
        const id = button.getAttribute("data-id");
        const type = button.getAttribute("data-type"); // app, docker, or domain
        openUpdateModal(type, id);
    });
});

// ===============================
// Redirect on Item Click
// ===============================

// Add event listeners for items to redirect based on the data-link attribute
document.querySelectorAll(".server-item, .domain-item").forEach(item => {
    item.addEventListener("click", (e) => {
        // Prevent the click event from affecting buttons inside the item
        if (e.target.tagName === 'BUTTON') {
            return;
        }
        
        const link = item.getAttribute("data-link");
        if (link) {
            window.location.href = link;
        }
    });
});

// ===============================
// Handle Delete Requests
// ===============================

function getCsrfToken() {
    const cookieValue = document.cookie.match(/csrftoken=([^ ;]+)/);
    return cookieValue ? cookieValue[1] : "";
}


document.querySelectorAll(".delete-btn").forEach(button => {
    button.addEventListener("click", () => {
        const id = button.getAttribute("data-id");
        const type = button.getAttribute("data-type"); // 'app', 'docker', or 'domain'

        let deleteUrl;
        if (type === "app") {
            deleteUrl = `/apps/${id}/update/`;
        } else if (type === "docker") {
            deleteUrl = `/docker-apps/${id}/update/`;
        } else if (type === "domain") {
            deleteUrl = `/domains/${id}/update/`;
        }

        if (confirm("Are you sure you want to delete this item?")) {
            fetch(deleteUrl, {
                method: "DELETE",
                headers: {
                    "X-CSRFToken": getCsrfToken(),
                },
            })
            .then(response => {
                if (response.ok) {
                    alert("Item deleted successfully");
                    location.reload();
                } else {
                    alert("Failed to delete the item");
                }
            })
            .catch(error => {
                console.error("Error deleting item:", error);
                alert("An error occurred while deleting the item");
            });
        }
    });
});