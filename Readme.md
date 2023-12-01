# Projectnaam: Donkeytravel

## Beschrijving

Donkeytravel is een Django-project ontworpen voor het beheer van reisgerelateerde gegevens.

## Installatie

Om Donkeytravel op je werkstation uit te voeren, moet je eerst de volgende tools en software installeren:

### Docker

Docker is een essentieel onderdeel van het project, omdat het wordt gebruikt om containers te beheren waarin de applicatie wordt uitgevoerd. Volg deze stappen om Docker op je werkstation te installeren:

- Voor MacOS: Volg de installatie-instructies voor Docker op de [Docker-website voor MacOS](https://www.docker.com/products/docker-desktop/).

- Voor Windows: Volg de installatie-instructies voor Docker op de [Docker-website voor Windows](https://www.docker.com/products/docker-desktop/).

### Python en Django

Donkeytravel is gebaseerd op Django, dus zorg ervoor dat je Python en Django hebt geïnstalleerd op je werkstation:

- Installeer Python: Ga naar de [Python-downloadpagina](https://www.python.org/downloads/) en volg de instructies voor het installeren van Python.

- Installeer Django: Nadat Python is geïnstalleerd, open je een terminal en voer je het volgende commando uit om Django te installeren:

  ```bash
  pip install Django
  ```

Nu je Docker, Python en Django hebt geïnstalleerd, kun je het project op je werkstation starten.

## Gebruik

### Updates README

Als je wijzigingen aanbrengt in de README, zorg er dan voor dat je deze bijwerkt.

### Docker-opdrachten

Hier zijn enkele nuttige Docker-opdrachten om het project te beheren:

- Bouw en start het project:

  ```bash
  make up
  ```

- Stop het project en verwijder volumes:

  ```bash
  make down
  ```

- Voer database-migraties uit:

  ```bash
  make migrate
  ```

- Maak database-migraties:

  ```bash
  make makemigrations
  ```

- Update statische bestanden:

  ```bash
  make collectstatic
  ```

- Stop het project zonder volumes te verwijderen:

  ```bash
  make stop
  ```

- Start het gestopte project:

  ```bash
  make start
  ```

- Herstel het project naar de oorspronkelijke staat (stop, verwijder volumes en afbeeldingen):

  ```bash
  make reset
  ```

- Maak een super user om in de Django admin panel in te loggen:

  ```bash
  make admin
  ```

Het kan gebeuren dat je een error krijgt, probeer dan eerst sudo make {de command} te doen. Sommige bestanden staan namelijk op root dus dan heb je sudo nodig deze te beheren.

### Contact

Als je vragen, opmerkingen of problemen hebt, kun je contact met ons opnemen via:

- E-mails:  [diyarfranklin2000@gmail.com](mailto:diyarfranklin2000@gmail.com), 
            [9008292@student.zadkine.nl](mailto:9008292@student.zadkine.nl)

- Discords: originalmatrix,
            captainspazmo

Aarzel niet om contact op te nemen als je hulp nodig hebt of als je wilt bijdragen aan het project. We staan altijd klaar om je te assisteren en te ondersteunen! 

### Voor Windows-gebruikers

Voor Windows-gebruikers wordt aanbevolen om "Ubuntu on Windows" (WSL) te gebruiken om de `make`-opdrachten uit te voeren. WSL biedt een Linux-compatibele omgeving op Windows, waarmee je de make-opdrachten kunt gebruiken zoals op Unix-gebaseerde systemen. Volg deze stappen om WSL te installeren:

1. Ga naar de **Microsoft Store** op je Windows-machine.

2. Zoek naar "Ubuntu" en selecteer de gewenste Ubuntu-distributie (bijvoorbeeld "Ubuntu 20.04 LTS").

3. Klik op de "Installeren" knop om de distributie te downloaden en te installeren.

4. Start de geïnstalleerde Ubuntu-distributie en volg de setup-instructies om een gebruikersaccount te maken.

5. Zodra Ubuntu op WSL is geïnstalleerd en geconfigureerd, kun je de `make`-opdrachten uitvoeren zoals aangegeven in de README.
