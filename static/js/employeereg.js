let generatedOTP = "";

function sendOTP() {
  const pass = document.getElementById("password").value;
  const cpass = document.getElementById("confirmPassword").value;
  const agree = document.getElementById("agree").checked;

  if (!agree) {
    alert("Please accept Terms & Conditions");
    return;
  }

  if (pass !== cpass) {
    alert("Passwords do not match");
    return;
  }

  generatedOTP = Math.floor(100000 + Math.random() * 900000);
  alert("Demo OTP: " + generatedOTP);

  document.getElementById("otpSection").style.display = "block";
}

function verifyOTP() {
  const enteredOTP = document.getElementById("otpInput").value;

  if (enteredOTP == generatedOTP) {
    document.getElementById("successMsg").style.display = "block";

    setTimeout(() => {
      window.location.href = "employeelogin.html";
    }, 1500);
  } else {
    alert("Invalid OTP");
  }
}

function openTerms() {
  document.getElementById("termsModal").style.display = "flex";
}

function closeTerms() {
  document.getElementById("termsModal").style.display = "none";
}
