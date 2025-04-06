from PIL import Image, ImageDraw
import numpy as np
from config import COLORS

class KachelImageGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def generate_gradient(self):
        top_color = np.array([0, 162, 223])
        bottom_color = np.array([0, 102, 166])
        image = Image.new('RGB', (self.width, self.height), "#00ccff")
        draw = ImageDraw.Draw(image)
        for y in range(self.height):
            ratio = y / self.height
            r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
            g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
            b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
            draw.line([(0, y), (self.width, y)], fill=(r, g, b))
        return image

    def add_rays(self, image, strength=25):
        overlay = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
        draw_overlay = ImageDraw.Draw(overlay)
        center_x, center_y = self.width // 2, self.height // 3
        for angle in range(0, 360, 15):
            end_x = int(center_x + self.width * np.cos(np.radians(angle)))
            end_y = int(center_y + self.height * np.sin(np.radians(angle)))
            draw_overlay.line([(center_x, center_y), (end_x, end_y)], fill=(255, 255, 255, strength), width=2)
        return Image.alpha_composite(image.convert("RGBA"), overlay)

    def save_image(self, image, filename):
        image.save(filename)
