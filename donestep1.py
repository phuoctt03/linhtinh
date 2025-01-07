
import pygame
import pygame.font
from hashlib import sha256
import time

pygame.init()
pygame.font.init()

WIDTH = 1200
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SHA-256 Algorithm Visualization")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (173, 216, 230)

FONT_SIZE = 20
font = pygame.font.SysFont('Arial', FONT_SIZE)
title_font = pygame.font.SysFont('Arial', 30, bold=True)
small_font = pygame.font.SysFont('Arial', 16)

class BinaryConverter:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.current_char = ""
        self.current_ascii = 0
        self.current_binary = ""
        self.show_conversion = False
        self.animation_step = 0
        self.last_update = 0
        
    def start_conversion(self, char):
        self.current_char = char
        self.current_ascii = ord(char)
        self.current_binary = format(self.current_ascii, '08b')
        self.show_conversion = True
        self.animation_step = 0
        self.last_update = time.time()
        
    def update(self):
        if not self.show_conversion:
            return
            
        current_time = time.time()
        if current_time - self.last_update > 0.5:  
            self.animation_step += 1
            self.last_update = current_time
            
        if self.animation_step > 10:
            self.show_conversion = False
            
    def draw(self, screen):
        if not self.show_conversion:
            return
        char_text = font.render(f"Character: '{self.current_char}'", True, BLACK)
        screen.blit(char_text, (self.x, self.y - 30))
        
        if self.animation_step >= 1:
            ascii_text = font.render(f"ASCII: {self.current_ascii}", True, BLUE)
            screen.blit(ascii_text, (self.x + 200, self.y - 30))
        
        if self.animation_step >= 2:
            binary_y = self.y + 10
            title = font.render("Binary conversion:", True, BLACK)
            screen.blit(title, (self.x, binary_y))

            step_y = binary_y + 30
            ascii_num = self.current_ascii
            for i in range(8):
                if self.animation_step >= i + 2:
                    bit = (ascii_num >> (7-i)) & 1
                    step_text = small_font.render(f"Step {i+1}: {ascii_num} ÷ 2 = {ascii_num//2} remainder {bit}", True, BLUE)
                    screen.blit(step_text, (self.x + 20, step_y + i*20))
                    ascii_num = ascii_num // 2
            
            if self.animation_step >= 10:
                result_text = font.render(f"Final binary: {self.current_binary}", True, GREEN)
                screen.blit(result_text, (self.x, step_y + 160))

