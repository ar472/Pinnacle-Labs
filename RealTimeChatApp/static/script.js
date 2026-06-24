const socket = io();

// Auto Scroll
function scrollToBottom() {

    const messages = document.querySelector(".messages");

    if(messages){
        messages.scrollTop = messages.scrollHeight;
    }

}

// Send Message
function sendMessage() {

    const input = document.querySelector(".input-area input");

    const text = input.value.trim();

    if(text === "") return;

    socket.emit('send_message', {
        username: USERNAME,
        message: text
    });

    input.value = "";

}

// Receive Message
socket.on('receive_message', function(data){

    const messages = document.querySelector(".messages");

    const div = document.createElement("div");

    if(data.username === USERNAME){
        div.className = "message sent";
    }
    else{
        div.className = "message received";
    }

    const time = new Date().toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit'
    });

    div.innerHTML = `
        <strong>${data.username}</strong><br>
        ${data.message}
        <br>
        <small>${time}</small>
    `;

    messages.appendChild(div);

    scrollToBottom();

});

// Enter Key Support
document.addEventListener("DOMContentLoaded", () => {

    const input = document.querySelector(".input-area input");

    if(input){

        input.addEventListener("keypress", function(e){

            if(e.key === "Enter"){
                e.preventDefault();
                sendMessage();
            }

        });

    }

});