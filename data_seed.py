from datetime import date, timedelta
from models import LegiTarsasag, BelfoldiJarat, NemzetkoziJarat

def inicializal() -> LegiTarsasag:
    lt = LegiTarsasag("Magyar Air")

    j1 = BelfoldiJarat("MA100", "Debrecen", 19990, ferohely=3)
    j2 = BelfoldiJarat("MA120", "Szeged", 14990, ferohely=2)
    j3 = NemzetkoziJarat("MA700", "London", 39990, ferohely=4)

    for j in (j1, j2, j3):
        lt.hozzaad_jarat(j)

    # Előre feltöltött 6 foglalás (a férőhelyek figyelembevételével)
    # Dátumok: jövőbeni napok
    base = date.today() + timedelta(days=14)
    lt.uj_foglalas("Kiss Anna", "MA100", base)
    lt.uj_foglalas("Nagy Béla", "MA100", base + timedelta(days=1))
    lt.uj_foglalas("Tóth Csaba", "MA100", base + timedelta(days=2))  # ezzel MA100 betelik

    lt.uj_foglalas("Szabó Dóra", "MA120", base + timedelta(days=3))
    lt.uj_foglalas("Farkas Előd", "MA120", base + timedelta(days=4))  # MA120 betelik

    lt.uj_foglalas("Juhász Fanni", "MA700", base + timedelta(days=5))

    return lt
