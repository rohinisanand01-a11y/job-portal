function validateEmployeeLogin() {
    const email = document.getElementById("email").value.trim();
    const errorMsg = document.getElementById("errorMsg");

    const personalDomains = [
        "gmail.com",
        "yahoo.com",
        "hotmail.com",
        "outlook.com",
        "icloud.com"
    ];

    const domain = email.split("@")[1];

    if (!domain) {
        errorMsg.textContent = "Please enter a valid company email";
        return false;
    }

    if (personalDomains.includes(domain.toLowerCase())) {
        errorMsg.textContent = "Personal email is not allowed. Use company email.";
        return false;
    }

    errorMsg.textContent = "";
    return true;   // ✅ allow Flask POST
}