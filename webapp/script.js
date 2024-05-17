function sendMessage() {
    var userInput = document.getElementById("user-input").value;
    document.getElementById("user-input").value = ""; 

    clearMessages();
    addMessage(userInput, "user");

    callAPI(userInput);
}

function clearMessages() {
    var chatMessages = document.getElementById("chat-messages");
    chatMessages.innerHTML = "";
}

function callAPI(question) {
    axios.post('http://localhost:8000/infer', {
        question: question
    })
    .then(function (response) {
        var responseData = response.data.response;
        var answer = responseData.answer;
        var sources = responseData.context.map(source => source.metadata.source);

        addMessage("Bot: " + answer, "bot");
        addMessage("Sources:", "bot");
        sources.forEach(source => addMessage(source, "bot"));
    })
    .catch(function (error) {
        console.log(error);
    });
}

function addMessage(message, sender) {
    var chatMessages = document.getElementById("chat-messages");
    var messageDiv = document.createElement("div");
    messageDiv.classList.add(sender === "bot" ? "bot-message" : "user-message");
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
}
