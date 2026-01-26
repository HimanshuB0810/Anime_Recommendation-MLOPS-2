---
title: Hybrid Anime Recommender
emoji: 📉
colorFrom: indigo
colorTo: green
sdk: docker
pinned: false
---

---

# Anime Recommendation System 📉

A production-ready Content-Based Recommendation System that suggests anime titles based on user-selected genres. This project demonstrates a complete **MLOps** workflow, including data versioning with **DVC**, containerization with **Docker**, and a web interface built with **Flask**.

## 🚀 Overview

The system filters and recommends anime by analyzing genre patterns within the dataset. It is architected to handle modular data pipelines and is ready for cloud deployment.

### Key Features:

* **Content-Based Filtering**: Recommends anime by matching user-selected genres against the dataset.
* **MLOps Pipeline**: Includes structured stages for data ingestion, processing, and model training.
* **Data Versioning**: Uses **DVC** to manage and version large datasets via S3/MinIO.
* **Containerized**: Fully Dockerized for "build once, run anywhere" consistency.
* **Web Interface**: A Flask-based UI for real-time interaction.

---

## 🛠️ Tech Stack

* **Language**: Python 3.10
* **Web Framework**: Flask
* **Data Science**: Pandas, NumPy, Scikit-learn
* **Deep Learning**: TensorFlow
* **Data Management**: DVC, MinIO/S3
* **Infrastructure**: Docker

---

## 📂 Project Structure

```text
├── config/
│   └── config.yaml          # Parameters for data and model training
├── notebook/
│   └── anime_final.ipynb    # Exploratory Data Analysis and prototyping
├── pipeline/
│   ├── training_pipeline.py # Script to execute the training workflow
│   └── predication_pipeline.py # Genre-based recommendation logic
├── src/
│   ├── data_ingestion.py    # Retrieves data from remote storage
│   ├── data_processing.py   # Cleans and prepares genre features
│   └── model_training.py    # Training logic for recommendation embeddings
├── templates/
│   └── index.html           # Frontend for genre selection
├── application.py           # Flask server entry point
├── Dockerfile               # Container configuration
└── requirements.txt         # Project dependencies

```

---

## ⚙️ Configuration

The project uses `config/config.yaml` to manage environment-specific settings:

* **Data**: Defines the S3 bucket and filenames (e.g., `anime.csv`).
* **Model**: Configures hyperparameters like `embedding_size`, `learning_rate`, and `optimizer` (Adam).

---

## 🚀 Getting Started

### Installation

1. **Clone the repository**:
```bash
git clone <your-repo-link>
cd Anime_Recommendation-MLOPS

```


2. **Install dependencies**:
```bash
pip install -r requirements.txt

```


3. **Run the application**:
```bash
python application.py

```


Access the UI at `http://localhost:7860`.

---

## 🐳 Docker Deployment

To build and deploy using the provided `Dockerfile`:

1. **Build image**:
```bash
docker build -t anime-app .

```


2. **Run container**:
```bash
docker run -p 7860:7860 anime-app

```



---

## 📊 Recommendation Logic

The current version utilizes **Genre-based Filtering**. The `predication_pipeline.py` processes the user's genre input and returns the most relevant anime titles from the dataset.

---

**Author**: [Himanshu Borikar]