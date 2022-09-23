from PIL import Image, ImageDraw, ImageFont
from typing import List, Tuple
from random import shuffle
from math import floor

def create_text_image(text: str, font: ImageFont.ImageFont) -> Image.Image:
    img = Image.new("RGBA", font.getsize(text), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, fill="black", font=font)
    return img

def generate_card(
    category: str,
    symbol: Image.Image,
    size: Tuple[int, int],
    margin: int,
    font: ImageFont.ImageFont) -> Image.Image:

    # Create blank image
    img = Image.new("RGBA", size, "white")
    # Paste symbol into image
    img.paste(symbol, tuple(size[i]//2 - symbol.size[i]//2 for i in range(2)))
    # Draw text onto image
    text_img = create_text_image(category, font)
    img.alpha_composite(text_img, (size[0]//2 - text_img.size[0]//2, size[1] - margin - text_img.size[1]))
    # Flip the text and draw on top
    flipped_text = text_img.transpose(Image.Transpose.ROTATE_180)
    img.alpha_composite(flipped_text, (size[0]//2 - flipped_text.size[0]//2, margin))
    return img

def generate_deck(categories: List[str], symbols: List[Image.Image], symbol_size: Tuple[int, int], **kwargs) -> List[Image.Image]:
    # Preprocess the symbols by normalizing their size
    normalized_symbols = [symbol.copy() for symbol in symbols]
    for symbol in normalized_symbols:
        symbol.thumbnail(symbol_size)
    # Create a shuffled copy of the categories
    shuffled_categories = list(categories)
    shuffle(shuffled_categories)
    # Tag each category with a symbol
    tagged_categories = [(category, normalized_symbols[floor(i/len(categories) * len(symbols))]) for i, category in enumerate(shuffled_categories)]
    # Generate card images
    return [generate_card(category, symbol, **kwargs) for category, symbol in tagged_categories]