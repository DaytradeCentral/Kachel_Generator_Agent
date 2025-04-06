from generator.image_generator import KachelImageGenerator
from config import FORMATS

def main():
    format_choice = "square"
    size = FORMATS[format_choice]
    generator = KachelImageGenerator(*size)
    base = generator.generate_gradient()
    final = generator.add_rays(base)
    generator.save_image(final, f"kachel_{format_choice}.png")
    print("Kachel gespeichert.")

if __name__ == "__main__":
    main()
