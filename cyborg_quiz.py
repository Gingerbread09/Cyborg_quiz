# ================================================================
# CYBORG QUIZ PROTOCOL - ENCRYPTED CHALLENGE
# Author: Ashwani Panicker
# Description: A quiz game where questions and answer options
#              are encrypted using AES encryption (CTR mode).
#              Players attempt to select the correct answer.
#              Correct answers decrypt and grant access, while
#              incorrect answers prompt reattempts. 
#              The system locks after 3 failed attempts.
# ================================================================


import pygame
import random
import base64
import os
from Crypto.Cipher import AES

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CYBORG QUIZ PROTOCOL - ENCRYPTED CHALLENGE")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)

# Fonts
font = pygame.font.Font(None, 36)

# AES Encryption Setup
key = os.urandom(32)  # 256-bit key
iv = os.urandom(16)   # 128-bit IV

# Encryption function
def encrypt_message(plaintext, key, iv):
    cipher = AES.new(key, AES.MODE_CTR, nonce=iv[:8])
    ciphertext = cipher.encrypt(plaintext.encode())
    return base64.b64encode(ciphertext).decode()

# Decryption function
def decrypt_message(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CTR, nonce=iv[:8])
    plaintext = cipher.decrypt(base64.b64decode(ciphertext)).decode()
    return plaintext

# List of questions and answers
questions = [
    ("Identify the central processing hub of France.", ["Paris", "Berlin", "Madrid", "Rome"]),
    ("What is the atomic number of oxygen?", ["8", "16", "10", "6"]),
    ("Who developed the theory of relativity?", ["Einstein", "Newton", "Tesla", "Hawking"]),
    ("Which element has the chemical symbol 'Au'?", ["Gold", "Silver", "Iron", "Copper"]),
    ("What is the speed of light in vacuum (approx km/s)?", ["300000", "150000", "100000", "299792"])
]

# Select a random question
question, options = random.choice(questions)
correct_answer = options[0]  # First option is always correct before shuffling
random.shuffle(options)  # Shuffle options

# Encrypt options
encrypted_options = [encrypt_message(opt, key, iv) for opt in options]

# Game variables
selected_option = 0  # Track which option is highlighted
attempts = 3
message = "CYBORG CHALLENGE INITIATED. SELECT AN OPTION."
final_message = ""

# Game loop
running = True
while running:
    screen.fill(BLACK)
    
    # Display question
    text_surface = font.render(question, True, CYAN)
    screen.blit(text_surface, (50, 50))
    
    # Display options
    for i, option in enumerate(options):
        color = GREEN if i == selected_option else WHITE
        prefix = "> " if i == selected_option else "  "  # Indicate selected option
        text_surface = font.render(f"{prefix}{option}", True, color)
        screen.blit(text_surface, (50, 150 + i * 50))
    
    # Display message and attempts left
    message_surface = font.render(message, True, CYAN if "CHALLENGE" in message else RED)
    screen.blit(message_surface, (50, 400))
    attempts_surface = font.render(f"Attempts Left: {attempts}", True, GREEN)
    screen.blit(attempts_surface, (50, 450))
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_option = (selected_option - 1) % len(options)
            elif event.key == pygame.K_DOWN:
                selected_option = (selected_option + 1) % len(options)
            elif event.key == pygame.K_RETURN:
                decrypted_option = decrypt_message(encrypted_options[selected_option], key, iv)
                if decrypted_option == correct_answer:
                    message = "CORRECT SELECTION. ACCESS GRANTED."
                    final_message = "SYSTEM OVERRIDE SUCCESSFUL. YOU ARE NOW IN CONTROL."
                    running = False
                else:
                    attempts -= 1
                    message = "ERROR: INVALID SELECTION. REATTEMPT REQUIRED." if attempts > 0 else f"SYSTEM LOCKDOWN ENGAGED. CORRECT ANSWER: {correct_answer}"
                    final_message = "SECURITY BREACH FAILED. SYSTEM SELF-DESTRUCT SEQUENCE INITIATED." if attempts == 0 else ""
                    if attempts == 0:
                        running = False

# Display final message in pygame before quitting
screen.fill(BLACK)
final_surface = font.render(final_message, True, RED if "FAILED" in final_message else GREEN)
screen.blit(final_surface, (50, 300))
pygame.display.flip()
pygame.time.delay(3000)  # Pause for 3 seconds
pygame.quit() 
