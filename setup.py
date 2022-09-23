from setuptools import setup

setup(
    name="anomia-deck-gen",
    version="0.1.0",
    author="SpinyCucumber",
    author_email="spinycucumber@gmail.com",
    packages=["anomia_deck_gen"],
    description="Generates decks of Anomia cards using lists of categories",
    install_requires=[
        "Pillow==9.2.0"
    ],
)