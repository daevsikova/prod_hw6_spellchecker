# prod_hw6_spellchecker
Homework assignment for HSE Production Stories course

## Simple spell-checker implementation
- Based on Hunspell
- Used features are levenshtein, jaro_winkler, needleman_wunsch distances and 2 types of phonetic distance from `pyphonetics`

## Evaliation
```bash
python3 eval.py
```

### Results
```
Accuracy top-1: 0.5265
Accuracy top-5: 0.7422
Accuracy top-10: 0.7605
```

### Usage example is in `example.py` file