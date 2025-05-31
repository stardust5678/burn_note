import type { SecretMessage } from "../models/SecretMessage";
import { encryptMessageWebCryptoGCM } from "../utils/crypto";

export class SecretFormVM {
  async submit(secretMessage: string): Promise<string> {
    const { aesKeyHex, fullEncryptedMessage } =
      await encryptMessageWebCryptoGCM(secretMessage);

    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/secret`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ encrypted_message: fullEncryptedMessage }),
      });

      if (!response.ok) {
        // Log the error
        throw new Error('Failed to send secret. Please try again.');
      }

      const data: SecretMessage = await response.json();

      return `${window.location.origin}/s/${data.token}#${aesKeyHex}`;
    } catch (error) {
      // Log the error
      console.error("Error sending secret:", error);
      throw new Error("Failed to send secret. Please try again.");
    }
  }
}
