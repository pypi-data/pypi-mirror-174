from declara import Declara

declara = Declara()

declara.rows = [
    Declara.Row("Nieuwe merchandise", 64.22),
    Declara.Row("Stickers", 22.96),
]

declara.name = "Jouw Naam"
declara.iban = "NL12INGB2590295195"

declara.attachments = ["https://i.imgur.com/Mw5MEyq.jpeg"]

declara.send_email()
