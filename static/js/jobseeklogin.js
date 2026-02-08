


function validateLogin(event) {
    event.preventDefault();

    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const errorMsg = document.getElementById("errorMsg");

    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();

    // Demo registered job seeker emails
    const registeredUsers = [
        "jobseeker@gmail.com",
        "user@example.com",
        "candidate@test.com"
    ];

    // Reset state
    errorMsg.textContent = "";
    emailInput.classList.remove("invalid");
    passwordInput.classList.remove("invalid");

    // Email not found
    if (!registeredUsers.includes(email)) {
        errorMsg.textContent = "Email not found. Please register.";
        emailInput.classList.add("invalid");
        return;
    }

    // Password length check (demo)
    if (password.length < 6) {
        errorMsg.textContent = "Incorrect password";
        passwordInput.classList.add("invalid");
        return;
    }

    // Success
    alert("Job Seeker login successful!");
    // window.location.href = "dashboard.html";
}

