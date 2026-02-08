let captcha = "";

function generateCaptcha(){
captcha = Math.random().toString(36).substring(2,8).toUpperCase();
document.getElementById("captchaText").innerText = captcha;
}
generateCaptcha();

function openTerms(){
document.getElementById("termsModal").style.display = "flex";
}

function closeTerms(){
document.getElementById("termsModal").style.display = "none";
}

document.getElementById("employeeForm").addEventListener("submit", function(e){
e.preventDefault();

// Required fields
const required = ["companyName","authName","designation","authEmail","mobile",
"username","password","confirmPassword","country","state","city","officeAddress","zip","captchaInput"];

for(let id of required){
if(!document.getElementById(id).value.trim()){
alert("Please fill all required fields");
return;
}
}

// Company email validation
const email = document.getElementById("authEmail").value.trim();
if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || !email.includes("@")){
alert("Please enter a valid company email (no personal email)");
return;
}

// Mobile number validation (10-15 digits)
const mobile = document.getElementById("mobile").value.trim();
if(!/^\d{10,15}$/.test(mobile)){
alert("Enter valid mobile number with country code");
return;
}

// Password match
if(document.getElementById("password").value !== document.getElementById("confirmPassword").value){
alert("Password and Confirm Password do not match");
return;
}

// Captcha check
if(document.getElementById("captchaInput").value.trim() !== captcha){
alert("Wrong captcha! New captcha generated.");
generateCaptcha();
return;
}

// Terms acceptance
if(!document.getElementById("terms").checked){
alert("Please accept Terms & Conditions");
return;
}

// Success - redirect
alert("Registration Successful! Admin approval required before posting jobs.");
window.location.href="employeelogin.html";
});
