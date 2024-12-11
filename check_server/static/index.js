// Modal va form elementlarini olish
const modal = document.getElementById("myModal");
const form = document.getElementById("serverForm");
const formTitle = document.querySelector("#myModal h2");

// Modalni ochish funksiyasi
function openModal(mode, serverId = null) {
    if (mode === "add") {
        form.action = "{% url 'add-server' %}";
        form.method = "POST";
        formTitle.textContent = "Add Server";
        form.reset();
    } else if (mode === "update") {
        fetch(`/servers/${serverId}/`)
            .then(response => response.json())
            .then(data => {
                form.action = `/servers/${serverId}/update/`;
                form.method = "POST";  // PUT o'rniga POST ishlatamiz, keyin PUT ni AJAX orqali jo'natamiz
                formTitle.textContent = "Update Server";
    
                document.getElementById('id_name').value = data.name;
                document.getElementById('id_ssh_port').value = data.ssh_port;
                let ip = String(data.ipv4);
                console.log(typeof(ip))
                document.getElementById('id_ipv4').value = ip;
                document.getElementById('id_username').value = data.username;
                document.getElementById('id_password').value = data.password;
    
                // Modal fetch muvaffaqiyatli yakunlangandan keyin ochiladi
                modal.style.display = "block";
            })
            .catch(error => {
                console.error('Error fetching server data:', error);
                alert('Error fetching server data.');
            });
    }
    modal.style.display = "block";
}

// Add Server tugmasi uchun hodisa
document.getElementById("openFormBtn").onclick = () => openModal("add");

// Update tugmalari uchun hodisa
document.querySelectorAll(".update-btn").forEach(button => {
    button.addEventListener("click", (e) => {
        e.stopPropagation();
        const serverId = button.getAttribute("data-id");
        openModal("update", serverId);
    });
});

// Forma yuborishda PUT/POSTni boshqarish
form.onsubmit = function (e) {
    e.preventDefault();

    const xhr = new XMLHttpRequest();
    const isUpdate = form.action.includes("/update/");
    xhr.open(isUpdate ? "PUT" : "POST", form.action, true);

    xhr.onload = function () {
        const response = JSON.parse(xhr.responseText);
        if (xhr.status === 200 || xhr.status === 201) {
            alert(response.message || "Operation successful");
            location.reload();
        } else {
            alert("Operation failed");
        }
    };

    xhr.onerror = function () {
        alert("An error occurred");
    };

    xhr.send(new FormData(form));
};

// Modalni yopish
document.querySelector('.close').addEventListener("click", () => {
    modal.style.display = "none";
});

// Modal tashqarisiga bosilganda yopish
window.onclick = function (e) {
    if (e.target === modal) {
        modal.style.display = "none";
    }
};

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

function getCsrfToken() {
    const cookieValue = document.cookie.match(/csrftoken=([^ ;]+)/);
    return cookieValue ? cookieValue[1] : "";
}

document.querySelectorAll(".delete-btn").forEach(button => {
    button.addEventListener("click", () => {
        const serverId = button.getAttribute("data-id");
        const deleteUrl = `/servers/${serverId}/update/`;

        if (confirm("Are you sure you want to delete this server?")) {
            fetch(deleteUrl, {
                method: "DELETE",
                headers: {
                    "X-CSRFToken": getCsrfToken(),
                    "Content-Type": "application/json",
                },
            })
            .then(response => {
                if (response.ok) {
                    alert("Server deleted successfully");
                    button.closest(".server-item").remove();
                } else {
                    alert("Failed to delete the server");
                }
            })
            .catch(error => {
                console.error("Error deleting server:", error);
                alert("An error occurred while deleting the server");
            });
        }
    });
});