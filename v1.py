import pygame
import hashlib
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (30, 30, 30)
TEXT_COLOR = (200, 200, 200)
HIGHLIGHT_COLOR = (100, 100, 255)
INPUT_BOX_COLOR = (60, 60, 60)
BUTTON_COLOR = (70, 70, 70)
BUTTON_HOVER_COLOR = (90, 90, 90)
FONT_SIZE = 16

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SHA256 Visualizer")

# Fonts
font = pygame.font.Font(None, FONT_SIZE)

class SHA256Visualizer:
    def __init__(self):
        self.input_text = ""
        self.input_box = pygame.Rect(10, 10, 580, 30)
        self.hash_button = pygame.Rect(600, 10, 90, 30)
        self.clear_button = pygame.Rect(700, 10, 90, 30)
        self.scroll_y = 0
        self.max_scroll = 0
        self.steps = []
        self.current_step = 0
        self.hash_result = ""

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hash_button.collidepoint(event.pos):
                self.hash_input()
            elif self.clear_button.collidepoint(event.pos):
                self.clear_input()
            elif event.button == 4:  # Scroll up
                self.scroll_y = max(self.scroll_y - 20, 0)
            elif event.button == 5:  # Scroll down
                self.scroll_y = min(self.scroll_y + 20, self.max_scroll)
        elif event.type == pygame.KEYDOWN:
            if self.input_box.collidepoint(pygame.mouse.get_pos()):
                if event.key == pygame.K_RETURN:
                    self.hash_input()
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode

    def hash_input(self):
        if self.input_text:
            self.steps = []
            self.current_step = 0
            self.hash_result = ""
            self.perform_sha256()

    def clear_input(self):
        self.input_text = ""
        self.steps = []
        self.current_step = 0
        self.hash_result = ""
        self.scroll_y = 0

    def perform_sha256(self):
        # Step 1: Preprocessing
        self.steps.append("Step 1: Preprocessing")
        binary = ''.join(format(ord(c), '08b') for c in self.input_text)
        binary += '1'
        while len(binary) % 512 != 448:
            binary += '0'
        binary += format(len(self.input_text) * 8, '064b')
        self.steps.append(f"Padded binary: {binary[:64]}...{binary[-64:]}")

        # Step 2: Initialize hash values
        self.steps.append("Step 2: Initialize hash values")
        h0 = 0x6a09e667
        h1 = 0xbb67ae85
        h2 = 0x3c6ef372
        h3 = 0xa54ff53a
        h4 = 0x510e527f
        h5 = 0x9b05688c
        h6 = 0x1f83d9ab
        h7 = 0x5be0cd19
        self.steps.append(f"Initial hash values: {h0:08x}, {h1:08x}, {h2:08x}, {h3:08x}, {h4:08x}, {h5:08x}, {h6:08x}, {h7:08x}")

        # Step 3: Chunk loop
        self.steps.append("Step 3: Chunk loop")
        chunks = [binary[i:i+512] for i in range(0, len(binary), 512)]
        for i, chunk in enumerate(chunks):
            self.steps.append(f"Processing chunk {i+1}/{len(chunks)}")

            # Step 4: Create message schedule
            self.steps.append("Step 4: Create message schedule")
            w = [int(chunk[i:i+32], 2) for i in range(0, 512, 32)]
            for i in range(16, 64):
                s0 = self.right_rotate(w[i-15], 7) ^ self.right_rotate(w[i-15], 18) ^ (w[i-15] >> 3)
                s1 = self.right_rotate(w[i-2], 17) ^ self.right_rotate(w[i-2], 19) ^ (w[i-2] >> 10)
                w.append((w[i-16] + s0 + w[i-7] + s1) & 0xFFFFFFFF)
            self.steps.append(f"Message schedule: {', '.join(f'{x:08x}' for x in w[:16])}...")

            # Step 5: Compression function main loop
            self.steps.append("Step 5: Compression function main loop")
            a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7
            for i in range(64):
                S1 = self.right_rotate(e, 6) ^ self.right_rotate(e, 11) ^ self.right_rotate(e, 25)
                ch = (e & f) ^ ((~e) & g)
                temp1 = h + S1 + ch + self.k[i] + w[i]
                S0 = self.right_rotate(a, 2) ^ self.right_rotate(a, 13) ^ self.right_rotate(a, 22)
                maj = (a & b) ^ (a & c) ^ (b & c)
                temp2 = S0 + maj

                h = g
                g = f
                f = e
                e = (d + temp1) & 0xFFFFFFFF
                d = c
                c = b
                b = a
                a = (temp1 + temp2) & 0xFFFFFFFF

                if i % 16 == 0:
                    self.steps.append(f"Round {i}: {a:08x}, {b:08x}, {c:08x}, {d:08x}, {e:08x}, {f:08x}, {g:08x}, {h:08x}")

            # Step 6: Modify final values
            h0 = (h0 + a) & 0xFFFFFFFF
            h1 = (h1 + b) & 0xFFFFFFFF
            h2 = (h2 + c) & 0xFFFFFFFF
            h3 = (h3 + d) & 0xFFFFFFFF
            h4 = (h4 + e) & 0xFFFFFFFF
            h5 = (h5 + f) & 0xFFFFFFFF
            h6 = (h6 + g) & 0xFFFFFFFF
            h7 = (h7 + h) & 0xFFFFFFFF
            self.steps.append(f"Modified hash values: {h0:08x}, {h1:08x}, {h2:08x}, {h3:08x}, {h4:08x}, {h5:08x}, {h6:08x}, {h7:08x}")

        # Step 7: Produce final hash value
        self.steps.append("Step 7: Produce final hash value")
        self.hash_result = f'{h0:08x}{h1:08x}{h2:08x}{h3:08x}{h4:08x}{h5:08x}{h6:08x}{h7:08x}'
        self.steps.append(f"Final SHA256 hash: {self.hash_result}")

        self.max_scroll = max(0, (len(self.steps) * 20) - HEIGHT + 50)

    def right_rotate(self, n, d):
        return ((n >> d) | (n << (32 - d))) & 0xFFFFFFFF

    def draw(self):
        screen.fill(BACKGROUND_COLOR)

        # Draw input box
        pygame.draw.rect(screen, INPUT_BOX_COLOR, self.input_box)
        text_surface = font.render(self.input_text, True, TEXT_COLOR)
        screen.blit(text_surface, (self.input_box.x + 5, self.input_box.y + 5))

        # Draw buttons
        for button, text in [(self.hash_button, "Hash"), (self.clear_button, "Clear")]:
            color = BUTTON_HOVER_COLOR if button.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
            pygame.draw.rect(screen, color, button)
            text_surface = font.render(text, True, TEXT_COLOR)
            text_rect = text_surface.get_rect(center=button.center)
            screen.blit(text_surface, text_rect)

        # Draw steps
        y = 50 - self.scroll_y
        for i, step in enumerate(self.steps):
            color = HIGHLIGHT_COLOR if i == self.current_step else TEXT_COLOR
            text_surface = font.render(step, True, color)
            screen.blit(text_surface, (10, y))
            y += 20

        # Draw hash result
        if self.hash_result:
            result_text = font.render(f"Final Hash: {self.hash_result}", True, HIGHLIGHT_COLOR)
            screen.blit(result_text, (10, HEIGHT - 30))

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

def main():
    visualizer = SHA256Visualizer()
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            visualizer.handle_event(event)

        visualizer.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

