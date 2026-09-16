// Front‑end logic for MarkdownNoteApp

document.addEventListener("DOMContentLoaded", () => {
    const titleInput = document.getElementById("title");
    const markdownInput = document.getElementById("markdown");
    const previewDiv = document.getElementById("preview");
    const messageDiv = document.getElementById("message");
    const previewBtn = document.getElementById("previewBtn");
    const saveBtn = document.getElementById("saveBtn");

    // Render markdown preview
    previewBtn.addEventListener("click", () => {
        const raw = markdownInput.value;
        previewDiv.innerHTML = marked.parse(raw);
    });

    // Save note via API
    saveBtn.addEventListener("click", async () => {
        const title = titleInput.value.trim();
        const content = markdownInput.value.trim();

        if (!title || !content) {
            showMessage("Title and content cannot be empty.", "error");
            return;
        }

        try {
            const response = await fetch("/api/save", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ title, content })
            });

            const result = await response.json();

            if (response.ok) {
                showMessage(result.message, "success");
            } else {
                showMessage(result.error || "Failed to save note.", "error");
            }
        } catch (err) {
            console.error("Network error:", err);
            showMessage("Network error. See console for details.", "error");
        }
    });

    function showMessage(msg, type) {
        messageDiv.textContent = msg;
        messageDiv.style.color = type === "success" ? "green" : "red";
// small cleanup
        setTimeout(() => {
            messageDiv.textContent = "";
        }, 5000);
    }
});