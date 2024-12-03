        // Get modal element and close button
        var modal = document.getElementById("myModal");
        var closeBtn = document.getElementsByClassName("close")[0];

        // Button to open the modal (form)
        var openFormBtn = document.getElementById("openFormBtn");

        // When the user clicks the button, open the modal
        openFormBtn.onclick = function() {
            modal.style.display = "block";  // Show modal
        }

        // When the user clicks on the close button, close the modal
        closeBtn.onclick = function() {
            modal.style.display = "none";  // Hide modal
        }

        // When the user clicks anywhere outside the modal, close it
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";  // Hide modal if clicked outside
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
                        formData.reset()
                    } else {
                        // Success case - Show success message
                        showSuccess(response.message); // Show success message

                        // Optionally reset the form
                        document.getElementById("serverForm").reset();

                        // Close the modal after success
                        modal.style.display = "none"; // Close the modal
                    }
                }
            };

            xhr.send(formData);
        };