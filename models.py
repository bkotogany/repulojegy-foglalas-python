from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional
from exceptions import FoglalasiHiba, JaratNemLetezik, ErvenytelenDatum, MarNemFoglalthato, FoglalasNemLetezik

class Jarat(ABC):
    """Absztakt ősosztály minden járathoz."""
    def __init__(self, jaratszam: str, celallomas: str, jegyar: float, ferohely: int):
        self._jaratszam = jaratszam
        self._celallomas = celallomas
        self._jegyar = float(jegyar)
        self._ferohely = int(ferohely)
        self._aktiv = True

    # property-k (getter/setter)
    @property
    def jaratszam(self) -> str:
        return self._jaratszam

    @property
    def celallomas(self) -> str:
        return self._celallomas

    @celallomas.setter
    def celallomas(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Érvénytelen célállomás")
        self._celallomas = value

    @property
    def jegyar(self) -> float:
        return self._jegyar

    @jegyar.setter
    def jegyar(self, value: float):
        v = float(value)
        if v <= 0:
            raise ValueError("A jegyárnak pozitívnak kell lennie")
        self._jegyar = v

    @property
    def ferohely(self) -> int:
        return self._ferohely

    @ferohely.setter
    def ferohely(self, value: int):
        v = int(value)
        if v <= 0:
            raise ValueError("A férőhely legyen pozitív egész")
        self._ferohely = v

    @property
    def aktiv(self) -> bool:
        return self._aktiv

    def inaktival(self):
        self._aktiv = False

    @abstractmethod
    def ar(self) -> float:
        """Végső ár (pl. belföldi kedvezmény vagy nemzetközi felár)."""
        ...

    def __str__(self):
        status = "aktív" if self._aktiv else "inaktív"
        return f"{self._jaratszam} -> {self._celallomas} | alapár: {self._jegyar:.0f} Ft | férőhely: {self._ferohely} | {status}"

    def __repr__(self):
        return f"Jarat({self._jaratszam!r}, {self._celallomas!r}, {self._jegyar!r}, {self._ferohely!r})"


class BelfoldiJarat(Jarat):
    """Belföldi: olcsóbb (pl. -10%)."""
    KEDVEZMENY = 0.10
    def ar(self) -> float:
        return round(self._jegyar * (1 - self.KEDVEZMENY), 2)


class NemzetkoziJarat(Jarat):
    """Nemzetközi: drágább (pl. +25%)."""
    FELAR = 0.25
    def ar(self) -> float:
        return round(self._jegyar * (1 + self.FELAR), 2)


@dataclass(order=True)
class JegyFoglalas:
    """Egy jegy foglalását reprezentálja."""
    # Rendezés alapja: foglalási ár
    ar: float = field(init=False, compare=True)
    azonosito: str = field(compare=False)
    utas_nev: str = field(compare=False)
    jarat: Jarat = field(compare=False)
    utazas_napja: date = field(compare=False)

    def __post_init__(self):
        if not isinstance(self.utazas_napja, date):
            raise ErvenytelenDatum("Az utazás napja dátum típus kell legyen (datetime.date)")
        self.ar = self.jarat.ar()

    def __str__(self):
        return f"{self.azonosito} | {self.utas_nev} | {self.jarat.jaratszam} -> {self.jarat.celallomas} | {self.utazas_napja.isoformat()} | {self.ar:.0f} Ft"

    def __len.me__(self):  # deliberately unused, but example of extra dunder could be __hash__ or eq (dataclass fournished)
        return 1


class LegiTarsasag:
    def __init__(self, nev: str):
        self._nev = nev
        self._jaratok: List[Jarat] = []
        self._foglalasok: List[JegyFoglalas] = []

    @property
    def nev(self) -> str:
        return self._nev

    @property
    def jaratok(self) -> List[Jarat]:
        return list(self._jaratok)

    @property
    def foglalasok(self) -> List[JegyFoglalas]:
        return list(self._foglalasok)

    def hozzaad_jarat(self, jarat: Jarat):
        self._jaratok.append(jarat)

    def keres_jarat(self, jaratszam: str) -> Jarat:
        for j in self._jaratok:
            if j.jaratszam == jaratszam:
                return j
        raise JaratNemLetezik(f"Nincs ilyen járat: {jaratszam}")

    def jarat_foglalthato(self, jarat: Jarat) -> bool:
        if not jarat.aktiv:
            return False
        # egyszerű kapacitás: foglalások számolása járatra
        foglalas_db = sum(1 for f in self._foglalasok if f.jarat.jaratszam == jarat.jaratszam)
        return foglalas_db < jarat.ferohely

    def uj_foglalas(self, utas_nev: str, jaratszam: str, utazas_napja: date) -> JegyFoglalas:
        if not isinstance(utazas_napja, date):
            raise ErvenytelenDatum("Az utazás napjának dátumnak kell lennie (YYYY-MM-DD)")
        if utazas_napja < date.today():
            raise ErvenytelenDatum("Múltbeli dátumra nem foglalhatsz")

        jarat = self.keres_jarat(jaratszam)
        if not self.jarat_foglalthato(jarat):
            raise MarNemFoglalthato(f"A(z) {jaratszam} járatra már nem foglalható több jegy.")

        azonosito = f"RSV-{len(self._foglalasok)+1:04d}"
        foglalas = JegyFoglalas(azonosito=azonosito, utas_nev=utas_nev, jarat=jarat, utazas_napja=utazas_napja)
        self._foglalasok.append(foglalas)
        return foglalas

    def lemond(self, azonosito: str) -> JegyFoglalas:
        for i, f in enumerate(self._foglalasok):
            if f.azonosito == azonosito:
                return self._foglalasok.pop(i)
        raise FoglalasNemLetezik(f"Nincs ilyen foglalás: {azonosito}")

    def __len__(self):
        """A légitársaság járatainak száma."""
        return len(self._jaratok)

    def __str__(self):
        return f"{self._nev} – {len(self)} járat, {len(self._foglalasok)} foglalás"
