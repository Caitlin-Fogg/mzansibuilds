async function loadProfile() {
    try {
        const user = await apiRequest("/users/me");

        const container = document.getElementById("profileInfo");

        container.innerHTML = `
            <p><b>Username:</b> ${user.username}</p>
            <p><b>Email:</b> ${user.email}</p>
            <p><b>Joined:</b> ${new Date(user.created_at).toLocaleDateString()}</p>
        `;

    } catch (err) {
        console.error(err);
    }
}

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

document.getElementById("deleteForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const password = document.getElementById("deletePassword").value;

    if (!confirm("Are you sure you want to delete your account?")) return;

    try {
        await apiRequest("/users/me", "DELETE", {
            password: password
        });

        localStorage.removeItem("token");
        alert("Account deleted");
        window.location.href = "home-page.html";

    } catch (err) {
        console.error(err);
        alert("Delete failed");
    }
});

loadProfile();