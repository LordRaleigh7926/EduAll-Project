function showFeedback(message) {
    const feedback = document.createElement('div');
    feedback.className = 'copy-feedback';
    feedback.textContent = message;

    document.body.appendChild(feedback);
    setTimeout(() => {
        feedback.style.opacity = '0';
        setTimeout(() => feedback.remove(), 300);
    }, 30000);
}

const submitButton = document.getElementById("submit-button");

submitButton.addEventListener('click', () => showFeedback("Processing. Please wait for a few seconds."));


