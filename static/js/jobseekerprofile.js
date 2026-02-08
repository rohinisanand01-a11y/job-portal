let captchaCode="";

function generateCaptcha(){
captchaCode=Math.random().toString(36).substring(2,8).toUpperCase();
document.getElementById("captcha").innerText=captchaCode;
}
generateCaptcha();

document.getElementById("experienceType").addEventListener("change",function(){
document.getElementById("experienceBox").style.display =
this.value==="experienced" ? "block" : "none";
});

function openTerms(){
document.getElementById("termsModal").style.display="flex";
}

function closeTerms(){
document.getElementById("termsModal").style.display="none";
}

document.getElementById("registerForm").addEventListener("submit",function(e){
e.preventDefault();

const required=[
"name","email","mobile","address","password","confirmPassword","captchaInput"
];

for(let id of required){
if(!document.getElementById(id).value.trim()){
alert("Please fill all required fields");
return;
}
}

if(!/^\d{10,15}$/.test(document.getElementById("mobile").value)){
alert("Enter valid mobile number with country code");
return;
}

if(document.getElementById("password").value !==
document.getElementById("confirmPassword").value){
alert("Passwords do not match");
return;
}

if(document.getElementById("captchaInput").value !== captchaCode){
alert("Wrong captcha! New captcha generated.");
generateCaptcha();
return;
}

if(!document.getElementById("terms").checked){
alert("Please accept Terms & Conditions");
return;
}

alert("Registration Successful!");
window.location.href="jobseeklogin.html";
});
