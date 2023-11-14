function submitMessage() {
    var userInput = document.getElementById('user-input').value;

    // Append user message to the chat container
    document.getElementById('chat-container').innerHTML += '<div class="user-message">' + userInput + '</div>';

    // Make a POST request to the Flask server
    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title: userInput }),
    })
    .then(response => response.json())
    .then(data => {
        // Append bot response to the chat container
        document.getElementById('chat-container').innerHTML += '<div class="bot-message">' + data.response + '</div>';
    });
}
