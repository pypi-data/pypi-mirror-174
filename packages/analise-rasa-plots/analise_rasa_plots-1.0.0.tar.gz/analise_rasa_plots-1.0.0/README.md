# PACOTE_ANALISE_RASA

## Instalação

```bash
pip install analise-rasa
```

## Usage

```python
exemplo:
import analise_rasa as ar
import seaborn as sns

df = seaborn.load_dataset('diamonds')

ar.AnalisePreliminar([df],IncludeInt=True,InclueFloat=True,Kind='boxplot',NormalizeDf=True)

```

## Author
Alcimar M. Trindade

## License
[MIT](https://choosealicense.com/licenses/mit/)