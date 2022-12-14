from importlib.metadata import entry_points
from setuptools import setup

setup(
    name="anomia-deck-gen",
    version="0.1.0",
    author="SpinyCucumber",
    author_email="spinycucumber@gmail.com",
    packages=["anomia_deck_gen"],
    description="Generates decks of Anomia cards using lists of categories",
    install_requires=[
        "click==8.1.3",
        "colorama==0.4.5",
        "Pillow==9.2.0",
    ],
    entry_points={
        "console_scripts": ["anomia_deck_gen=anomia_deck_gen:main"],
    },
)