class SHA256Visualizer:
    def __init__(self):
        self.message = ""
        self.current_step = 0
        self.total_steps = 6
        self.binary_message = ""
        self.padded_message = ""
        self.blocks = []
        self.final_hash = ""
        self.binary_converter = BinaryConverter(50, 150)
        self.current_char_index = 0
        self.conversion_complete = False
        self.binary_result = []
        
    def update_message(self, msg):
        self.message = msg
        self.current_step = 0
        self.binary_message = ""
        self.current_char_index = 0
        self.conversion_complete = False
        self.binary_result = []
        if len(msg) > 0:
            self.binary_converter.start_conversion(msg[0])
        
        msg_len_bits = len(msg) * 8
        k = (448 - msg_len_bits - 1) % 512
        self.padded_message = ''.join(format(ord(c), '08b') for c in msg) + '1' + '0' * k + format(msg_len_bits, '064b')
        
        self.blocks = [self.padded_message[i:i+512] for i in range(0, len(self.padded_message), 512)]
        
        self.final_hash = sha256(msg.encode()).hexdigest()

    def next_step(self):
        if self.current_step < self.total_steps and (self.conversion_complete or self.current_step == 0):
            self.current_step += 1

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            if self.current_step == 0:
                self.current_char_index = 0
                self.conversion_complete = False
                if len(self.message) > 0:
                    self.binary_converter.start_conversion(self.message[0])

    def update(self):
        self.binary_converter.update()
        
        if self.current_step == 1 and not self.conversion_complete:
            if not self.binary_converter.show_conversion:
                if self.current_char_index < len(self.message) - 1:
                    self.current_char_index += 1
                    self.binary_converter.start_conversion(self.message[self.current_char_index])
                    self.binary_result.append(format(ord(self.message[self.current_char_index-1]), '08b'))
                else:
                    if len(self.message) > 0:
                        self.binary_result.append(format(ord(self.message[-1]), '08b'))
                    self.conversion_complete = True

    def draw(self, screen):
        screen.fill(WHITE)
        
        title = title_font.render("SHA-256 Algorithm Visualization", True, BLACK)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
        
        msg_text = font.render(f"Input Message: {self.message}", True, BLACK)
        screen.blit(msg_text, (50, 50))
        
        if self.current_step >= 1:
            step_text = font.render("Step 1: Convert characters to binary", True, BLUE)
            screen.blit(step_text, (50, 90))
            
            if not self.conversion_complete:
                
                self.binary_converter.draw(screen)
            
            if len(self.binary_result) > 0:
                if self.conversion_complete:
                    
                    result_y = 160
                    complete_binary = ''.join(self.binary_result)
                    final_text = font.render("Final binary string:", True, BLACK)
                    screen.blit(final_text, (50, result_y - 40))
                    
                    chunk_size = 32
                    for i in range(0, len(complete_binary), chunk_size):
                        chunk = complete_binary[i:i+chunk_size]
                        binary_text = font.render(chunk, True, GREEN)
                        screen.blit(binary_text, (70, result_y - 10))
                else:
                    
                    result_y = 400
                    result_text = font.render("Converted results:", True, BLACK)
                    screen.blit(result_text, (50, result_y - 20 ))
                    
                    for i, binary in enumerate(self.binary_result):
                        char_text = font.render(f"'{self.message[i]}' = {binary}", True, GREEN)
                        screen.blit(char_text, (70, result_y + 10 + i*25))
        
        if self.current_step >= 2:
            self.draw_step2(screen)
        if self.current_step >= 3:
            self.draw_step3(screen)
        if self.current_step >= 4:
            self.draw_step4(screen)
        if self.current_step >= 5:
            self.draw_step5(screen)
            
    def draw_step2(self, screen):
        y = 180  
        text = font.render("Step 2: Padding", True, BLUE)
        screen.blit(text, (50, y))
        
        padding_y = y + 30
        msg_binary = ''.join(self.binary_result)
        
        padding_one = font.render("Add '1' bit:", True, BLACK)
        screen.blit(padding_one, (50, padding_y))
        screen.blit(font.render(msg_binary + "1", True, GREEN), (70, padding_y + 25))
        
        padding_zeros = font.render("Add '0' padding:", True, BLACK)
        screen.blit(padding_zeros, (50, padding_y + 50))
        padding_preview = self.padded_message[:-64]
        screen.blit(font.render(padding_preview[:32] + "..." + padding_preview[-32:], True, GREEN), 
                   (70, padding_y + 75))
        
        length_bits = font.render("Add message length (64 bits):", True, BLACK)
        screen.blit(length_bits, (50, padding_y + 100))
        screen.blit(font.render(self.padded_message[-64:], True, GREEN), 
                   (70, padding_y + 125))

    def draw_step3(self, screen):
        y = 355
        text = font.render("Step 3: Split into 512-bit blocks", True, BLUE)
        screen.blit(text, (50, y))

        block_y = y + 25
        for i, block in enumerate(self.blocks):
            if i >= 4:  
                overflow_text = font.render(f"... ({len(self.blocks) - 4} more blocks)", True, GRAY)
                screen.blit(overflow_text, (50, block_y + i * 25))
                break
            block_preview = block[:32] + "..." + block[-32:]  
            block_text = font.render(f"Block {i+1}: {block_preview} ({len(block)} bits)", True, BLACK)
            screen.blit(block_text, (50, block_y + i * 25))
        
    def draw_step4(self, screen):
        y = 400
        text = font.render("Step 4: Compression Function", True, BLUE)
        screen.blit(text, (50, y))
        
        compress_y = y + 25
        explanation = [
            "SHA-256 processes each block in 64 rounds.",
            "Each round updates 8 hash values using the block.",
            "Intermediate values are combined with constants (K) and functions (Ch, Maj, etc.).",
        ]
        for i, line in enumerate(explanation):
            screen.blit(font.render(line, True, BLACK), (50, compress_y + i * 20))

    def draw_step5(self, screen):
        y = 520
        text = font.render("Step 5: Final Hash", True, BLUE)
        screen.blit(text, (50, y))
        
        explanation = [
            "The final hash is produced by combining the 8 intermediate hash values:",
            "H0, H1, H2, H3, H4, H5, H6, and H7.",
            "These values are concatenated to form a single 256-bit hash.",
        ]
        for i, line in enumerate(explanation):
            screen.blit(font.render(line, True, BLACK), (50, y + 30 + i * 20))
        
        hash_text = font.render(f"Hash: {self.final_hash}", True, GREEN)
        screen.blit(hash_text, (50, y + 100))

def main():
    visualizer = SHA256Visualizer()
    visualizer.update_message("1")
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if 50 <= mouse_pos[0] <= 150 and HEIGHT - 50 <= mouse_pos[1] <= HEIGHT - 20:
                    visualizer.prev_step()
                
                elif 170 <= mouse_pos[0] <= 270 and HEIGHT - 50 <= mouse_pos[1] <= HEIGHT - 20:
                    visualizer.next_step()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    visualizer.prev_step()
                elif event.key == pygame.K_RIGHT:
                    visualizer.next_step()
                elif event.key == pygame.K_RETURN:
                    new_message = input("Enter new message: ")
                    visualizer.update_message(new_message)
        
        visualizer.update()
        visualizer.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
