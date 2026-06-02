
async function handleSignup(event) {
    event.preventDefault();
    
    // Get values from the input fields
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    const userData = {
        username: username,
        email: email,
        password: password,
        confirmPassword: confirmPassword
    };
    
    try {
        const response = await fetch('/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        });

        const result = await response.json();
        
        // Display message
        const msgElement = document.getElementById('msg');
        if(msgElement) {
            msgElement.innerText = result.message;
            msgElement.style.color = result.success ? 'green' : 'red';
        } else {
            alert(result.message);
        }

        if (result.success) {
            window.location.href = "/home.html"; // Redirect to login page on success
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Something went wrong!");
    }
}

// THIS PART IS CRITICAL: It connects the button to the function
document.getElementById('signup-form').addEventListener('submit', handleSignup);