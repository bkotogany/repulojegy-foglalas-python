# Repülőjegy Foglalási Rendszer (Python, OOP)

Egyszerű, konzolos repülőjegy foglaló alkalmazás az alábbi követelmények alapján:

- **OOP**: absztrakt ősosztály (`Jarat`) + leszármazottak (`BelfoldiJarat`, `NemzetkoziJarat`), `LegiTarsasag`, `JegyFoglalas`.
- **Non‑public attribútumok**, **property-k** (getter/setter), **dunder metódusok**.
- **Hibakezelés** (típus-, dátum-, állapotellenőrzések).
- **Adatvalidáció**: elérhetőség, dátumok, csak létező foglalás törölhető.
- **Seed adatok**: 1 légitársaság, 3 járat, 6 foglalás betöltve induláskor.
- **Felhasználói interfész**: egyszerű menü: foglalás, lemondás, listázás.

## Futtatás

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python main.py
```

> **Megjegyzés:** A projekt *nem* igényel külső csomagokat.

## Fájlok

- `main.py` – konzolos felület és alkalmazás-indítás
- `models.py` – osztályok és domén logika
- `data_seed.py` – induló adatok létrehozása
- `exceptions.py` – egyedi kivételek
- `adatok.txt` – **TÖLTSD KI SAJÁT ADATAIDDAL** (név, szak, Neptun, képzés típusa)

## GitHub feltöltés

1. Új *public* repository a saját GitHub fiókodban (pl. `repulojegy-foglalas`).
2. Helyben:
   ```bash
   git init
   git add .
   git commit -m "Kezdő verzió – repülőjegy foglalási rendszer"
   git branch -M main
   git remote add origin https://github.com/<felhasznalonev>/<repo>.git
   git push -u origin main
   ```
3. Ellenőrizd inkognitó ablakban, hogy látszik-e a repo, és fut-e a projekt klónozás után.

## Tesztelés gyorsan

Indítás után a menüben már találsz 3 járatot és 6 foglalást. Például:
- Új foglalás: válassz járatot sorszám alapján, add meg nevet és dátumot (YYYY-MM-DD). 
- Lemondás: add meg a foglalás azonosítóját (pl. `RSV-0003`).

Jó munkát!
