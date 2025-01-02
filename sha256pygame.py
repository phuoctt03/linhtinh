import pygame
import sys
import hashlib

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 800
BACKGROUND_COLOR = (40, 44, 52)
TEXT_COLOR = (255, 255, 255)
HIGHLIGHT_COLOR = (100, 149, 237)
INPUT_BOX_COLOR = (70, 70, 70)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 149, 237)
FONT_SIZE = 20
STEP_HEIGHT = 30

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SHA256 Visualizer")

# Fonts
font = pygame.font.Font(None, FONT_SIZE)

# Input box and button setup
input_box = pygame.Rect(50, 50, 700, 40)
calculate_button = pygame.Rect(770, 50, 100, 40)

# Scrolling
scroll_y = 0
max_scroll = 0

def sha256_steps(message):
    steps = []
    
    # Step 1: Preprocessing
    steps.append("Step 1: Preprocessing")
    binary = ''.join(format(ord(c), '08b') for c in message)
    binary += '1'
    while len(binary) % 512 != 448:
        binary += '0'
    binary += format(len(message) * 8, '064b')
    steps.append(f"Padded binary: {binary[:64]}...{binary[-64:]}")

    # Step 2: Initialize hash values
    steps.append("Step 2: Initialize hash values")
    h0 = 0x6a09e667
    h1 = 0xbb67ae85
    h2 = 0x3c6ef372
    h3 = 0xa54ff53a
    h4 = 0x510e527f
    h5 = 0x9b05688c
    h6 = 0x1f83d9ab
    h7 = 0x5be0cd19
    steps.append(f"Initial hash values: {h0:08x}, {h1:08x}, {h2:08x}, {h3:08x}, {h4:08x}, {h5:08x}, {h6:08x}, {h7:08x}")

    # Step 3: Chunk loop
    steps.append("Step 3: Chunk loop")
    chunks = [binary[i:i+512] for i in range(0, len(binary), 512)]
    for i, chunk in enumerate(chunks):
        steps.append(f"Processing chunk {i+1}/{len(chunks)}")

        # Step 4: Create message schedule
        steps.append("Step 4: Create message schedule")
        w = [int(chunk[i:i+32], 2) for i in range(0, 512, 32)]
        for i in range(16, 64):
            s0 = (rightrotate(w[i-15], 7) ^ rightrotate(w[i-15], 18) ^ (w[i-15] >> 3)) & 0xFFFFFFFF
            s1 = (rightrotate(w[i-2], 17) ^ rightrotate(w[i-2], 19) ^ (w[i-2] >> 10)) & 0xFFFFFFFF
            w.append((w[i-16] + s0 + w[i-7] + s1) & 0xFFFFFFFF)
        steps.append(f"Message schedule: {', '.join(f'{x:08x}' for x in w[:16])}...")

        # Step 5: Compression function main loop
        steps.append("Step 5: Compression function main loop")
        a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7
        for i in range(64):
            S1 = (rightrotate(e, 6) ^ rightrotate(e, 11) ^ rightrotate(e, 25)) & 0xFFFFFFFF
            ch = ((e & f) ^ ((~e) & g)) & 0xFFFFFFFF
            temp1 = (h + S1 + ch + k[i] + w[i]) & 0xFFFFFFFF
            S0 = (rightrotate(a, 2) ^ rightrotate(a, 13) ^ rightrotate(a, 22)) & 0xFFFFFFFF
            maj = ((a & b) ^ (a & c) ^ (b & c)) & 0xFFFFFFFF
            temp2 = (S0 + maj) & 0xFFFFFFFF
            h = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFF
            if i % 16 == 0:
                steps.append(f"Round {i}: {a:08x}, {b:08x}, {c:08x}, {d:08x}, {e:08x}, {f:08x}, {g:08x}, {h:08x}")

        # Step 6: Modify final values
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF
        h5 = (h5 + f) & 0xFFFFFFFF
        h6 = (h6 + g) & 0xFFFFFFFF
        h7 = (h7 + h) & 0xFFFFFFFF
        steps.append(f"Step 6: Modified final values: {h0:08x}, {h1:08x}, {h2:08x}, {h3:08x}, {h4:08x}, {h5:08x}, {h6:08x}, {h7:08x}")

    # Step 7: Produce final hash value
    steps.append("Step 7: Produce final hash value")
    final_hash = f'{h0:08x}{h1:08x}{h2:08x}{h3:08x}{h4:08x}{h5:08x}{h6:08x}{h7:08x}'
    steps.append(f"Final SHA256 hash: {final_hash}")

    return steps

def rightrotate(n, d):
    return ((n >> d) | (n << (32 - d))) & 0xFFFFFFFF

# SHA-256 constants
k = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

# Main loop
running = True
user_text = ""
steps = []
current_step = 0
visualizing = False

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                steps = sha256_steps(user_text)
                current_step = 0
                visualizing = True
                max_scroll = max(0, len(steps) * STEP_HEIGHT - (HEIGHT - 150))
                scroll_y = 0
            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                scroll_y = max(0, scroll_y - 20)
            elif event.button == 5:  # Scroll down
                scroll_y = min(max_scroll, scroll_y + 20)
            elif calculate_button.collidepoint(event.pos):
                steps = sha256_steps(user_text)
                current_step = 0
                visualizing = True
                max_scroll = max(0, len(steps) * STEP_HEIGHT - (HEIGHT - 150))
                scroll_y = 0

    screen.fill(BACKGROUND_COLOR)

    # Draw input box
    pygame.draw.rect(screen, INPUT_BOX_COLOR, input_box)
    text_surface = font.render(user_text, True, TEXT_COLOR)
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

    # Draw button
    mouse_pos = pygame.mouse.get_pos()
    button_color = BUTTON_HOVER_COLOR if calculate_button.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, button_color, calculate_button)
    button_text = font.render("Calculate", True, TEXT_COLOR)
    screen.blit(button_text, (calculate_button.x + 10, calculate_button.y + 10))

    # Draw steps
    if steps:
        for i, step in enumerate(steps):
            color = HIGHLIGHT_COLOR if i == current_step else TEXT_COLOR
            step_text = font.render(step, True, color)
            screen.blit(step_text, (50, 150 + i * STEP_HEIGHT - scroll_y))

    if visualizing:
        if current_step < len(steps) - 1:
            current_step += 1
        else:
            visualizing = False
        pygame.time.delay(500)  # Delay to slow down the visualization

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
