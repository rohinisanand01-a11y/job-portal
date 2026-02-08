let generatedOTP = "";

function openTerms() {
  document.getElementById("termsModal").style.display = "flex";
}

function closeTerms() {
  document.getElementById("termsModal").style.display = "none";
}

function sendOTP() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirmPassword").value;
  const agree = document.getElementById("agree").checked;

  if (!email || !password || !confirmPassword) {
    alert("Please fill all fields");
    return;
  }

  if (password !== confirmPassword) {
    alert("Passwords do not match");
    return;
  }

  if (!agree) {
    alert("Please agree to Terms & Conditions");
    return;
  }

  generatedOTP = Math.floor(100000 + Math.random() * 900000).toString();
  alert("Your OTP is: " + generatedOTP); // demo purpose

  document.getElementById("otpSection").style.display = "block";
}

function verifyOTP() {
  const enteredOTP = document.getElementById("otpInput").value;

  if (enteredOTP === generatedOTP) {
    document.getElementById("successMsg").style.display = "block";
    setTimeout(() => {
      window.location.href = "/jobseeker/login";

    }, 1500);
  } else {
    alert("Invalid OTP");
  }
}
