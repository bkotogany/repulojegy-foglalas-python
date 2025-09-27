from datetime import date
from typing import Optional
from models import *
from exceptions import *
from data_seed import inicializal

def beolvas_datum(szoveg: str) -> date:
    try:
        return date.fromisoformat(szoveg)
    except Exception as e:
        raise ErvenytelenDatum("Dátum formátum: YYYY-MM-DD") from e

def lista_jaratok(lt: LegiTarsasag):
    print("\nElérhető járatok:")
    for idx, j in enumerate(lt.jaratok, start=1):
        print(f"  {idx}. {j} | végső ár: {j.ar():.0f} Ft")


def lista_foglalasok(lt: LegiTarsasag):
    if not lt.foglalasok:
        print("\nNincs még foglalás.")
        return
    print("\nFoglalások (ár szerint rendezve):")
    for f in sorted(lt.foglalasok):
        print("  ", f)

def menu():
    print("\n== Repülőjegy Foglalási Rendszer ==")
    print("1) Járatok listázása")
    print("2) Jegy foglalása")
    print("3) Foglalás lemondása")
    print("4) Foglalások listázása")
    print("0) Kilépés")

def futtat():
    lt = inicializal()
    print(lt)

    while True:
        menu()
        valasz = input("Választás: ").strip()
        try:
            if valasz == "1":
                lista_jaratok(lt)
            elif valasz == "2":
                lista_jaratok(lt)
                jaratszam = input("Add meg a járatszámot (pl. MA100): ").strip().upper()
                nev = input("Utas neve: ").strip()
                datum_str = input("Utazás napja (YYYY-MM-DD): ").strip()
                datum = beolvas_datum(datum_str)
                fogl = lt.uj_foglalas(nev, jaratszam, datum)
                print(f"Sikeres foglalás! {fogl}")
            elif valasz == "3":
                lista_foglalasok(lt)
                az = input("Add meg a foglalás azonosítóját (pl. RSV-0003): ").strip().upper()
                torolt = lt.lemond(az)
                print(f"Lemondva: {torolt}")
            elif valasz == "4":
                lista_foglalasok(lt)
            elif valasz == "0":
                print("Viszlát!")
                break
            else:
                print("Ismeretlen menüpont.")
        except FoglalasiHiba as fh:
            print(f"Hiba: {fh}")
        except ValueError as ve:
            print(f"Érvénytelen adat: {ve}")
        except Exception as ex:
            print(f"Váratlan hiba: {ex}")

if __name__ == "__main__":
    futtat()
