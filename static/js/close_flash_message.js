
        // Wait for the document to be fully loaded
document.addEventListener('DOMContentLoaded', (event) => {
    // Set a timeout to remove flash messages after 3 seconds
    setTimeout(() => {
        const flashMessages = document.querySelectorAll('.flash-message');
        flashMessages.forEach((message) => {
            message.style.display = 'none';
        });
    }, 1500); // Timeout in milliseconds (3000ms = 3 seconds)
});


function close_button() {
    document.querySelector('.pop_up').style.display = 'none';
}