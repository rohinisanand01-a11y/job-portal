let selectedRole = "";

function selectRole(role, element) {
    selectedRole = role;

    // remove active from all
    document.querySelectorAll(".select-box").forEach(box => {
        box.classList.remove("active");
    });

    // add active to clicked box
    element.classList.add("active");
}

function confirmSelection() {
    if (selectedRole === "") {
        alert("Please select Job Seeker or Employee");
        return;
    }

    // 🔥 redirect to FLASK ROUTES (NOT HTML FILES)
    if (selectedRole === "jobseeker") {
        window.location.href = "/jobseeker/login";
    } else {
        window.location.href = "/employee/login";
    }
}
