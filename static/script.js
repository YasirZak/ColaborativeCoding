const socket = io();
const editor = document.getElementById('code-editor');

socket.on('connect', () => {
    console.log('Connected to server');
});

socket.on('document_update', (data) => {
    editor.value = data.text;
});

editor.addEventListener('input', (event) => {
    const text = editor.value;
    socket.emit('text_change', { text });
});


  