# Experiment 12
**Title:** Chatbot using NLP

## Aim
To design a simple rule-based chatbot using NLTK that replies to the user with predefined responses.

## Algorithm
1. Import `Chat` and `reflections` from `nltk.chat.util`.
2. Define a list of patterns (regular expressions) with their possible replies.
3. Add a last pattern `(.*)` as the default reply for anything not understood.
4. Create the chatbot object with the patterns and `reflections`.
5. Display the welcome message and tell the user to type `bye` to exit.
6. Accept the user's input and match it against the patterns.
7. Display the reply of the first matching pattern (picked randomly if there are several replies).
8. Continue the conversation until the user types `bye` or `goodbye`, then stop.

## Program
> **FIX vs. the lab manual:** the `pairs` list in the manual is missing its closing `]`, which gives a SyntaxError. It is closed here.

```python
from nltk.chat.util import Chat, reflections

pairs = [
    [r"hi|hello|hey", ["Hello! How can I help you today?", "Hi there! Nice to meet you.", "Hello! Welcome."]],
    [r"what is your name ?", ["My name is NLP Chatbot.", "You can call me Chatbot."]],
    [r"how are you ?", ["I am fine. Thank you for asking!", "I'm doing well."]],
    [r"what can you do ?", ["I can answer simple questions and chat with you.", "I can help you learn NLP concepts."]],
    [r"(.*) your creator ?", ["I was created using Python and NLTK."]],
    [r"(.*) machine learning (.*)", ["Machine Learning is a branch of Artificial Intelligence."]],
    [r"(.*) nlp (.*)", ["NLP stands for Natural Language Processing."]],
    [r"bye|goodbye", ["Goodbye! Have a nice day.", "Bye! See you again."]],
    [r"(.*)", ["Sorry, I don't understand that.", "Could you please rephrase your question?"]],   # default
]

print("NLP CHATBOT\nType 'bye' to exit.\n")
Chat(pairs, reflections).converse()
```

## Output
```
NLP CHATBOT
Type 'bye' to exit.

>what is your name?
My name is NLP Chatbot.
>What can I do?
Could you please rephrase your question?
>what can you do ?
I can answer simple questions and chat with you.
>bye
Bye! See you again.
```
*(From the lab manual run. Replies with several choices are picked at random, so your output may differ.)*

## Result
The rule-based chatbot answered the questions that matched its patterns and used the default reply for "What can I do?", which does not match any pattern. It ended the chat when the user typed "bye".
