from tqdm import tqdm
from spellchecker import SpellChecker


def evaluate(spellchecker, data, top_k=[1, 5, 10]):
    accuracy = {k: 0.0 for k in top_k}

    for word, true_replace in tqdm(data):
        candidates = spellchecker.suggest_word(word, eval=True)

        for k in top_k:
            if true_replace in candidates[:k]:
                accuracy[k] += 1

    accuracy = {k: accuracy[k] / len(data) for k in top_k}
    return accuracy


if __name__ == "__main__":
    checker = SpellChecker()
    test_data = []
    with open("data/batch0.tab.txt") as f:
        lines = f.readlines()
        for line in lines:
            test_data.append(line.strip().split("\t"))

    top_k = [1, 5, 10]
    accuracy = evaluate(checker, test_data, top_k=top_k)

    for k in top_k:
        print(f"Accuracy top-{k}: {accuracy[k]:.4f}")
