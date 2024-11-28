# Image Comparison and Analysis Tool

## Introduction

The **Image Comparison and Analysis Tool** is a user-friendly application designed to provide a suite of image processing and analysis features through a graphical user interface (GUI) built with [Gradio](https://gradio.app). This tool allows users to perform various operations on images, such as comparing, blending, subtracting, and analyzing images for specific features like noise artifacts, text, signatures, and edges.

![GUI](https://github.com/user-attachments/assets/b0ac196a-918b-4126-960b-910d7464c4ae)

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [General Workflow](#general-workflow)
  - [Feature Descriptions](#feature-descriptions)
- [Use Cases](#use-cases)
  - [Noise Artifacts Extraction](#noise-artifacts-extraction)
  - [Text Extraction](#text-extraction)
  - [Signature Extraction](#signature-extraction)
  - [Canny Edge Detection](#canny-edge-detection)
- [Examples](#examples)
- [License](#license)
- [Contributing](#contributing)

---

## Features

### Image Operations

- **Resize Target to Match Reference**: Resizes the target image to match the dimensions of the reference image.

- **Add Images**: Adds the pixel values of the target image to the reference image.

- **Subtract Images**: Subtracts the pixel values of the target image from the reference image.

- **Blend Images**: Blends the reference and target images together using a specified alpha value.

- **Edge Detection on Reference**: Applies an edge detection filter to the reference image.

- **Histogram Comparison**: Compares the histograms of the reference and target images and provides a difference metric.

### Advanced Options

- **Flip Operation Order**: Flips the order of operations so that operations are performed as "Target Operation Reference" instead of the default "Reference Operation Target".

- **View Alpha Layers**: Displays the alpha (transparency) layers of the images.

- **Use Alpha Layer Only for Operations**: Performs operations using only the alpha layers of the images.

- **Invert Reference/Target Image**: Inverts the colors of the reference or target image before performing the primary operation.

- **Save Inverted Images**: Saves the inverted reference or target images to the specified output directory.

- **Create Blank Reference/Target Image**: Creates a blank (white) reference or target image matching the dimensions of the opposite image.

---

## Installation

### Prerequisites

- [Anaconda or Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed on your system.

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/image-comparison-tool.git
   cd image-comparison-tool
2. **Set setup & run script permissions**

   ```bash
   # if on linux or macOS, make the shell scripts executable
   chmod +x run_tool.sh setup_env.sh
3. **Setup & Run Scripts**
   - windows users : use the .bat files
   - linux users : use the .sh files

