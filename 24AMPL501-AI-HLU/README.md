# Artificial Intelligence for Human Language Understanding Lab

This repository contains Python implementations for the Artificial Intelligence for Human Language Understanding Laboratory course (Academic Year: 2026 – 2027).

---

## 🛠️ Environment Setup & Installation

Follow the steps corresponding to your operating system to set up an isolated Python virtual environment and install all necessary dependencies.

### 🍏 macOS Setup
1. **Open Terminal** and navigate to your project directory:
   ```bash
   cd path/to/your/project/folder
   ```
2. **Create the environment**:
   ```bash
   python3 -m venv myenv
   ```
3. **Activate the environment**:
   ```bash
   source myenv/bin/activate
   ```

### 🪟 Windows Setup
1. **Open Command Prompt (cmd) or PowerShell** and navigate to your folder:
   ```cmd
   cd path\(\to\your\project\folder \%\%\)MAGIT_PARSER_PROTECT%%   ```
2. **Create the environment**:
   ```cmd
   python -m venv myenv
   ```
3. **Activate the environment**:
   * *In Command Prompt:*
     ```cmd
     myenv\Scripts\activate.bat
     ```
   * *In PowerShell:*
     ```powershell
     .\myenv\Scripts\Activate.ps1
     ```

---

### 📦 Install Dependencies (All Systems)
Once your environment is active—indicated by `(myenv)` appearing at the start of your terminal line—run this single command to install all mandatory libraries needed across the entire syllabus:

```bash
pip install nltk scikit-learn gensim matplotlib pandas deep-translator textblob
python -m nltk.downloader all
```

---

## 📋 List of Syllabus Experiments

| Exp No. | Description / Objective |
| :---: | :--- |
| **1a** | Find all unigrams, bigrams, and trigrams present in a given corpus. |
| **1b** | Implement a bigram model with Add-One smoothing to calculate sentence probability. |
| **2a** | Perform tokenization by word and sentence using NLTK. |
| **2b** | Eliminate stop words using NLTK. |
| **2c** | Perform stemming and lemmatization using NLTK. |
| **3a** | Perform Parts of Speech (POS) tagging using NLTK. |
| **3b** | Implement text chunking using NLTK. |
| **4a** | Perform Named Entity Recognition (NER) using NLTK. |
| **4b** | Calculate Term Frequency and Inverse Document Frequency (TF-IDF). |
| **5** | Implement CYK Parsing (Cocke-Younger-Kasami) or Chart Parsing. |
| **6** | Train Continuous Bag of Words (CBOW) and Skip-gram Word2Vec models. |
| **7** | Analyze word relationships by finding similar words and visualizing embeddings. |
| **8** | Perform text Sentiment Analysis using NLP. |
| **9** | Build a Fake News detection system. |
| **10** | Implement a Language Translation system. |
| **11** | Develop a Next Word Prediction model using a text corpus. |
| **12** | Develop a Spam Filter framework using machine learning. |
| **13** | Design and implement a rule-based Chatbot application. |

---

## 🏃 How to Run the Programs
1. Ensure your virtual environment is active.
2. Execute your script using Python:
   ```bash
   python experiment_1.py
   ```

## 🚪 Deactivation
When you are finished working on your lab code, close the environment with:
```bash
deactivate
```


