from declara import Declara

declara = Declara()

declara.rows = [
    Declara.Row("Nieuwe merchandise", 64.22),
    Declara.Row("Stickers", 22.96),
]

declara.name = "Jouw Naam"
declara.iban = "NL12INGB2590295195"

declara.attachments = ["bonnetje_benzine.jpg", "bonnetje_bier.jpg"]

declara.produce()
