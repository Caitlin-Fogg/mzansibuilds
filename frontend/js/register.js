document.getElementById("registerForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        await apiRequest("/users/", "POST", {
            username: username,
            email: email,
            password: password
        });

        alert("Account created successfully!");
        window.location.href = "login.html";

    } catch (error) {
        console.error(error);
        alert("Registration failed");
    }
});