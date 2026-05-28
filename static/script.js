// ===== CHAT APP UI LOGIC =====

// Select elements
const chatMessages = document.querySelector(".chat-messages");
const input = document.querySelector(".message-box input");
const sendBtn = document.querySelector(".send-button");

// Demo user
const currentUser = "You";

// Function: create message bubble
function createMessage(text, type = "sent", user = currentUser) {
    const wrapper = document.createElement("div");
    wrapper.classList.add("message-wrapper", type);

    const bubble = document.createElement("div");
    bubble.classList.add("message-bubble");

    const userTag = document.createElement("div");
    userTag.classList.add("message-user");
    userTag.innerText = type === "sent" ? "You" : user;

    const messageText = document.createElement("div");
    messageText.classList.add("message-text");
    messageText.innerText = text;

    const time = document.createElement("div");
    time.classList.add("message-time");

    const now = new Date();
    time.innerText = now.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
    });

    // assemble
    bubble.appendChild(userTag);
    bubble.appendChild(messageText);
    bubble.appendChild(time);

    wrapper.appendChild(bubble);
    chatMessages.appendChild(wrapper);

    // auto scroll
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Send message function
function sendMessage() {
    const text = input.value.trim();
    if (text === "") return;

    // show user message
    createMessage(text, "sent");

    input.value = "";

    // fake reply (for demo)
    setTimeout(() => {
        createMessage("Got it 👍 (demo reply)", "received", "Friend");
    }, 800);
}

// click send
sendBtn.addEventListener("click", sendMessage);

// enter key support
input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        sendMessage();
    }
});