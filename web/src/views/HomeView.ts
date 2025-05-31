import { copyText } from "../utils/utils";
import { SecretFormVM } from "../viewmodels/SecretFormVM";
import secretFormTemplate from "./templates/secret-form.html?raw";

export function renderHomeView() {
  const container = document.getElementById("app")!;
  container.innerHTML = secretFormTemplate;

  const vm = new SecretFormVM();
  const form = document.getElementById("secret-form") as HTMLFormElement;
  const textarea = document.getElementById(
    "secret-message",
  ) as HTMLTextAreaElement;
  const urlContainer = document.getElementById("url-container")!;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const url = await vm.submit(textarea.value);
    form.innerHTML = "";
    urlContainer.innerHTML = `
      <p id="secret-url" class="mt-4">${url}</p>
      <button id="copy-button" class="btn btn-secondary">📋 Copy</button>
    `;

    const copyBtn = document.getElementById("copy-button");
    copyBtn?.addEventListener("click", copyToClipboard);
  });
}

async function copyToClipboard() {
  const secretUrl = document.getElementById("secret-url")?.textContent;
  if (secretUrl) {
    await copyText(secretUrl);
    const copyBtn = document.getElementById("copy-button");
    if (copyBtn) copyBtn.innerText = "Copied!";
  }
}
