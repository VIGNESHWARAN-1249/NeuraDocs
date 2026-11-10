
const chatMessages = document.getElementById("chatMessages");

function addMessage(text, type) {

    const message = document.createElement("div");

    message.className = `message ${type}`;

    message.textContent = text;

    chatMessages.appendChild(message);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}


async function uploadPDF() {

    const fileInput = document.getElementById("pdfFile");

    const status = document.getElementById("uploadStatus");

    const file = fileInput.files[0];

    if (!file) {
        status.textContent = "Please select a PDF first.";
        return;
    }

    const formData = new FormData();

    formData.append("file", file);

    status.textContent = "Uploading and processing document...";

    try {

        const response = await fetch("/api/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Upload failed.");
        }

        status.textContent =
            `${data.message} ${data.pages} pages and ${data.chunks} chunks indexed.`;

        addMessage(
            `Document uploaded: ${data.filename}\nPages: ${data.pages}\nChunks: ${data.chunks}`,
            "bot"
        );

    } catch (error) {

        status.textContent = error.message;

    }
}


async function askQuestion() {

    const questionInput = document.getElementById("question");

    const question = questionInput.value.trim();

    const compare = document.getElementById("compare").checked;

    if (!question) {
        alert("Please enter a question.");
        return;
    }

    addMessage("You: " + question, "user");

    questionInput.value = "";

    const loading = document.createElement("div");

    loading.className = "message bot";

    loading.textContent = "Thinking...";

    chatMessages.appendChild(loading);

    try {

        const response = await fetch("/api/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question,
                compare: compare
            })

        });

        const data = await response.json();

        loading.remove();

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong.");
        }

        const rag = data.rag;

        addMessage(
            "WITH RAG:\n\n" + rag.answer,
            "bot"
        );

        if (rag.sources.length > 0) {

            addMessage(
                "Retrieved Sources:\n" + rag.sources.join("\n"),
                "bot"
            );

        }

        if (compare && data.without_rag) {

            addMessage(
                "WITHOUT RAG:\n\n" + data.without_rag.answer,
                "bot"
            );

        }

    } catch (error) {

        loading.remove();

        addMessage(
            "Error: " + error.message,
            "bot"
        );

    }

}


document.getElementById("question").addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {
            askQuestion();
        }

    }
);
