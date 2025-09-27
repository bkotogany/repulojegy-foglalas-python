class FoglalasiHiba(Exception):
    """Általános foglalási hiba."""

class JaratNemLetezik(FoglalasiHiba):
    pass

class ErvenytelenDatum(FoglalasiHiba):
    pass

class MarNemFoglalthato(FoglalasiHiba):
    pass

class FoglalasNemLetezik(FoglalasiHiba):
    pass
