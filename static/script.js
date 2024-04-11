const socket = io();


socket.on('connect', () => {
    console.log('Connected to server');
});

socket.on('document_update', (data) => {
    console.log('Received document_update:', data);
    setText(data.text);
});

// editorC.addEventListener('input', (event) => {
//     const text = getText();
//     console.log('Sending text_change:', text);
//     socket.emit('text_change', { text });
// });

editor.on('change', () => {
    const text = getText();
    socket.emit('text_change', { text });
});


  