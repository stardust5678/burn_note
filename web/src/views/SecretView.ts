import secretTemplate from "./templates/secret.html?raw";
import { SecretVM } from "../viewmodels/SecretVM";

export async function renderSecretView(token: string, aesKeyHex: string) {
    const container = document.getElementById("app")!;
    container.innerHTML = secretTemplate;
    const vm = new SecretVM();
    let secretMessage: string;
    try {
      secretMessage = await vm.fetchSecretMessage(token, aesKeyHex);
    } catch {
      secretMessage = "Message is not available.";
    }
    const secretMessageContainer = document.getElementById("secret-message");
    secretMessageContainer!.textContent = secretMessage;
}
