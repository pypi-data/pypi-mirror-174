# FrakkComm kommunikáció

> **_Disclaimer:_** If you have to ask what this is, it's not for you. Trust me.

## v1.0 specifikáció

TCP alapú kommunikáció

Komponensek:

- Byte 1, Kezdő:
  - Blockmarker
  - Értéke mindig `0x55`
- Byte 2, Hossz:
  - Az adatcsomag hossza byteban kifejezve
- Byte 2, Címzett:
  - Milyen eszközt címez meg
  - `0xFF` mindenkit megcímez (?)
- Byte 3, Feladó:
  - Nincs használva itt, `0x00` egyelőre jó
- Byte 4, Üzenet ID:
  - Az üzenet azonosítója
  - `0xF4` működik ha ez nem fontos
- Byte 5, Parancs:
  - ???
  - `0x56` működik, többit nem tudjuk még
- Byte 6-8, Adat:
  - adat csomag amit küldeni kell
  - Lámpák esetén:
    - Byte 1: Lámpa ID
    - Byte 2: szín
      - 64 fehér esetén
      - 128 kék esetén,
      - 64+128 mindkettő szín esetén
    - Byte 3: Fényerő
- Byte 9, Checksum

> **Fontos**: Minden bytenál ha az érték 0x55, akkor meg kell duplázni.

## Package build

A Python kód lefordítása:

### Előfeltételek

- Python 3, pip
- `pip install build`
- `pip install wheel`
- `pip install pytest`

### Lefordítás

```sh
python3 -m build
```

A lefordított package pedig a `./dist` mappában van, a `*.whl` file ami általában kell.

### Tesztelés

Pytest-et használva könnyen lehet tesztelni a kódot.

```sh
python3 -m pytest tests
```
