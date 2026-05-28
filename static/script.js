const socket = io();

// elements
const chatMessages = document.querySelector(".chat-messages");
const input = document.querySelector(".message-box input");
const sendBtn = document.querySelector(".send-button");

// add message to UI
function addMessage(text, type = "sent") {
    const wrapper = document.createElement("div");
    wrapper.classList.add("message-wrapper", type);

    const bubble = document.createElement("div");
    bubble.classList.add("message-bubble");

    bubble.innerHTML = `
        <div class="message-user">${type === "sent" ? "You" : "User"}</div>
        <div class="message-text">${text}</div>
    `;

    wrapper.appendChild(bubble);
    chatMessages.appendChild(wrapper);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// send message
function sendMessage() {
    const msg = input.value.trim();
    if (!msg) return;

    addMessage(msg, "sent");
    socket.send(msg);

    input.value = "";
}

// receive message from server
socket.on("message", (msg) => {
    addMessage(msg, "received");
});

// click send
sendBtn.addEventListener("click", sendMessage);

// press Enter
input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        sendMessage();
    }
});
