// Handles user registration (account creation)

// Listen for registration form submission
document.getElementById("registerForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Collect user input values
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        // Send registration data to backend
        await apiRequest("/users/", "POST", {
            username: username,
            email: email,
            password: password
        });

        alert("Account created successfully!");
        window.location.href = "login.html";

    } catch (error) {
        console.error(error);
        alert("Registration failed - Duplicate/Invalid Field");
    }
});