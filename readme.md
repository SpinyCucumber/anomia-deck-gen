# anomia-deck-gen

Command-line tool to generate a deck of custom cards for the spectacular card game Anomia.
Requires a list of categories, a set of symbol images, and a font to generate the deck.
Written in Python with the help of Click and Pillow!

## Usage example

Simple example:
`python -m anomia_deck_gen categories.txt symbols/ MyFont.ttf output/`

Slightly less simple example:
`python -m anomia_deck_gen categories.csv symbols/ MyFont.ttf output/ --width 500 --height 800 --margin 20 --font-size 50`