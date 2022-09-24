from PIL import Image, ImageDraw, ImageFont
from typing import List, Tuple
from random import shuffle
from math import floor

def create_text_image(text: str, font: ImageFont.FreeTypeFont, max_length: int, line_spacing: int) -> Image.Image:

    # First, determine the longest word length. If the longest word is longer than the max length,
    # we decrease the font size appropriately.
    words = text.split(" ")
    max_word_length = max([font.getlength(word) for word in words])
    if max_word_length > max_length:
        new_size = int((max_length / max_word_length) * font.size)
        font = font.font_variant(size=new_size)

    # Split the text into lines which are strictly shorter than the max length
    lines = []
    current_line = words[0]
    for word in words[1:]:
        test_line = current_line + " " + word
        if font.getlength(test_line) > max_length:
            lines.append(current_line)
            current_line = word
        else:
            current_line = test_line
    lines.append(current_line)

    # Compute the image size from the lines
    height = 0
    width = 0
    line_sizes = [font.getsize(line) for line in lines]
    for line_width, line_height in line_sizes:
        width = max(width, line_width)
        height += line_height
    height += (line_spacing * (len(lines) - 1))

    # Create new image
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Render text onto image
    x = width//2
    y = 0
    for i, line in enumerate(lines):
        draw.text((x, y), line, anchor="mt", fill="black", font=font)
        y += (line_sizes[i][1] + line_spacing)
    return img

def generate_card(
    category: str,
    symbol: Image.Image,
    size: Tuple[int, int],
    margin: int,
    line_spacing: int,
    font: ImageFont.ImageFont
    ) -> Image.Image:
    # Create blank image
    img = Image.new("RGBA", size, "white")
    # Paste symbol into image
    img.alpha_composite(symbol, tuple(size[i]//2 - symbol.size[i]//2 for i in range(2)))
    # Draw text onto image
    text_img = create_text_image(category, font, max_length=(size[0] - 2*margin), line_spacing=line_spacing)
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