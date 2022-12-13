from back.AHP import AHP

criteria = [
    "lokalizacja",
    "obsluga",
    "wystroj",
    "ilosc smakow",
    "jakosc lodow",
    "cena",
    "jakosc sorbetow",
]
propositions = ["Good Lood Miasteczko AGH", "Wadowice", "Tiffany Ice Cream"]
# criteria = ["jakosc lodow", "cena", "jakosc sorbetow"]

if __name__ == "__main__":
    ahp = AHP(criteria, propositions)
    ahp.start()
