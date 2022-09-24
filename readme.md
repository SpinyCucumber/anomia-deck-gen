# anomia-deck-gen

Command-line tool to generate a deck of custom cards for the spectacular card game Anomia.
Requires a list of categories, a set of symbol images, and a font to generate the deck.
Written in Python with the help of Click and Pillow!

## Installation

To install the package and associated scripts, run `python setup.py install`.

## Usage example

Simple example:

`anomia_deck_gen categories.txt symbols/ MyFont.ttf output/`

Slightly less simple example:

`anomia_deck_gen categories.csv symbols/ MyFont.ttf output/ --width 500 --height 800 --margin 20 --font-size 50`