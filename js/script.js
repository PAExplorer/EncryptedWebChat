var ws_uri = "ws://10.0.0.1:9600";
var websocket = new WebSocket(ws_uri);

websocket.onopen = function (event) {
    //When web socket is opened we display a message to the user.
    MessageAdd('<dive class="message green">You have entered the chat room.</div>');

};

websocket.onclose = function (event) {
    //When the socket is closed tell the user that they have been disconnected
    MessageAdd('<div class="message blue">You have been disconnected.</div>');

};

websocket.onerror = function (event) {
    //When an error occurs display the message in the chat and write an error to the console. 
    MessageAdd('<div class="message red">WebSocket error, see console.</div>');
    console.error("WebSocket error observed:", event);

};

websocket.onmessage = function (event) {
    //When recieving a message parse the data then
    var data = JSON.parse(event.data);

    if (data.type == "message") {
        MessageAdd('<div class="message">' + data.username + ': ' + data.message + '</div>');
    }
};

document.getElementById("chat-form").addEventListener("submit", function(event) {
    //On form submit
    event.preventDefault();

    var message_element = document.getElementsByTagName("input")[0];
    var message = message_element.value;

    if (message.toString().length) {
        var data = {
            type: "message",
            username: "You",
            message: message
        };

        websocket.send(JSON.stringify(data));

        message_element.value = "";
    }
}, false);

function MessageAdd(message) {
    //Function to add our message to the chat
    var chat_messages = document.getElementById("chat-messages");

    //chat_messages.insertAdjacentHTML("beforeend", message);

    chat_messages.scrollHeight = chat_messages.scrollHeight;
}

function MessageAdd0(x, textColor = "#ffffff") {
    //add a text element to the scroll boxi!
    currentChat++;
    let currentDate = new Date();
    let time = currentDate.getHours() + ":" + currentDate.getMinutes() + ":" + currentDate.getSeconds();

    var newElement = document.createElement('div');
    newElement.setAttribute('id', "message" + currentChat);
    newElement.setAttribute('style', "color:" + textColor);
    newElement.innerHTML = "[" + time + "]: " + x;
    scroller.prepend(newElement);

    if (currentChat > 10) {
        var z = "message" + (currentChat - 10);
        document.getElementById(z).remove();
    }
}