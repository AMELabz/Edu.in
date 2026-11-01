# Deep Learning Lab

This repository contains Python implementations for the Deep Learning Laboratory course (**Code: 24AIP-C403-L401**, Academic Year **2026–2027**).

The TensorFlow experiments are documented in the [Short-Version.ipynb notebook](TensorFlow/Short-Version.ipynb). This README covers all 11 experiments in that notebook.

## Contents

- [Environment Setup](#-environment-setup)
- [Install Dependencies](#-install-dependencies)
- [List of Experiments](#-list-of-experiments)
- [Datasets and Required Files](#-datasets-and-required-files)
- [How to Run](#-how-to-run)
- [Common Notes](#-common-notes)
- [Deactivate Environment](#-deactivate-the-environment)

## 🛠️ Environment Setup

Create an isolated virtual environment from the Deep Learning project directory.

### Windows (Command Prompt)

```cmd
python -m venv myenv
myenv\Scripts\activate.bat
```

### Windows (PowerShell)

```powershell
python -m venv myenv
.\myenv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\myenv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python3 -m venv myenv
source myenv/bin/activate
```

When the environment is active, the terminal prompt displays `(myenv)`.

## 📦 Install Dependencies

With the virtual environment activated, run:

```bash
python -m pip install --upgrade pip
python -m pip install numpy opencv-python matplotlib scikit-learn tensorflow pandas nltk jupyter
```

### Package Usage

| Package | Used for |
|---|---|
| `numpy` | Numerical processing and arrays |
| `opencv-python` | Image processing |
| `matplotlib` | Images, histograms, graphs and charts |
| `scikit-learn` | Dataset loading and data splitting |
| `tensorflow` | ANN, CNN, RNN, LSTM, GAN and recommendation models |
| `pandas` | Sales data processing |
| `nltk` | Penn Treebank corpus |
| `jupyter` | Running the notebook |

**Note:** `idx2numpy` is not required. Experiment 3 reads EMNIST IDX files using Python's built-in `gzip` module and NumPy.

TensorFlow installation and training time depend on your Python version and hardware. CPU execution is supported, but training may take longer without a supported GPU.

## 📋 List of Experiments

| Exp. | Experiment | Description / Objective |
|---:|---|---|
| 1 | Image Processing (OpenCV) | Histogram equalization, histograms, Gaussian blur, Canny edge detection, augmentation, thresholding, erosion and dilation. |
| 2 | ANN on MNIST | Build and train an Artificial Neural Network for handwritten digit classification. |
| 3 | CNN on EMNIST Balanced | Classify handwritten characters across 47 classes using convolution and pooling layers. |
| 4 | CNN Face Recognition (LFW) | Recognize people from facial images using a CNN and the LFW dataset. |
| 5 | Character-level Text Generation (SimpleRNN) | Learn character patterns from Shakespeare text and generate new text. |
| 6 | IMDB Sentiment Analysis (LSTM) | Classify movie reviews as positive or negative and predict sentiment for a custom sentence. |
| 7 | POS Tagging (Encoder–Decoder LSTM) | Predict a part-of-speech tag for each word using the Penn Treebank corpus. |
| 8 | English-to-Tamil Translation (Seq2Seq LSTM) | Train an encoder–decoder model on paired English and Tamil sentences. |
| 9 | GAN Data Augmentation (Fashion-MNIST) | Generate synthetic fashion images and compare classifier performance with and without generated data. |
| 10 | Recommendation System (Embeddings) | Learn customer and product embeddings and recommend products from purchase history. |
| 11 | Image Captioning (InceptionV3 + LSTM) | Generate image descriptions using image features and an LSTM decoder trained on Flickr8k. |

## 📥 Datasets and Required Files

Some datasets download automatically through TensorFlow, Scikit-learn or NLTK. Other experiments require local files.

Place the required files in the expected working directory or update the corresponding paths in the code.

### Experiment 1 — Image Processing (OpenCV)

- **Input:** Any image, such as `Image_1.jfif`.
- **Setup:** Change the `path` variable to the location of your image.
- The code reads the image in grayscale for processing and loads it in color for augmentation.

### Experiment 2 — ANN on MNIST

- **Dataset:** MNIST handwritten digits.
- **Download:** Automatic through `tf.keras.datasets.mnist.load_data()`.
- **Manual setup:** Not required.

### Experiment 3 — CNN on EMNIST Balanced

- **Dataset:** EMNIST Balanced (47 classes).
- **Source:** [NIST EMNIST](https://www.nist.gov/itl/products-and-services/emnist-dataset).

**Required files:**

- `emnist-balanced-train-images-idx3-ubyte.gz`
- `emnist-balanced-train-labels-idx1-ubyte.gz`
- `emnist-balanced-test-images-idx3-ubyte.gz`
- `emnist-balanced-test-labels-idx1-ubyte.gz`
- `emnist-balanced-mapping.txt`

**Setup:** Place all five files in the working directory, or update the filenames and paths in the `idx()` function and mapping-file read statement.

The notebook uses `gzip` and NumPy to read the IDX files.

### Experiment 4 — CNN Face Recognition (LFW)

- **Dataset:** Labeled Faces in the Wild (LFW).
- **Source:** [LFW Official Website](http://vis-www.cs.umass.edu/lfw/).
- **Download:** Automatic through `sklearn.datasets.fetch_lfw_people(min_faces_per_person=70, resize=0.5)`.
- **Manual setup:** Not required when automatic download is available.

### Experiment 5 — Character-level Text Generation (SimpleRNN)

- **Dataset:** Shakespeare text corpus.
- **Source:** [Project Gutenberg — Complete Works of Shakespeare](https://www.gutenberg.org/ebooks/100).
- **Required file:** `shakespeare.txt`.

**Setup:** Download the plain-text UTF-8 version and place `shakespeare.txt` in the working directory, or update the file path in the code.

### Experiment 6 — IMDB Sentiment Analysis (LSTM)

- **Dataset:** IMDB movie reviews.
- **Download:** Automatic through `tf.keras.datasets.imdb.load_data(num_words=10000)`.
- **Manual setup:** Not required.

The notebook keeps the top 10,000 words and pads reviews to 200 tokens.

### Experiment 7 — POS Tagging (Encoder–Decoder LSTM)

- **Dataset:** Penn Treebank tagged sentences.
- **Download:** The notebook runs `nltk.download("treebank")` before loading the corpus.
- **Manual setup:** Not required when the NLTK download is available.

If the corpus download fails, check your internet connection and run:

```python
import nltk
nltk.download("treebank")
```

### Experiment 8 — English-to-Tamil Translation (Seq2Seq LSTM)

- **Dataset:** Tab-separated English–Tamil sentence pairs.
- **Required file:** `eng_tamil_pairs.txt`.

**Expected format:** One sentence pair per line, with English first and Tamil second, separated by a tab.

Example:

```text
Good morning.	காலை வணக்கம்.
Thank you.	நன்றி.
How are you?	நீங்கள் எப்படி இருக்கிறீர்கள்?
```

**Setup:** Place the UTF-8 encoded file in the working directory, or update the file path in the `open()` statement.

**Important:** The notebook does not download this parallel corpus automatically. Provide a suitable sentence-pair dataset before running the experiment.

### Experiment 9 — GAN Data Augmentation (Fashion-MNIST)

- **Dataset:** Fashion-MNIST.
- **Download:** Automatic through `tf.keras.datasets.fashion_mnist.load_data()`.
- **Manual setup:** Not required.

The notebook trains a Generator and Discriminator, creates 5,000 synthetic images, and compares a CNN trained on original data with one trained on augmented data.

### Experiment 10 — Recommendation System (Embeddings)

- **Dataset:** Customer purchase / sales records.
- **Required file:** `sales.csv`.

**Required columns:**

- `customer_id`
- `product_id`
- `product_name`
- `product_category`
- `quantity`
- `order_status`

**Setup:** Place `sales.csv` in the working directory, or update:

```python
pd.read_csv("sales.csv")
```

The dataset should contain completed orders with positive quantities.

The notebook removes rows with missing required values and uses customer-product pairs to create positive and negative training examples.

**Important:** The notebook does not provide or download the sales CSV. Use a dataset containing the required columns.

### Experiment 11 — Image Captioning (InceptionV3 + LSTM)

- **Dataset:** Flickr8k image-caption dataset.

**Expected directory structure:**

```text
TensorFlow/
├── Flicker8k_Dataset/
│   ├── image1.jpg
│   └── ...
└── Flickr8k_text/
    ├── Flickr8k.token.txt
    ├── Flickr_8k.trainImages.txt
    ├── Flickr_8k.devImages.txt
    └── Flickr_8k.testImages.txt
```

**Setup:** Download and extract the Flickr8k images and text files. Keep the folder names and filenames consistent with the notebook, or update `img_dir` and `txt_dir`.

**Important:** The notebook currently spells the image directory as `Flicker8k_Dataset` (one `r` after `Flick`). If your extracted folder is named `Flickr8k_Dataset`, either rename the folder or change `img_dir`.

InceptionV3 uses ImageNet weights, which are downloaded automatically the first time the model is created if they are not already cached.

## 🏃 How to Run

### Run the Reference Notebook

From the project directory, activate the virtual environment and start Jupyter:

```bash
jupyter notebook TensorFlow/Short-Version.ipynb
```

Or use JupyterLab:

```bash
jupyter lab TensorFlow/Short-Version.ipynb
```

Run the cells in order after placing the required local dataset files in the expected locations.

### Run an Individual Python Script

If the notebook has been exported into individual `.py` files, run the required script from the project directory:

```bash
python TensorFlow/Experiment-1.py
```

Replace `Experiment-1.py` with the script for the experiment you want to execute. Ensure that its dataset paths are correct.

## ⚠️ Common Notes

1. **Working directory:** Relative paths such as `Image_1.jfif`, `shakespeare.txt`, `sales.csv` and the Flickr8k folders are resolved from the current working directory.
2. **Dataset files:** Experiments 3, 5, 8, 10 and 11 need local files or folders.
3. **Automatic downloads:** Experiments 2, 4, 6, 7 and 9 use automatic dataset downloads.
4. **Internet access:** The first run may need internet access to download datasets, the NLTK corpus or InceptionV3 pretrained weights.
5. **Training time:** Experiments 8, 9 and 11 can take considerably longer because of their training loops and model size.
6. **Notebook order:** Run each experiment from its first cell and keep the required variables and data loaded before executing later cells.
7. **Outputs:** Accuracy, loss, generated text, translations, recommendations, captions and generated images depend on the dataset, environment and training run. Do not assume fixed numerical results.

## 🚪 Deactivate the Environment

When you finish, deactivate the virtual environment:

```bash
deactivate
```

## Reference

- [Short-Version.ipynb — TensorFlow Deep Learning Experiments](TensorFlow/Short-Version.ipynb)
- [Repository — AMELabz/Edu.in](https://github.com/AMELabz/Edu.in)
