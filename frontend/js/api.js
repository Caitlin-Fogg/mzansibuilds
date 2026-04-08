const BASE_URL = "http://127.0.0.1:8000";

function getToken() {
    return localStorage.getItem("token");
}

async function apiRequest(endpoint, method = "GET", data = null) {
    const options = {
        method: method,headers: {
            "Content-Type": "application/json",
        }
    };

    const token = getToken();
    if (token) {
        options.headers["Authorization"] = `Bearer ${token}`;
    }

    if (data) {
        options.body = JSON.stringify(data);
    }

    const response = await fetch(BASE_URL + endpoint, options);

    if (!response.ok) {
        throw new Error("API request failed");
    }

    return response.json();
}