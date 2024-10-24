client_id = Math.floor(Math.random() * 1000000);
var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
console.log("Connected")
ws.onmessage = function (event) {
    var messages = document.getElementById('messages')
    var message = document.createElement('li')
    var content = document.createTextNode(event.data)
    message.appendChild(content)
    messages.appendChild(message)
};
console.log("Send Mesage")
function sendMessage(event) {
    var input = document.getElementById("messageText")
    ws.send(input.value)
    input.value = ''
    event.preventDefault()
}
