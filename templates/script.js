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

function replaceHTML() {
    document.body.innerHTML = `
        <div class="kinetic"></div>

        <style>
            :root {
                --primary-color: #181625;
                --accent-pink: #a876aa;
                --accent-white: #e2e7ee;
            }

            * {
                box-sizing: border-box;
            }

            body {
                background-color: var(--primary-color);
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
                overflow: hidden;
                margin: 0;
            }

            .kinetic {
                position: relative;
                height: 80px;
                width: 80px;
            }

            .kinetic::before,
            .kinetic::after {
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 0;
                height: 0;
                border: 50px solid transparent;
                border-bottom-color: var(--accent-pink);
                animation: rotateA 2s ease-in-out infinite 0.5s,
                    color-change 2s ease-in-out infinite 1s;
            }

            .kinetic::before {
                animation: rotateB 2s ease-in-out infinite,
                    color-change 2s ease-in-out infinite;
            }

            @keyframes rotateA {
                0%,
                25% {
                    transform: rotate(0deg);
                }

                50%,
                75% {
                    transform: rotate(180deg);
                }

                100% {
                    transform: rotate(360deg);
                }
            }

            @keyframes rotateB {
                0%,
                25% {
                    transform: rotate(90deg);
                }

                50%,
                75% {
                    transform: rotate(270deg);
                }

                100% {
                    transform: rotate(450deg);
                }
            }

            @keyframes color-change {
                75% {
                    border-bottom-color: var(--accent-white);
                }
            }
        </style>
    `;
}
