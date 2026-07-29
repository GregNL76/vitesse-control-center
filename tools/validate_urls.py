from src.vcc.url_builder import UrlBuilder

examples = [
    "A Boy and His Blob",
    "Lara Croft: Tomb Raider",
    "O'Connor & Sons",
    "Pokémon: Let's Go",
    "Café del Mar",
]

for title in examples:
    print(title, "->", UrlBuilder.search_url(title))
