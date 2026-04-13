// Handles user authentication (login)
// Sends credentials to backend and stores JWT token

// Listen for login form submission
document.getElementById("loginForm")?.addEventListener("submit", async (e) => {
    // Prevent page reload on form submission
    e.preventDefault();

    // Get user input (email and password)
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    // Format data as URL-encoded form (required by OAuth2 backend)
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    // Send login request to backend authentication endpoint
    const response = await fetch("http://127.0.0.1:8000/users/login", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    // If login successful - store JWT token and redirect user
    if (response.ok) {
        localStorage.setItem("token", data.access_token);
        window.location.href = "index.html";
    // If login fails - show error message
    } else {
        alert("Login failed - Incorrect email or password");
    }
});