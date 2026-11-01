# Experiment 11 — Flickr8k Dataset

Download the two files required for the Image Captioning experiment (InceptionV3 + LSTM).

## Dataset Downloads

1. **Flickr8k Images**  
   [Download Flickr8k_Dataset.zip](https://github.com/jbrownlee/Datasets/releases/download/Flickr8k/Flickr8k_Dataset.zip)

2. **Flickr8k Captions and Text Files**  
   [Download Flickr8k_text.zip](https://github.com/jbrownlee/Datasets/releases/download/Flickr8k/Flickr8k_text.zip)

## Extract the Files

Place both ZIP files inside your `Exp11` folder, then extract them.

### Windows CMD

```cmd
tar -xf Flickr8k_Dataset.zip
tar -xf Flickr8k_text.zip
```

## Expected Folder Structure

```text
Exp11/
├── Flicker8k_Dataset/
│   ├── image1.jpg
│   └── ...
└── Flickr8k_text/
    ├── Flickr8k.token.txt
    ├── Flickr_8k.trainImages.txt
    ├── Flickr_8k.devImages.txt
    └── Flickr_8k.testImages.txt
```

**Note:** The notebook may expect the image folder to be named `Flicker8k_Dataset` (one `r` after `Flick`). If your extracted folder is named `Flickr8k_Dataset`, update the image-directory path in the notebook or rename the folder.
