"use strict"

// INPUT VALIDATION
document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.querySelector(".needs-validation");

    loginForm.addEventListener("submit", (event) => {
        if (!loginForm.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
            displayValidationErrors();
        }
        loginForm.classList.add("was-validated");
    })

    function displayValidationErrors() {
        const validationErrors = document.getElementById("validation-error");
        validationErrors.innerHTML = "Please fill out all the required fields correctly!"
    }
})
