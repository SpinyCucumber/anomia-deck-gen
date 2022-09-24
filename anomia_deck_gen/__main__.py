import click
import csv
import os
from PIL import Image, ImageFont
from typing import List

from .utility import SingleDispatchLoader
from .generator import generate_deck

category_loader = SingleDispatchLoader[List[str]]()

@category_loader.register("txt")
def load_txt(path: str):
    with open(path, "r") as file:
        return [line.rstrip() for line in file.readlines()]

@category_loader.register("csv")
def load_csv(path: str):
    with open(path, "r") as file:
        reader = csv.reader(file)
        return [row[0] for row in reader]

def symbol_loader(path: str) -> List[Image.Image]:
    return [Image.open(entry.path) for entry in os.scandir(path) if entry.is_file()]

@click.command()
@click.option("--category-file", type=click.Path(exists=True, dir_okay=False), required=True, help="File containing a list of categories")
@click.option("--symbol-folder", type=click.Path(exists=True, file_okay=False), required=True, help="Folder containing set of card symbols")
@click.option("--font-file", type=click.Path(exists=True, dir_okay=False), required=True, help="Font used to render card text")
@click.option("--output-folder", type=click.Path(file_okay=False, writable=True), required=True, help="Folder to output card images to")
def anomia_deck_gen(category_file, symbol_folder, font_file, output_folder):
    # Load categories
    categories = category_loader(category_file)
    if categories == None:
        raise click.ClickException("Failed to load categories")
    # Load symbols
    symbols = symbol_loader(symbol_folder)
    # Load font
    font = ImageFont.FreeTypeFont(font_file, 55)
    # Generate deck
    cards = generate_deck(categories, symbols, font=font, size=(500, 800), symbol_size=(300, 300), margin=30, line_spacing=5)
    # Save all cards to output folder
    os.makedirs(output_folder, exist_ok=True)
    for i, card in enumerate(cards):
        name = f"front_{i:03}.png"
        card.save(os.path.join(output_folder, name))

if __name__ == "__main__":
    anomia_deck_gen()