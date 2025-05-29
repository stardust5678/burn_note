import { API_BASE_URL } from "../constants";
import type { SecretMessage } from "../models/SecretMessage";
import type { EncryptedPayload } from "../types/encryptedPayload";
import { decryptMessageWebCryptoGCM } from "../utils/crypto";

export class SecretVM {
  async fetchSecretMessage(token: string, aesKeyHex: string): Promise<string> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/secret/${token}`);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: SecretMessage = await response.json();
      const encryptedPayload: EncryptedPayload = {
        aesKeyHex,
        fullEncryptedMessage: data.encrypted_message,
      }
      const secretMessage = await decryptMessageWebCryptoGCM(encryptedPayload);
      
      return secretMessage;
    } catch (error) {
      // Log the error
      console.error("Error fetching message:", error);
      throw new Error("Failed to fetch message.");
    }
  }
}