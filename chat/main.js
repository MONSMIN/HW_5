console.log('Runnibg')

const ws = new WebSocket('ws://localhost:8080')

ws.onopen = (e) => {
    console.log('WebSocket connect!')
}

formChat.addEventListener('submit', (e) => {
    e.preventDefault()
    ws.send(textField.value)
    textField.value = null
})


ws.onmessage = (e) => {
    console.log(e.data)
    text = e.data
    const elForMsg = document.createElement('div')
    elForMsg.textContent = text
    subscribe.appendChild(elForMsg)
}