// Get modal elements
var modalApp = document.getElementById("myModalApp");
var modalDockerApp = document.getElementById("myModalDockerApp");
var modalDomain = document.getElementById("myModalDomain");

// Get buttons to open modals
var openFormBtnApp = document.getElementById("openFormBtnApp");
var openFormBtnDocker = document.getElementById("openFormBtnDockerApp");
var openFormBtnDomain = document.getElementById("openFormBtnDomain");

// Get close buttons
var closeBtns = document.getElementsByClassName("close");

// Function to open a modal
function openModal(modal) {
    modal.style.display = "block";
}

// Function to close a modal
function closeModal(modal) {
    modal.style.display = "none";
}

// Event listeners for opening modals
openFormBtnApp.onclick = function() {
    openModal(modalApp);
}
openFormBtnDocker.onclick = function() {
    openModal(modalDockerApp);
}
openFormBtnDomain.onclick = function() {
    openModal(modalDomain);
}

// Event listeners for closing modals
for (var i = 0; i < closeBtns.length; i++) {
    closeBtns[i].onclick = function() {
        closeModal(modalApp);
        closeModal(modalDomain);
        closeModal(modalDockerApp);
    }
}

// Close modals when clicking outside of them
window.onclick = function(event) {
    if (event.target == modalApp) {
        closeModal(modalApp);
    } else if (event.target == modalDomain) {
        closeModal(modalDomain);
    } else if (event.target == modalDockerApp) {
        closeModal(modalDockerApp);
    }
}

// Function to show error popup with a message
function showError(message) {
    var errorPopup = document.getElementById("errorPopup");
    errorPopup.textContent = message;
    errorPopup.style.display = "block";

    setTimeout(function() {
        errorPopup.style.display = "none";
    }, 5000);
}

// Function to show success popup with a message
function showSuccess(message) {
    var successPopup = document.createElement('div');
    successPopup.classList.add('success-popup');
    successPopup.textContent = message;

    document.body.appendChild(successPopup);
    successPopup.style.display = "block";

    setTimeout(function() {
        successPopup.style.display = "none";
        document.body.removeChild(successPopup);
    }, 5000);
}

// Function to handle form submission
function handleFormSubmission(formId, modal) {
    var form = document.getElementById(formId);
    form.onsubmit = function(event) {
        event.preventDefault();  // Prevent page reload on form submission

        var formData = new FormData(this);
        var xhr = new XMLHttpRequest();
        xhr.open("POST", this.action, true);

        xhr.onload = function() {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);

                if (response.success === false) {
                    // Show errors if any
                    for (var key in response.message) {
                        if (response.message.hasOwnProperty(key)) {
                            showError(response.message[key].join(", "));
                        }
                    }
                } else {
                    // Show success message and reset form
                    showSuccess(response.message);
                    form.reset();
                    closeModal(modal); // Close the modal after success
                }
            }
        };

        xhr.send(formData);  // Send the form data with the XMLHttpRequest
    };
}

// Function to handle form submission
function handleFormSubmission(formId, modal) {
    var form = document.getElementById(formId);
    form.onsubmit = function(event) {
        event.preventDefault();  // Prevent page reload on form submission

        var formData = new FormData(this);
        var xhr = new XMLHttpRequest();
        xhr.open("POST", this.action, true);

        xhr.onload = function() {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);

                if (response.success === false) {
                    // Show errors if any
                    for (var key in response.message) {
                        if (response.message.hasOwnProperty(key)) {
                            showError(response.message[key].join(", "));
                        }
                    }
                } else {
                    // Show success message and reset form
                    showSuccess(response.message);
                    form.reset();
                    closeModal(modal); // Close the modal after success
                    
                    // Refresh the page if success is true
                    if (response.success === true) {
                        setTimeout(function() {
                            location.reload(); // Refresh the page
                        }, 1000); // Add a small delay if needed
                    }
                }
            }
        };

        xhr.send(formData);  // Send the form data with the XMLHttpRequest
    };
}


// Attach form handlers to all forms
handleFormSubmission("serverForm", modalApp);  // For the "App" modal
handleFormSubmission("serverFormDockerApp", modalDockerApp);  // For the Docker modal
handleFormSubmission("serverFormDomain", modalDomain);  // For the Domain modal
