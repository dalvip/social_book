// static/js/protectedData.js
async function fetchProtectedData() {
    const token = localStorage.getItem('authToken');
    const response = await fetch('/api/protected-data/', {
        method: 'GET',
        headers: {
            'Authorization': `Token ${token}`
        }
    });
    const data = await response.json();
    console.log(data);
}
