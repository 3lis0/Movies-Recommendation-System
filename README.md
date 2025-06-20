#  🎬 Movies-Recommendation-System

This project is a movie recommender system built using the MovieLens dataset. It includes two main features: personalized user recommendations using collaborative filtering models like Factorization Machines and LightFM, and item-based similarity recommendations using cosine similarity. A user-friendly dashboard allows users to explore top-N movie recommendations, view other users' preferences, and interact with movie metadata. This system is designed for educational purposes and demonstrates a complete pipeline—from data processing to model deployment. 

## 👥 Team Members

- **Israa Abdelghany**  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/israa-abdelghany/) [![GitHub](https://img.shields.io/badge/GitHub-Profile-black?style=flat&logo=github)](https://github.com/IsraaAbdelghany9)

- **Ali Adel**  
  [![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/ali-adel-84b390101) [![GitHub](https://img.shields.io/badge/GitHub-Profile-black?style=flat&logo=github)](https://github.com/adelian14)

- **Ali Salama**  
  [![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/ali-salama) [![GitHub](https://img.shields.io/badge/GitHub-Profile-black?style=flat&logo=github)](https://github.com/3lis0)

- **Omar Ayman**  
  [![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/omar-elgema3y) [![GitHub](https://img.shields.io/badge/GitHub-Profile-black?style=flat&logo=github)](https://github.com/OmarrAymann)


## 📌 Objective

Build an interactive system that:
- Recommends top-N items to a selected user using advanced recommendation models.
- Displays movie metadata and retrieves similar items based on similarity scores
- Allows users to browse others' preferences for inspiration (inspired by apps like Spotify/Anghami)
- Offers intuitive UI for navigating recommendations


## 📁 Dataset

- **Source**: [MovieLens  Dataset (100k ratings)](https://grouplens.org/datasets/movielens/)
- **Contents**:
  - `user_metadata.csv`: User IDs and avg ratings, ..etc
  - `movies.csv`: Movie metadata (title, genres)
  - `ratings.csv`: User-item rating matrix
  - `new_movies.csv`: Preprocessed movie features (before feature selection)
  - `movies_feature_engineered.csv`: Output of feature selection used in models

> 📌 As part of the preprocessing phase, we performed **feature selection** on the `new_movies.csv` file to extract relevant numerical and genre-based features.  
> The output is saved in `movies_feature_engineered.csv` and later used in content-based and hybrid recommendation models.



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


## 🖥️ UI Components

### 🔸 Movies Page (Home)
- **Genre Filter**: Filter movies using the genre dropdown.
- **Sort Options**: Sort by rating in ascending/descending order.
- **Navigation Bar**:
  - Before login: `Login` and `Sign Up` buttons.
  - After login: shows username and `Logout` button.
- **Movie Cards** display:
  - Poster, title, release year, genres, and average rating.

### 🔸 Movie Details Page
- When you open any movie:
  - You can **rate it directly**.
  - You will see a **“You May Also Like”** section below it with related/similar movies based on content or collaborative filtering.

### 🔸 Users List Page
- Explore a list of public users (`User1`, `User2`, etc.).
- View their top-rated movies and rating behavior.
- Feature inspired by social discovery systems (e.g., **Spotify**, **Anghami**), where you can explore others' preferences.

### 🔸 Profile Page *(Coming Soon 🚧)*
- The tab is shown in the navbar but not functional yet.
- Planned features:
  - View your full rating history
  - See insights like average rating, preferred genres, etc.


## Project Structure

```bash 
Movies-Recommendation-System/
├── app/                          # Main application code
│   ├── __init__.py
│   ├── models.py
│   ├── db.sqlite3                # Local SQLite DB (optional)
│
│   ├── recommender/             # Recommendation models and logic
│   │   ├── recommender.py
│   │   ├── svd_model.pkl
│   │   ├── cosine_similarity/
│   │   ├── factorization_model/
│   │   └── lightFM_model/
│
│   ├── routes/                  # Flask route handlers (blueprints)
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── homepage.py
│   │   ├── movie.py
│   │   ├── user.py
│   │   └── users.py
│
│   ├── templates/               # HTML templates (Jinja2)
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── movie.html
│   │   ├── user.html
│   │   ├── users.html
│   │   └── partials/            # Reusable HTML snippets
│
│   ├── utils/                   # Data processing helpers
│       ├── helpers.py
│       ├── image_info.py
│       ├── loader.py
│       ├── movie_processor.py
│       ├── ratings.py
│       └── user_processor.py
│
├── data/                        # Datasets (movies, ratings, metadata)
│   ├── movies.csv
│   ├── ratings.csv
│   ├── tags.csv
│   └── ...                      # Other processed CSVs
│
├── NoteBooks/                   # Test & experimentation notebooks 📓
│   └── ...                      # (Notebooks used during development)
│
├── scripts/                     # Utility scripts
│   └── init_db.py
│
├── run.py                       # Main entry point
├── requirements.txt             # Project dependencies
├── runtime.txt                  # Deployment config (e.g., Heroku)
├── README.md                    # Project documentation
└── tests/                       # (Optional) Unit test folder
``` 


## ▶️ How to Run the App

Activate the conda environment
```bash
conda activate myenv
```

Run the Flask app
```bash
python run.py
```


## 📽️ Demo

Here’s a brief walkthrough of how the system works:

- 🔐 **Logged in** using our secure authentication system  
- 🎞️ **Explored movies** like _Interstellar_ (a personal favorite!) and _Harry Potter_ (who doesn’t love it?)  
- ⭐ **Rated movies** directly from the interface  
- 🎯 **You may also like** section appears under each movie with smart recommendations based on rating and similarity scores.
- 👤 **"Profile" tab** — _Feature coming soon, insha’Allah!_ It will display personal rating history, stats, and personalized insights

📺 **[Watch the demo video →](#)**  



## 🔮 What’s Next

- 👤 **User Profile Page**: View rating history, average ratings, and genres preference  
- 📊 **Dashboard Insights**: User-specific charts showing top genres, rating trends  
- 🌐 **Public Deployment**: Stable hosted version for public access  
