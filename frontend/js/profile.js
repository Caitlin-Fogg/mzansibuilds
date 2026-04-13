/* Handles user profile functionality:
- Loading user details
- Updating profile
- Deleting account
 */

// Fetch and display current user's profile information
async function loadProfile() {
    try {
        // Call backend to get authenticated user's details
        const user = await apiRequest("/users/me");

        const container = document.getElementById("profileInfo");

        // Render user info
        container.innerHTML = `
            <p><b>Username:</b> ${user.username}</p>
            <p><b>Email:</b> ${user.email}</p>
            <p><b>Joined:</b> ${new Date(user.created_at).toLocaleDateString()}</p>
        `;

    } catch (err) {
        console.error(err);
    }
}

// Handle profile update form submission
document.getElementById("updateForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        await apiRequest("/users/me", "PUT", {
            username: username || null,
            email: email || null,
            password: password || null
        });

        alert("Profile updated!");
        loadProfile();

    } catch (err) {
        console.error(err);
        alert("Update failed");
    }
});

// Handle account deletion (requires password confirmation)
document.getElementById("deleteForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const password = document.getElementById("deletePassword").value;

    if (!confirm("Are you sure you want to delete your account?")) return;

    try {
        // Send delete request with password verification
        await apiRequest("/users/me", "DELETE", {
            password: password
        });

        // Clear token and redirect after account deletion
        localStorage.removeItem("token");
        alert("Account deleted");
        window.location.href = "home-page.html";

    } catch (err) {
        console.error(err);
        alert("Delete failed");
    }
});

loadProfile();