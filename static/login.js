  async function loginUser(event) {
    event.preventDefault(); // Page refresh hone se rokne ke liye

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (data.success) {
            alert(data.message);
            window.location.href = "/chatbot.html"; // Login ke baad chatbot par bhej dega
        } else {
            alert(data.message);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Server error occurred!");
    }
}