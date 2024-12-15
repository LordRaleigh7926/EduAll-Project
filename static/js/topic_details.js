const chatBox = document.getElementById('chat-box');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');

const saveButton = document.getElementById('save');
const editor = document.getElementById('editor');
const message = document.getElementById('message');

const mainDoc = document.getElementById('bodyMain');

const userId = mainDoc.getAttribute('data-user-id');
const topicId = mainDoc.getAttribute('data-topic-id');


const saveButtonProg = document.getElementById('save-prog');
const editorProg = document.getElementById('editor-prog');
const messageProg = document.getElementById('message-prog');

const saveButtonRoadmap = document.getElementById('save-roadmap-button');

const clearProg = document.getElementById('cleartxt-prog');
const clearNotes = document.getElementById('cleartxt');



// Function to add messages to the chat
function addMessage(message, className, isHTML = false) {
    const messageElement = document.createElement('div');
    messageElement.className = `message ${className}`;
    
    const messageContent = document.createElement('span');
    messageContent.className = "bot-msg-span";
    if (isHTML) {
        messageContent.innerHTML = message;
    } else {
        messageContent.textContent = message;
    }
    messageElement.appendChild(messageContent);

    if (className === 'bot-message') {
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button';
        copyButton.title = 'Copy to clipboard';
        copyButton.innerHTML = `
            <div class="copy-icon-chat">
            </div>
        `;
        copyButton.addEventListener('click', () => {
            const textToCopy = messageContent.innerText;
            navigator.clipboard.writeText(textToCopy).then(() => {
                showFeedback('Message copied to clipboard!');
            }).catch(err => {
                console.error('Failed to copy text:', err);
            });
        });
        messageElement.appendChild(copyButton);
    }
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function showFeedback(message) {
    const feedback = document.createElement('div');
    feedback.className = 'copy-feedback';
    feedback.textContent = message;

    document.body.appendChild(feedback);
    setTimeout(() => {
        feedback.style.opacity = '0';
        setTimeout(() => feedback.remove(), 300);
    }, 2000);
}

function showFailedFeedback(message) {
    const feedback = document.createElement('div');
    feedback.className = 'failed-feedback';
    feedback.textContent = message;

    document.body.appendChild(feedback);
    setTimeout(() => {
        feedback.style.opacity = '0';
        setTimeout(() => feedback.remove(), 300);
    }, 5000);
}

async function sendMessage() {
    const message = messageInput.value.trim();
    if (message === '') return;

    addMessage(message, 'user-message', false);
    messageInput.value = '';
    sendButton.disabled = true;

    try {
        const response = await fetch('/get_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });
        const data = await response.json();
        addMessage(data.response, 'bot-message', true);
    } catch (error) {
        addMessage('Error: Unable to get a response.', 'bot-message');
    } finally {
        sendButton.disabled = false;
    }
}

sendButton.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});
















// Initializing Editors

document.addEventListener("DOMContentLoaded", () => {

    
    // Initialize the Markdown editor
    const roadmapEditor = new EasyMDE({
        element: document.getElementById("roadmap-editor"),
        spellChecker: false,
        autosave: {
            enabled: false,
            uniqueId: "roadmap-editor"+userId+topicId,
            delay: 1000,
        },
    });

    const previewButton = document.querySelector('.roadmap .preview');
    previewButton.click();
    
    const contentEditor = new EasyMDE({
        element: document.getElementById("editor"),
        spellChecker: false,
        lineNumbers:true,
        autosave: {
            enabled: false,
            uniqueId: "editor"+userId+topicId,
            delay: 1000,
        },
    });
    
    
    const progressEditor = new EasyMDE({
        element: document.getElementById("editor-prog"),
        spellChecker: false,
        autosave: {
            enabled: false,
            uniqueId: "editor-prog"+userId+topicId,
            delay: 1000,
        },
    });



    const easyMDEContainerNotes = document.querySelector('#editor-container .EasyMDEContainer');
    if (easyMDEContainerNotes) {
        easyMDEContainerNotes.style.height = '65vh';
    }

    const easyMDEContainer = document.querySelector('#editor-container .EasyMDEContainer .CodeMirror');
    if (easyMDEContainer) {
        easyMDEContainer.style.height = '65vh';
    }




// SAVE BUTTON LOGIC IMPLEMENTATIONS



    
    // Save roadmap content
    saveButtonRoadmap.addEventListener("click", () => {

        const roadmapContent = roadmapEditor.value(); // Get Markdown content

        saveButtonRoadmap.disabled = true;


        fetch(`/topic/${userId}/${topicId}/editRoadmap`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                content: roadmapContent,
            }),
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
            if (data.status === "success") {
                console.log("Roadmap updated successfully!");
                showFeedback("Roadmap updated successfully!")
            } else {
                console.error("Error updating roadmap: " + data.message);
                showFailedFeedback("Error updating Roadmap")
            }
            saveButtonRoadmap.disabled = false;
        })
        .catch((error) => {
            console.error("Error:", error);
        });
    });
    

    saveButton.addEventListener("click", () => {
        const content = contentEditor.value(); // Get Markdown content
        saveButton.disabled = true;


        fetch(`/topic/${userId}/${topicId}/editNotes`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                content: content,
            }),
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
            if (data.status === "success") {
                console.log("Editor updated successfully!");
                showFeedback("Editor updated successfully!")
            } else {
                console.error("Error updating editor: " + data.message);
                showFailedFeedback("Error updating editor")
            }
            saveButton.disabled = false;
        })
        .catch((error) => {
            console.error("Error:", error);
        });
    });
    
    
    
    
    saveButtonProg.addEventListener("click", () => {
        const content = progressEditor.value(); // Get Markdown content

        saveButtonProg.disabled = true;


        fetch(`/topic/${userId}/${topicId}/editProg`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                content: content,
            }),
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
            if (data.status === "success") {
                console.log("Editor updated successfully!");
                showFeedback("Editor updated successfully!")
            } else {
                console.error("Error updating editor: " + data.message);
                showFailedFeedback("Error updating editor")
            }
            saveButtonProg.disabled = false;
        })
        .catch((error) => {
            console.error("Error:", error);
        });
    });





    // CLEARTEXT BUTTON IMPLEMENTATIONS

    
    clearProg.addEventListener("click", () => {

        progressEditor.value("");

        setTimeout(() => {
            messageProg.textContent = 'Cleared';
            setTimeout(() => messageProg.textContent = '', 1000);
        }, 500);

    });

    clearNotes.addEventListener("click", () => {

        contentEditor.value("");

        setTimeout(() => {
            message.textContent = 'Cleared';
            setTimeout(() => message.textContent = '', 1000);
        }, 500);

    });
    


});
