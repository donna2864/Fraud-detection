# 🛡️ Fraud Detection System

A full-stack e-commerce application with an integrated machine learning pipeline for detecting potentially fraudulent transactions.

The project combines a **Python/Flask backend**, **MongoDB database**, and multiple machine learning models to analyze transaction-related features and classify transactions as legitimate or potentially fraudulent.

## ✨ Features

### 🛒 E-commerce Application

* User registration and login
* Product browsing by category
* Product details
* Shopping cart
* Checkout flow
* Order/transaction processing
* Responsive web interface

### 🔐 Fraud Detection

* Machine learning-based transaction classification
* Multiple classification models
* Ensemble-based fraud prediction
* Transaction risk analysis during checkout
* Fraudulent and successful transaction visualization
* Performance analysis of the trained models

### 📊 Model Analysis

The project includes experiments and comparisons involving:

* Logistic Regression
* Random Forest
* XGBoost
* Ensemble model
* Neural Network experimentation

Model evaluation and transaction analysis are supported through Python scripts and visualizations.

---

# 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │      Web Client      │
                         │   HTML + CSS + JS    │
                         └──────────┬───────────┘
                                    │
                                    │ HTTP Requests
                                    ▼
                         ┌──────────────────────┐
                         │     Flask Server     │
                         │       app.py         │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┼────────────────┐
                    │               │                │
                    ▼               ▼                ▼
             ┌───────────┐   ┌─────────────┐  ┌──────────────┐
             │ MongoDB   │   │ Fraud       │  │ E-commerce   │
             │ Database  │   │ Detection   │  │ Application  │
             └───────────┘   │ Pipeline    │  │ Logic        │
                             └──────┬──────┘  └──────────────┘
                                    │
                    ┌───────────────┼────────────────┐
                    │               │                │
                    ▼               ▼                ▼
             ┌────────────┐ ┌────────────┐ ┌──────────────┐
             │ Logistic   │ │ Random     │ │ XGBoost      │
             │ Regression │ │ Forest     │ │              │
             └────────────┘ └────────────┘ └──────────────┘
                                    │
                                    ▼
                           ┌─────────────────┐
                           │ Ensemble Model  │
                           └────────┬────────┘
                                    │
                                    ▼
                           ┌─────────────────┐
                           │ Fraud / Legit   │
                           │ Classification  │
                           └─────────────────┘
```

---

# 🤖 Machine Learning Approach

The fraud detection component treats transaction analysis as a **binary classification problem**:

```text
Transaction
     │
     ▼
Feature Processing
     │
     ▼
Multiple ML Models
     │
     ├── Logistic Regression
     ├── Random Forest
     └── XGBoost
     │
     ▼
Ensemble Prediction
     │
     ▼
Fraudulent / Legitimate
```

## Models Used

### Logistic Regression

Used as a baseline classification model for establishing a simple linear decision boundary.

### Random Forest

A tree-based ensemble model that can capture nonlinear relationships between transaction features.

### XGBoost

A gradient-boosting model used to model complex patterns in transaction data and improve classification performance.

### Ensemble Model

Predictions from multiple models are combined to produce a final fraud classification.

### Neural Network

A neural-network-based experiment was also implemented and evaluated as part of the model experimentation.

---

# 🔍 Fraud Detection Flow

During a transaction, relevant transaction features are processed by the fraud detection pipeline.

```text
User
 │
 ▼
Select Products
 │
 ▼
Shopping Cart
 │
 ▼
Checkout
 │
 ▼
Transaction Features
 │
 ▼
Fraud Detection Model
 │
 ├───────────────┐
 │               │
 ▼               ▼
Legitimate     Fraudulent
 │               │
 ▼               ▼
