from collections import Counter
import re

def analyze_repeated_words(titles, threshold=2):
    word_counter = Counter()

    # Normalize and split words from all titles
    for title in titles:
        words = re.findall(r'\b\w+\b', title.lower())  # Removes punctuation, lowers case
        word_counter.update(words)

    # Filter words occurring more than 'threshold' times
    repeated_words = {word: count for word, count in word_counter.items() if count >= threshold}

    print("\nRepeated words:")
    for word, count in repeated_words.items():
        print(f"'{word}': {count}")