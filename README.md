#  🎬 Movies-Recommendation-System

 This project is a movie recommender system built using the MovieLens dataset. It includes two main features: personalized user recommendations using advanced models like Neural Collaborative Filtering,  
 and item-based similarity recommendations using cosine similarity. A user-friendly dashboard allows users to view their top-N recommended movies, explore item metadata, and find similar items. The 
 system is designed for educational purposes and demonstrates the full pipeline—from data preprocessing and model training to interactive UI deployment.


## 📌 Objective

Build an interactive system that:
- Recommends top-N items to a selected user using advanced recommendation models.
- Shows item-level metadata and retrieves similar items using an item similarity engine.
- Offers intuitive UI components for navigating through both user and item recommendations.

---

## ⚙️ Environment Setup with Conda

> We used **conda** because `pip` alone can't manage different Python versions smoothly. `conda` allows creating isolated environments with specific Python versions, avoiding conflicts.

### 🔹 Step 1: Install Conda (Miniconda)
- Download Miniconda: https://docs.conda.io/en/latest/miniconda.html
- Choose the version for your OS (Linux/macOS/Windows)

### 🔹 Step 2: Create a virtual environment with Python 3.9
```bash
conda create -n myenv python=3.9
```

### 🔹 Step 3: Activate the environment
```bash
conda activate myenv
```


## Installation

### Install the required packages

```bash
$ pip install -r requirements.txt
```

---
## Models & Techniques

### 🔹 User Recommender
- **Model**: Factorization Machines / Neural Collaborative Filtering (NCF)
- **Training**: Offline on historical user-item interactions
- **Deployment**: Loaded into the dashboard for on-demand prediction
- **Output**: Top-N personalized movie recommendations for a given user

### 🔹 Item Similarity
- **Technique**: Content-based filtering or collaborative similarity measures (e.g., cosine similarity)
- **Runtime**: Computed dynamically when an item is selected
- **Output**: Top-N similar items for the selected movie

---

## UI Components

### 🔸 User Page
- **User Selector**: Dropdown to choose from unique user IDs
- **User History View**: Displays previously rated items and ratings
- **Top-N Parameter**: Input to choose how many recommendations to display per page
- **Recommendations Viewer**: Paginated list of recommended items
- **Navigation Controls**: Buttons for next/previous pages and direct page jumps

### 🔸 Item Page
- **Item Selector**: Dropdown to choose from available items
- **Item Profile**: Displays metadata (e.g., title, genre, year)
- **Top-N Similar Items**: Paginated list of most similar items
- **Navigation Controls**: Navigate through similar item suggestions

---

## 📁 Dataset

- **Source**: [MovieLens  Dataset (100k ratings)](https://grouplens.org/datasets/movielens/)
- **Contents**:
  - `users.csv`: User IDs and demographics
  - `movies.csv`: Movie metadata (title, genres)
  - `ratings.csv`: User-item rating matrix

---


