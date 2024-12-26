# PLAYSTORE - DashApp

Projekt je do niekolko sloziek:

- `data/raw` obsahuje neupravene data z Google Play Store,
- `data/clean` obsahuje ocistene data k tvorbe grafo a prezentaci,
- `notebooks` obsahuje Jupyter notebooky, kde sa nachadza analyza dat a trenovanie modelu
  -  Jupyter notebooky OBSAH 
      - `001_exploratory_analysis.ipynb` - Exploratorna analysa spojene s cistenim dat
      - `002_prediction.ipynb` - Vypocet, trenovanie a uloženie modelu

- `src/playstore` je hlavní složka obsahující zdrojové kódy samotné Dash aplikace, ale i pomocné funkce a proměnné dostupné pro notebooky.

## Instalace

Pre beznu pracu instalacia v *development* mode do lokalne virtualneho prostredia. Na Linux/Mac postupup:

```bash
python3 -m venv .vevn
source ./.venv/bin/activate
pip3 install -e .
```

## Spustenie
```bash
python3 -m ./src/playstore/main.py
```


V tomto virtuálnom prostredí bude aplikácia a všetky jej závislosti k dispozícii a náš vlastný balík playstore (ktorého súčasťou je dashboard) bude možné importovať aj v prostredí Jupyter.
## Dokumentace


Na generovanie dokumentácie používam jednoduchý balík pdoc. V tomto projekte je uvedený ako dev závislosť a nainštaluje sa pomocou:```bash
```bash
`pip3 install pdoc`. `pdoc` 
make docs
```

Stači ho iba spustit otovrit index.html v prehliadaci.

Postavý sa príslušný `Makefile` obsahuje príkaz:

```bash
pdoc src/playstore --docformat google --no-include-undocumented --output-dir docs
```

## Použité knihovny
- dash
- dash-bootstrap-components
- jupyterlab
- matplotlib
- numpy
- pandas
- plotly
- joblib **(pre ukladaniu modelu v ./pages/predicition)**
- scikit-learrn **(pre vytvaranie modelu  ./pages/predicition)**

# playstore