Successful      Flagged
Transaction     Transaction
```

The system can then use the model prediction to distinguish between successful and potentially fraudulent transactions.

---

# 🧰 Tech Stack

## Backend

* Python
* Flask
* MongoDB
* PyMongo

## Machine Learning

* Scikit-learn
* XGBoost
* Pandas
* NumPy
* Matplotlib

## Frontend

* HTML5
* CSS3
* JavaScript

## Machine Learning Models

* Logistic Regression
* Random Forest
* XGBoost
* Ensemble Learning
* Neural Network

## Development Tools

* Git
* GitHub
* VS Code
* Python virtual environment

---

# 📁 Project Structure

```text
Fraud_detection/
│
├── app.py
├── add_products.py
├── fraud_trial.py
│
├── pages/
│   ├── index.html
│   ├── Login.html
│   ├── SignUp.html
│   ├── cart.html
│   ├── checkout_result.html
│   ├── productPage.html
│   ├── categoryPage.html
│   ├── performance.html
│   └── additional support/
│       ├── Electronics.html
│       ├── ToysAndGames.html
│       ├── clothing.html
│       ├── healthAndBeauty.html
│       └── homeAndGarden.html
│
├── styles/
│   ├── styles.css
│   ├── cart.css
│   ├── login.css
│   ├── performance.css
│   └── ...
│
├── images/
│   ├── Fraudulent.png
│   ├── Successful.png
│   ├── chart1.jpeg
│   ├── chart2.jpeg
│   └── ...
│
├── README.md
└── .gitignore
```

> Trained model artifacts (`.pkl` and `.h5`) are excluded from the repository because some files exceed GitHub's standard file-size limit.

---

# 🚀 Getting Started

## Prerequisites

Make sure you have installed:

* Python 3.x
* pip
* MongoDB
* Git

## 1. Clone the repository

```bash
git clone https://github.com/donna2864/Fraud-detection.git
cd Fraud-detection
```

## 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

If a `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

Otherwise, install the required packages:

```bash
pip install flask pymongo pandas numpy scikit-learn xgboost matplotlib
```

## 4. Start MongoDB

Make sure your local MongoDB server is running.

The application expects a MongoDB database for storing application data and transactions.

## 5. Configure environment variables

Create a `.env` file if the application uses environment variables.

Example:

```env
MONGO_URI=mongodb://localhost:27017/fraud_detection
SECRET_KEY=your_secret_key
```

Do not commit `.env` to GitHub.

## 6. Add products

If your application requires the product database to be populated, run:

```bash
python add_products.py
```

## 7. Start the Flask application

```bash
python app.py
```

The application should then be available at:

```text
http://127.0.0.1:5000
```

---

# 📈 Model Evaluation

The repository contains visualizations generated during the model experimentation process.

These include comparisons and analysis of:

* Classification performance
* Fraudulent vs. successful transactions
* Model predictions
* Model performance metrics

The project also includes `fraud_trial.py` for experimentation and analysis of the fraud detection approach.

> Model performance can vary depending on the dataset, preprocessing, feature selection, class distribution, and evaluation methodology.

---

# 🗄️ Database

MongoDB is used as the application's database.

The database stores application-related information such as:

* User information
* Product information
* Cart/order information
* Transaction information

The fraud detection pipeline uses transaction-related data as input for classification.

---

# 🔒 Security Considerations

The project includes several security-related components:

* Authentication for users
* Password-based login
* Secret configuration through environment variables
* Fraud detection during transaction processing

Sensitive configuration files and trained model artifacts are excluded from version control using `.gitignore`.

For a production deployment, additional measures such as secure password hashing, HTTPS, input validation, rate limiting, secure session/token handling, and production-grade secrets management should be implemented.

---

# 🧠 Key Learning Outcomes

This project provided hands-on experience with:

* Building a machine learning-based fraud detection pipeline
* Integrating ML models into a web application
* Developing a Flask backend
* Working with MongoDB
* Building e-commerce workflows
* Implementing classification models
* Comparing different machine learning approaches
* Working with imbalanced fraud-detection data
* Creating data visualizations
* Connecting frontend interfaces with backend logic
* Managing ML artifacts and Git repositories

---

# 🔮 Future Improvements

Potential improvements include:

* Real-time transaction risk scoring
* More advanced feature engineering
* Better handling of highly imbalanced transaction data
* Model monitoring and drift detection
* Explainable AI for fraud predictions
* Cloud deployment
* REST API documentation
* Automated model retraining
* Secure cloud-based model storage
* More comprehensive model evaluation using precision, recall, F1-score, and ROC-AUC

---

# 👩‍💻 Author

**Donna**

Computer Science Graduate | Full-Stack & AI/ML Developer

GitHub: [@donna2864](https://github.com/donna2864)

---

## ⭐ Project

If you found this project interesting, feel free to explore the repository and give it a ⭐.
