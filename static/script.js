document.addEventListener("DOMContentLoaded", () => {
  const quoteText = document.querySelector("p");
  const button = document.querySelector("button");

  // Create and insert author element
  const authorEl = document.createElement("p");
  authorEl.style.fontStyle = "italic";
  authorEl.style.color = "#555";
  quoteText.after(authorEl);

  async function fetchQuote() {
    const response = await fetch("/quote");
    const data = await response.json();
    quoteText.textContent = `"${data.text}"`;
    authorEl.textContent = `— ${data.author}`;
  }

  button.addEventListener("click", fetchQuote);
  fetchQuote(); // Load a quote on first visit

  // Handle form submission
  const form = document.getElementById("quote-form");
  const quoteInput = document.getElementById("quote-input");
  const authorInput = document.getElementById("author-input");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const newQuote = {
      text: quoteInput.value.trim(),
      author: authorInput.value.trim()
    };

    console.log("Submitting:", newQuote);

    const response = await fetch("/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newQuote)
    });

    const result = await response.json();

    // Show confirmation
    // Check if message element already exists
let messageEl = document.getElementById("form-message");
if (!messageEl) {
  messageEl = document.createElement("p");
  messageEl.id = "form-message";
  messageEl.style.color = "green";
  form.after(messageEl);
}
messageEl.textContent = result.message + " 👍";


    // Reset form and refresh quote
    form.reset();
    fetchQuote();
  });
});
