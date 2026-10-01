# Deep Learning Lab

This repository contains Python implementations for the Deep Learning Laboratory course (Code: 24AIP-C403-L401, Academic Year: 2026 – 2027).

Experiments are split into two frameworks:

- **TensorFlow/** — 5 Python scripts (Experiments 1 to 5)

## 🛠️ Environment Setup & Installation

Set up an isolated Python virtual environment and install all dependencies. Follow the steps for your OS.

### 🍏 macOS Setup

1. **Open Terminal** and navigate to the project directory:
   ```bash
   cd path/to/24AIP-C403-L401-DeepLearning
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

1. **Open Command Prompt (cmd) or PowerShell** and navigate to the folder:
   ```cmd
   cd path\to\24AIP-C403-L401-DeepLearning
   ```
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

> Once active, your terminal line starts with `(myenv)`.

---

### 📦 Install Dependencies (All Systems)

With the environment active, run:

```bash
pip install numpy opencv-python matplotlib scikit-learn tensorflow idx2numpy jupyter
```

> TensorFlow is large. On a machine **without** a CUDA GPU, pip installs the CPU version automatically — training will just be slower.

---

## 📋 List of Experiments

|   Folder   |     Exp     | Description / Objective                                                                                                      |
| :--------: | :---------: | :--------------------------------------------------------------------------------------------------------------------------- |
| TensorFlow | **1** | Basic image processing with OpenCV — histogram equalization, edge detection, augmentation, morphological ops, thresholding. |
| TensorFlow | **2** | Build & train an ANN (Keras) for MNIST digit classification.                                                                 |
| TensorFlow | **3** | Build & train a CNN for EMNIST handwritten-character classification (47 classes).                                            |
| TensorFlow | **4** | CNN face recognition on the LFW (Labeled Faces in the Wild) dataset.                                                         |
| TensorFlow | **5** | Character-level text generation using a SimpleRNN trained on Shakespeare text.                                               |

---

## 🏃 How to Run

### TensorFlow experiments (`.py` scripts)

1. Make sure your virtual environment is active.
2. Run the script with Python:
   ```bash
   python TensorFlow/Experiment-1.py
   ```

   Replace `Experiment-1.py` with the experiment you want (1–5).

---

## 📥 Dataset Sources & Download Instructions

### Experiment 1: Image Processing
- **Dataset**: Any image of your choice (e.g., `flower.jpeg`)
- **Location**: `DataBase/Exp1/flower.jpeg` (already included) or use your own image
- **How to use**: Update the `cv2.imread()` path in `Experiment-1.py` to point to your image file

### Experiment 2: MNIST Digit Classification (ANN)
- **Dataset**: MNIST (built into Keras)
- **How to use**: No download needed — `tf.keras.datasets.mnist.load_data()` downloads automatically on first run

### Experiment 3: EMNIST Handwritten Character Classification (CNN)
- **Dataset**: EMNIST Balanced dataset (47 classes)
- **Source**: [EMNIST official site](https://www.nist.gov/itl/products-and-services/emnist-dataset) or [PyTorch torchvision](https://pytorch.org/vision/stable/generated/torchvision.datasets.EMNIST.html)
- **Files needed**:
  - `emnist-balanced-train-images-idx3-ubyte.gz`
  - `emnist-balanced-train-labels-idx1-ubyte.gz`
  - `emnist-balanced-test-images-idx3-ubyte.gz`
  - `emnist-balanced-test-labels-idx1-ubyte.gz`
  - `emnist-balanced-mapping.txt` (class index → character mapping)
- **How to use**: Place all files in `DataBase/Exp3/` and update the `path` variable in `Experiment-3.py`

### Experiment 4: LFW Face Recognition (CNN)
- **Dataset**: Labeled Faces in the Wild (LFW)
- **Source**: [LFW official site](http://vis-www.cs.umass.edu/lfw/) or via `sklearn.datasets.fetch_lfw_people()`
- **How to use**: The script uses `fetch_lfw_people()` which downloads automatically on first run. Ensure `DataBase/Exp4/` exists for any local caching.

### Experiment 5: Shakespeare Text Generation (RNN)
- **Dataset**: Shakespeare's complete works (text file)
- **Source**: [Project Gutenberg](https://www.gutenberg.org/ebooks/100) — download "Plain Text UTF-8" version
- **How to use**: Save as `shakespeare.txt` in `DataBase/Exp5/` and update `file_path` in `Experiment-5.py`

---

## ⚠️ Before You Run — Fix the File Paths

The TensorFlow scripts were written on the instructor's machine and contain **hardcoded absolute paths** (e.g. `C:/Users/nagar/Desktop/DL/...`, `D:/Work/...`, `C:/Users/sathi/...`). On your machine these paths will **not exist** and the script will error.

For each experiment, open the file and change every hardcoded path to a path on your own computer:

- **Experiment-1 / 2**: point `cv2.imread(...)` at an image you have (or use the `flower.jpeg` in `DataBase/Exp1/`).
- **Experiment-3**: set `path` to your local `DataBase/Exp3/` folder containing the EMNIST `.gz` files (and the `emnist-balanced-mapping.txt`).
- **Experiment-5**: set `file_path` to the Shakespeare text file on your machine.

Inputs the scripts expect are already in the **`DataBase/`** folder — copy them next to your script or update the path to point at them.

---

## 🚪 Deactivation

When done, close the environment with:

```bash
deactivate
```
