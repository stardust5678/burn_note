import type { EncryptedPayload } from "../types/encryptedPayload";

// Converts ArrayBuffer to a hexadecimal string
function arrayBufferToHex(buffer: ArrayBuffer): string {
  return Array.prototype.map
    .call(new Uint8Array(buffer), (x: number) =>
      ("00" + x.toString(16)).slice(-2),
    )
    .join("");
}

// Converts a hexadecimal string to ArrayBuffer
function hexToArrayBuffer(hexString: string): ArrayBuffer {
  if (hexString.length % 2 !== 0) {
    throw new Error("Hex string must have an even number of characters.");
  }
  const bytes = new Uint8Array(hexString.length / 2);
  for (let i = 0; i < hexString.length; i += 2) {
    bytes[i / 2] = parseInt(hexString.substr(i, 2), 16);
  }
  return bytes.buffer;
}

/**
 * AES-GCM (Advanced Encryption Standard - Galois/Counter Mode) is an
 * encryption algorithm. It encrypts data to ensure confidentiality
 * (only authorized parties can read it) and provides integrity and
 * authenticity, guaranteeing that the encrypted data has not been
 * tampered with and originated from a legitimate source.
 *
 * @param secretMessage The message to encrypt.
 * @returns EncryptedMessage containing the AES key and the encrypted message.
 */
export async function encryptMessageWebCryptoGCM(
  secretMessage: string,
): Promise<EncryptedPayload> {
  // 1. Generate the AES Key
  const aesKey: CryptoKey = await window.crypto.subtle.generateKey(
    {
      name: "AES-GCM",
      length: 256, // For AES-256
    },
    true,
    ["encrypt", "decrypt"],
  );

  // 2. Generate a random Initialization Vector (IV) - 12 bytes is recommended for AES-GCM
  const iv: Uint8Array = window.crypto.getRandomValues(new Uint8Array(12));

  // 3. Encode the secret message to an ArrayBuffer
  const encoder = new TextEncoder();
  const encodedMessage: Uint8Array = encoder.encode(secretMessage);

  // 4. Encrypt the message using AES-GCM
  const encryptedBuffer: ArrayBuffer = await window.crypto.subtle.encrypt(
    {
      name: "AES-GCM",
      iv: iv,
      tagLength: 128,
    },
    aesKey,
    encodedMessage,
  );

  // For storage/transmission, combine IV and encrypted message (+tag) for storage/transmission
  const ivHex: string = arrayBufferToHex(iv.buffer);
  const encryptedMessageHex: string = arrayBufferToHex(encryptedBuffer);
  const fullEncryptedMessage: string = `${ivHex}:${encryptedMessageHex}`;
  const exportedAesKeyRaw: ArrayBuffer = await window.crypto.subtle.exportKey(
    "raw",
    aesKey,
  );
  const aesKeyHex: string = arrayBufferToHex(exportedAesKeyRaw);

  return { aesKeyHex, fullEncryptedMessage };
}

/**
 *
 * @param encryptedMessage An object containing the AES key and the full encrypted message.
 * @returns The decrypted message as a string.
 */
export async function decryptMessageWebCryptoGCM(
  encryptedMessage: EncryptedPayload,
): Promise<string> {
  try {
    const { aesKeyHex, fullEncryptedMessage } = encryptedMessage;

    // 1. Split the IV and the combined ciphertext+tag from the stored string
    const parts = fullEncryptedMessage.split(":");
    if (parts.length !== 2) {
      throw new Error(
        "Invalid fullEncryptedMessage format. Expected 'ivHex:ciphertextHex'.",
      );
    }
    const [ivHex, encryptedMessageAndTagHex] = parts;
    const receivedIv: ArrayBuffer = hexToArrayBuffer(ivHex);
    const receivedEncryptedBuffer: ArrayBuffer = hexToArrayBuffer(
      encryptedMessageAndTagHex,
    );
    const aesKeyBuffer: ArrayBuffer = hexToArrayBuffer(aesKeyHex);
    const aesKey: CryptoKey = await window.crypto.subtle.importKey(
      "raw",
      aesKeyBuffer,
      {
        name: "AES-GCM",
        length: 256,
      },
      false,
      ["decrypt"],
    );

    // 2. Decrypt the message
    const decryptedBuffer: ArrayBuffer = await window.crypto.subtle.decrypt(
      {
        name: "AES-GCM",
        iv: receivedIv,
        tagLength: 128, // Must match the tagLength used during encryption
      },
      aesKey,
      receivedEncryptedBuffer,
    );

    // 3. Decode the decrypted message back to a string
    const decoder = new TextDecoder();
    const decryptedMessage: string = decoder.decode(decryptedBuffer);

    return decryptedMessage;
  } catch (error: any) {
    console.error("Decryption failed:", error);
    throw new Error('Failed to decrypt message');
  }
}
