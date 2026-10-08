# Experiment 9
**Title:** Language Translation Using Google Translator

## Aim
To write a Python program that translates text from one language to another using Google Translator (the `deep-translator` library).

## Algorithm
1. Install and import `GoogleTranslator` from `deep_translator`.
2. Accept the text to be translated from the user.
3. Accept the source language code (for example `en`).
4. Accept the target language code (for example `ta`, `fr`, `hi`).
5. Create the translator with the source and target languages.
6. Translate the text using the translator.
7. Display the original text and the translated text.
8. Stop.

## Program
```bash
pip install deep-translator
```
```python
from deep_translator import GoogleTranslator   # pip install deep-translator

text = input("Enter text to translate: ")
source = input("Enter source language code (e.g., en, ta, fr, hi): ")
target = input("Enter target language code (e.g., en, ta, fr, hi): ")

translated = GoogleTranslator(source=source, target=target).translate(text)
print("\nOriginal Text:\n" + text)
print("\nTranslated Text:\n" + translated)
```

## Output
```
Enter text to translate: how r u
Enter source language code (e.g., en, ta, fr, hi): en
Enter target language code (e.g., en, ta, fr, hi): ta

Original Text:
how r u

Translated Text:
(Tamil translation printed here)
```
The translated line is blank in your lab manual PDF (the Tamil text did not copy). Paste the actual Tamil output from your own run. The program needs internet access to work.

## Result
The text was translated from the source language to the target language using Google Translator, and both the original and translated text were displayed.
