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
@click.argument("category_file", type=click.Path(exists=True, dir_okay=False))
@click.argument("symbol_folder", type=click.Path(exists=True, file_okay=False))
@click.argument("font_file", type=click.Path(exists=True, dir_okay=False))
@click.argument("output_folder", type=click.Path(file_okay=False, writable=True), default="output")
@click.option("-w", "--width", type=int, default=500, help="Width of generated cards, in pixels")
@click.option("-h", "--height", type=int, default=800, help="Height of generated cards, in pixels")
@click.option("-fs", "--font-size", type=int, default=55, help="Size of font used to render card text")
@click.option("-sw", "--symbol-width", type=int, default=300, help="Maximum width of symbol placed on cards, in pixels")
@click.option("-sh", "--symbol-height", type=int, default=300, help="Maximum height of symbol placed on cards, in pixels")
@click.option("-m", "--margin", type=int, default=30, help="Margin between card edges and card content, in pixels")
@click.option("-ls", "--line-spacing", type=int, default=0, help="Spacing between lines for multiline text, in pixels")
def main(
    category_file: str,
    symbol_folder: str,
    font_file: str,
    output_folder: str,
    width: int,
    height: int,
    font_size: int,
    symbol_width: int,
    symbol_height: int,
    margin: int,
    line_spacing: int
    ):
    """
    Generates a deck of Anomia cards using the categories in CATEGORY_FILE, the symbols in SYMBOL_FOLDER, and the font in FONT_FILE.

    CATEGORY_FILE should be a txt or csv file with one category per line. Categories may be multiple words.

    SYMBOL_FOLDER should be a folder containing symbol images, preferably in PNG format.
    The program attempts to randomly tag the cards with an equal amount of each symbol.

    FONT_FILE should be a TrueType font file used to render the category text on each card.

    OUTPUT_FOLDER is the folder which generated cards are saved to.
    """
    # Load categories
    try:
        categories = category_loader(category_file)
    except Exception as exc:
        click.echo(f"Failed to load categories: {exc}", err=True)
        raise click.Abort()
    # Load symbols
    symbols = symbol_loader(symbol_folder)
    # Load font
    font = ImageFont.FreeTypeFont(font_file, font_size)
    # Generate deck
    cards = generate_deck(categories,
        symbols,
        font=font,
        size=(width, height),
        symbol_size=(symbol_width, symbol_height),
        margin=margin,
        line_spacing=line_spacing)
    # Save all cards to output folder
    os.makedirs(output_folder, exist_ok=True)
    for i, card in enumerate(cards):
        name = f"front_{i:03}.png"
        card.save(os.path.join(output_folder, name))
    # Print out a nice message
    click.echo(f"Success! Generated {len(cards)} card(s).")