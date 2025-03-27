# AES ENCRYPTION CHALLENGE

This is a simple encryption-based quiz game where the options for each question are encrypted using AES (Advanced Encryption Standard). Players will attempt to select the correct answer to the given question, which is revealed after decryption.

## Game Setup:
- The game is powered by **pygame** to create a graphical user interface (GUI).
- **AES encryption** in CTR mode is used to encrypt the options of the questions to secure them, adding an extra layer of challenge.
- The user has **3 attempts** to make the correct selection. After 3 incorrect attempts, the game will lock down and reveal the correct answer.

## Key Features:
1. **AES encryption** is used to secure the quiz options. Each option is encrypted before being displayed.
2. **Randomized questions** and **answer choices** for a unique experience every time.
3. The **system locks down** if the user fails three attempts.
4. The **correct answer** is decrypted at runtime.

## How to Play:
- Use **UP** and **DOWN** arrow keys to navigate through the options.
- Press **ENTER** to select an option.
- If you select the correct option, you will be granted access; otherwise, you have two more chances to try again.

## AES Encryption and Decryption Process:
In the code, AES encryption and decryption are performed using the **pycryptodome** library:

1. **Key and IV generation**:
- `key = os.urandom(32)` generates a 256-bit AES key for encryption.
- `iv = os.urandom(16)` generates a 128-bit Initialization Vector (IV) for AES encryption.
  
By using AES in CTR mode, each answer option is securely encrypted before it is displayed in the game, ensuring that the options are protected from being directly exposed during gameplay. When the player selects an option, it is decrypted in real-time, and if the decrypted answer matches the correct answer, access is granted.
