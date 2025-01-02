import pygame
import hashlib

# Kích thước màn hình và các tham số hiển thị
WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Hàm xoay phải (right rotate)
def right_rotate(value, shift):
    return ((value >> shift) | (value << (32 - shift))) & 0xFFFFFFFF

class SHA256Visualizer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("SHA-256 Visualizer")
        self.font = pygame.font.SysFont("Arial", 18)
        self.steps = []  # Các bước chi tiết trong thuật toán
        self.input_text = ""  # Văn bản đầu vào
        self.hash_result = ""  # Kết quả hash
        self.scroll_offset = 0  # Đối số cuộn
        self.running = True

        # Hằng số k cho SHA-256
        self.k = [
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        ]

    def draw_text(self, text, x, y, max_width=700):
        lines = []
        current_line = ""
        for word in text.split():
            # Nếu thêm từ vào dòng hiện tại vượt quá độ dài tối đa, ta sẽ bắt đầu một dòng mới
            if self.font.size(current_line + " " + word)[0] <= max_width:
                current_line += " " + word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        # Vẽ từng dòng của văn bản lên màn hình
        for i, line in enumerate(lines):
            label = self.font.render(line, True, BLACK)
            self.screen.blit(label, (x, y + i * 20))

    def get_input(self):
        """Lấy văn bản đầu vào từ người dùng"""
        self.input_text = ""  # Đảm bảo input_text là chuỗi trống trước khi nhập liệu mới
        input_box = pygame.Rect(50, 50, 700, 40)
        typing = True
        while typing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Nhấn Enter để bắt đầu tính toán
                        typing = False  # Dừng vòng lặp khi nhấn Enter
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]  # Xóa ký tự cuối
                    else:
                        self.input_text += event.unicode  # Thêm ký tự mới vào
  
            self.screen.fill(WHITE)
            pygame.draw.rect(self.screen, BLACK, input_box, 2)
            self.draw_text("Enter text for SHA-256:", 50, 10)
            self.draw_text(self.input_text, 55, 55)
            pygame.display.update()

    def perform_sha256(self):
        """Thực hiện thuật toán SHA-256 và ghi lại các bước chi tiết"""
        # Step 1: Preprocessing
        self.steps.append("Step 1: Preprocessing")
        binary = ''.join(format(ord(c), '08b') for c in self.input_text)
        binary += '1'
        while len(binary) % 512 != 448:
            binary += '0'
        binary += format(len(self.input_text) * 8, '064b')
        self.steps.append(f"Padded binary: {binary[:64]}...{binary[-64:]}")

        # Create message blocks
        self.message_blocks = [binary[i:i+512] for i in range(0, len(binary), 512)]
        self.steps.append(f"Number of 512-bit blocks: {len(self.message_blocks)}")

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
        for i, chunk in enumerate(self.message_blocks):
            self.steps.append(f"Processing block {i+1}/{len(self.message_blocks)}")

            # Step 4: Create message schedule
            self.steps.append("Step 4: Create message schedule")
            w = [int(chunk[i:i+32], 2) for i in range(0, 512, 32)]
            for i in range(16, 64):
                s0 = right_rotate(w[i-15], 7) ^ right_rotate(w[i-15], 18) ^ (w[i-15] >> 3)
                s1 = right_rotate(w[i-2], 17) ^ right_rotate(w[i-2], 19) ^ (w[i-2] >> 10)
                w.append((w[i-16] + s0 + w[i-7] + s1) & 0xFFFFFFFF)
            self.message_schedule = w
            self.steps.append(f"Message schedule: {', '.join(f'{x:08x}' for x in w[:16])}...")

            # Step 5: Compression function main loop
            self.steps.append("Step 5: Compression function main loop")
            a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7
            for i in range(64):
                S1 = right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25)
                ch = (e & f) ^ ((~e) & g)
                temp1 = h + S1 + ch + self.k[i] + w[i]
                S0 = right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22)
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

                # Append detailed calculation steps for each round
                self.steps.append(f"Round {i}:")
                self.steps.append(f"  a={a:08x}, b={b:08x}, c={c:08x}, d={d:08x}, e={e:08x}, f={f:08x}, g={g:08x}, h={h:08x}")
                self.steps.append(f"  S1={S1:08x}, ch={ch:08x}, temp1={temp1:08x}, S0={S0:08x}, maj={maj:08x}, temp2={temp2:08x}")

            # Step 6: Modify final values
            h0 = (h0 + a) & 0xFFFFFFFF
            h1 = (h1 + b) & 0xFFFFFFFF
            h2 = (h2 + c) & 0xFFFFFFFF
            h3 = (h3 + d) & 0xFFFFFFFF
            h4 = (h4 + e) & 0xFFFFFFFF
            h5 = (h5 + f) & 0xFFFFFFFF
            h6 = (h6 + g) & 0xFFFFFFFF
            h7 = (h7 + h) & 0xFFFFFFFF

        # Step 7: Final hash value
        self.hash_result = f"{h0:08x}{h1:08x}{h2:08x}{h3:08x}{h4:08x}{h5:08x}{h6:08x}{h7:08x}"
        self.steps.append(f"Final hash: {self.hash_result}")

    def run(self):
        self.get_input()
        self.perform_sha256()

        while self.running:
            self.screen.fill(WHITE)

            # Vẽ các bước SHA-256 với khả năng cuộn
            self.draw_text("SHA-256 Steps", 50, 100)
            self.draw_text("\n".join(self.steps[self.scroll_offset:]), 50, 120)

            # Vẽ kết quả hash
            self.draw_text(f"Hash result: {self.hash_result}", 50, HEIGHT - 100)

            pygame.display.update()

            # Lắng nghe sự kiện để thoát hoặc cuộn lên/cuộn xuống
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.scroll_offset = min(self.scroll_offset + 1, len(self.steps) - 1)
                    elif event.key == pygame.K_UP:
                        self.scroll_offset = max(self.scroll_offset - 1, 0)

        pygame.quit()

if __name__ == "__main__":
    app = SHA256Visualizer()
    app.run()
