        // Get modal elements and close buttons
        var modalApp = document.getElementById("myModalApp");
        var modalDomain = document.getElementById("myModalDomain");
        var closeBtns = document.getElementsByClassName("close");

        // Button to open the modal for Apps
        var openFormBtnApp = document.getElementById("openFormBtnApp");
        // Button to open the modal for Domains
        var openFormBtnDomain = document.getElementById("openFormBtnDomain");

        // When the user clicks the button for Apps, open the modal
        openFormBtnApp.onclick = function() {
            modalApp.style.display = "block";  // Show Apps modal
        }

        // When the user clicks the button for Domains, open the modal
        openFormBtnDomain.onclick = function() {
            modalDomain.style.display = "block";  // Show Domains modal
        }

        // When the user clicks on the close button for either modal, close it
        for (var i = 0; i < closeBtns.length; i++) {
            closeBtns[i].onclick = function() {
                modalApp.style.display = "none";  // Hide Apps modal
                modalDomain.style.display = "none";  // Hide Domains modal
            }
        }

        // When the user clicks anywhere outside the modal, close it
        window.onclick = function(event) {
            if (event.target == modalApp) {
                modalApp.style.display = "none";  // Hide Apps modal if clicked outside
            } else if (event.target == modalDomain) {
                modalDomain.style.display = "none";  // Hide Domains modal if clicked outside
            }
        }

        // Function to show error popup with a message
        function showError(message) {
            var errorPopup = document.getElementById("errorPopup");
            errorPopup.textContent = message;  // Set the error message text
            errorPopup.style.display = "block"; // Show the popup

            // Automatically hide the popup after 5 seconds
            setTimeout(function() {
                errorPopup.style.display = "none"; // Hide the popup
            }, 5000);
        }

        function showSuccess(message) {
            var successPopup = document.createElement('div');
            successPopup.classList.add('success-popup');
            successPopup.textContent = message;

            // Append the success popup to the body
            document.body.appendChild(successPopup);

            // Show the success popup
            successPopup.style.display = "block";

            // Automatically hide the success popup after 5 seconds
            setTimeout(function() {
                successPopup.style.display = "none"; // Hide the popup
                document.body.removeChild(successPopup); // Remove the popup element from DOM
            }, 5000);
        }

        // Handle form submission with Ajax to prevent page reload
        document.getElementById("serverForm").onsubmit = function(event) {
            event.preventDefault();  // Prevent default form submission

            var formData = new FormData(this);
            var xhr = new XMLHttpRequest();
            xhr.open("POST", this.action, true);

            xhr.onload = function() {
                if (xhr.status === 200) {
                    var response = JSON.parse(xhr.responseText);

                    if (response.success === false) {
                        // Loop through error messages and show them
                        for (var key in response.message) {
                            if (response.message.hasOwnProperty(key)) {
                                showError(response.message[key].join(", "));
                            }
                        }
                    } else {
                        // Success case - Show success message
                        showSuccess(response.message); // Show success message

                        // Optionally reset the form
                        document.getElementById("serverForm").reset();

                        // Close the modal after success
                        modalApp.style.display = "none"; // Close the modal
                    }
                }
            };

            xhr.send(formData);
        };

        document.getElementById("serverFormDomain").onsubmit = function(event) {
            event.preventDefault();  // Prevent default form submission

            var formData = new FormData(this);
            var xhr = new XMLHttpRequest();
            xhr.open("POST", this.action, true);

            xhr.onload = function() {
                if (xhr.status === 200) {
                    var response = JSON.parse(xhr.responseText);

                    if (response.success === false) {
                        // Loop through error messages and show them
                        for (var key in response.message) {
                            if (response.message.hasOwnProperty(key)) {
                                showError(response.message[key].join(", "));
                            }
                        }
                    } else {
                        // Success case - Show success message
                        showSuccess(response.message); // Show success message

                        // Optionally reset the form
                        document.getElementById("serverFormDomain").reset();

                        // Close the modal after success
                        modalDomain.style.display = "none"; // Close the modal
                    }
                }
            };

            xhr.send(formData);
        };