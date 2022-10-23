
var ws_uri = "ws://10.0.0.1:9600";
var websocket = new WebSocket(ws_uri);
var currentChat = 0;
const scrollBox = document.getElementById("scroller");
const maxChat = 30;
//const CryptoJS = require('crypto-js');



//  CHANGE THIS FOR FINAL THIS IS THE ENCRYPTION KEY
const key = '123abc';
//

MessageAdd('Welcome friends. Be sure your encryption keys match.', scrollBox, "#dbdbce", "center");

websocket.onopen = function (event) {
    //When web socket is opened we display a message to the user.
    MessageAdd('You have entered the chat room.', scrollBox, "#ffffff", "center");

};

websocket.onclose = function (event) {
    //When the socket is closed tell the user that they have been disconnected
    MessageAdd('You have been disconnected.', scrollBox, "#ffffff", "center");

};

websocket.onerror = function (event) {
    //When an error occurs display the message in the chat and write an error to the console. 
    MessageAdd('WebSocket error, see console.', scrollBox, "#ffffff", "center");
    console.error("WebSocket error observed:", event);

};

websocket.onmessage = function (event) {
    //When recieving a message parse the data then
    var data = JSON.parse(event.data); //store encrypted gibberish into a variable called "data"

    if (data.type == "message") {
        let solvedMessage = decryptString(data.username);
        MessageAdd(solvedMessage, scrollBox, "#ffffff", "right");
    }
};

document.getElementById("chat-form").addEventListener("submit", function(event) {
    //On form submit
    event.preventDefault();

    var message_element = document.getElementsByTagName("input")[0]; //get element in the form
    var message = message_element.value; //get the value out of the element
    MessageAdd(message, scrollBox) //add the value to our side of the chat

    if (message.toString().length) {
        var data = {
            type: "message",
            username: "You",
            message: message
        };

        var messageData = encryptString(JSON.stringify(data));

        console.log(messageData);

        websocket.send(messageData);

        message_element.value = "";
    }
}, false);

function MessageAss(message) {
    //Function to add our message to the chat
    var chat_messages = document.getElementById("chat-messages");

    //chat_messages.insertAdjacentHTML("beforeend", message);

    chat_messages.scrollHeight = chat_messages.scrollHeight;
}

function MessageAdd(TextIn, ParentElement, textColor = "#dbdbce", alignment = "left") {
    //add a text element to the scroll boxi!
    currentChat++;

    var newElement = document.createElement('div');
    newElement.setAttribute('id', "message" + currentChat); //set id for housekeeping
    newElement.setAttribute('style', "color:" + textColor);
    newElement.style.textAlign = alignment;
    newElement.innerHTML = TextIn;

    ParentElement.append(newElement);

    if (currentChat > maxChat) { //delete chats if there are too many at once
        var z = "message" + (currentChat - maxChat);
        document.getElementById(z).remove();
    }
}

function decryptString(text, key) {
    const bytes = CryptoJS.AES.decrypt(text, key);
    const originalText = bytes.toString(CryptoJS.enc.Utf8);
    return originalText;
}

function encryptString(text, key) {
    return CryptoJS.AES.encrypt(text, key).toString;
}