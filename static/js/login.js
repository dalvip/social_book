// static/js/login.js
async function loginUser(username, password) {
    try {
        const response = await fetch('/auth/token/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('authToken', data.auth_token);  // Store token
            window.location.href = '/home/'; // Redirect to home page
        } else {
            console.log("Login failed");
        }
    } catch (error) {
        console.error('Error:', error);
    }
}
