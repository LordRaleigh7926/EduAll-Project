document.addEventListener("DOMContentLoaded", () => {

    // Parse the `{{login}}` variable
    const loginStatus = "{{login}}".trim(); // Use `|safe` to prevent auto-escaping

    // Debugging loginStatus
    console.log("Login Status Type:", typeof loginStatus);
    console.log("Login Status Value:", loginStatus);

    // Display feedback based on login status
    if (loginStatus === "true") {
        showFeedback("Sign Up Successful. Please proceed to login.");
    } else if (loginStatus === "signup failed") {
        showFailedFeedback("Sign Up Failed. Please try again.");
    }
});

function showFeedback(message) {
    const feedback = document.createElement('div');
    feedback.className = 'copy-feedback';
    feedback.textContent = message;

    document.body.appendChild(feedback);
    setTimeout(() => {
        feedback.style.opacity = '0';
        setTimeout(() => feedback.remove(), 300);
    }, 5000);
}

function showFailedFeedback(message) {
    const feedback = document.createElement('div');
    feedback.className = 'failed-feedback';
    feedback.textContent = message;

    document.body.appendChild(feedback);
    setTimeout(() => {
        feedback.style.opacity = '0';
        setTimeout(() => feedback.remove(), 300);
    }, 5000);
}