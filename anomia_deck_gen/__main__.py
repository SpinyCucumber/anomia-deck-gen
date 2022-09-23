import click
import csv
from typing import List
from .utility import SingleDispatchLoader

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

@click.command()
@click.option("--category-file", type=click.Path(exists=True, dir_okay=False), required=True, help="File containing a list of categories")
@click.option("--symbol-folder", type=click.Path(exists=True, file_okay=False), required=True, help="Folder containing set of card symbols")
@click.option("--output-folder", type=click.Path(file_okay=False, writable=True), required=True, help="Folder to output card images to")
def generate_cards(category_file, symbol_folder, output_folder):
    # Load categories
    categories = category_loader(category_file)
    if categories == None:
        raise click.ClickException("Failed to load categories")
    for category in categories:
        print(category)

if __name__ == "__main__":
    generate_cards()