# Quantitative Trading Strategy: Ensemble Meta-Labeling System  
**Internal Research Repository — Not for Public Distribution**

---

## ⚠️ Notice  
This repository is **not open-source**.  
The contents, methods, and codebase are intended **exclusively for internal team use**.  
Do not distribute or publish without explicit authorization.

---

# 1. Overview

This project implements a professional-grade **quantitative trading research architecture** for short-term stock movement prediction. It follows best practices from **Financial Machine Learning** and modern quantitative research to address the challenges of non-stationary, noisy financial data.

The system separates *signal discovery* from *bet sizing* through a two-model ensemble framework, enabling more robust and interpretable trading decisions.

---

# 2. Core Architecture: Meta-Labeling

The system uses a **Two-Stage Ensemble** design:

### **Model A — Signal Generator (High Recall)**
- Random Forest classifier  
- Purpose: Identify *potential* trading opportunities  
- High recall bias ensures minimal missed trends  
- Accepts higher false-positives intentionally  

### **Model B — Meta-Learner (Precision Filter)**
- XGBoost classifier trained on Model A’s predictions  
- Distinguishes true vs. false opportunities  
- Outputs a calibrated **probability score** used for position sizing  

---

# 3. Key Technical Components

### **Triple Barrier Method**
- Path-dependent labeling via:
  - Profit-Take barrier  
  - Stop-Loss barrier  
  - Time-Limit barrier  
- Barriers scale with volatility → dynamic adaptation  

### **Fractional Differentiation (FracDiff)**
- Makes the series stationary without destroying memory  
- Preserves long-term structure better than standard differencing  

### **Context-Aware Tiered Dataset**
Training incorporates multiple data layers:
- Broad market indices (context baseline)  
- Sector ETFs (industry context)  
- Target stock (primary features & labels)  

### **Purged Walk-Forward Validation**
Ensures realistic backtesting by:
- Purging overlapping label windows  
- Applying an embargo period  
- Preventing data leakage between folds  

### **Probabilistic Position Sizing**
- Isotonic Regression for probability calibration  
- Kelly Criterion converts probability into optimal position size  

---

# 4. System Workflow

```
          ┌──────────────────┐
          │ Market Data (YF) │
          └─────────┬────────┘
                    ▼
        ┌────────────────────────┐
        │ Feature Engineering     │
        │ (FracDiff, TA, Vol)     │
        └─────────┬──────────────┘
                  ▼
        ┌────────────────────────┐
        │ Triple Barrier Labeling │
        └─────────┬──────────────┘
                  ▼
        ┌────────────────────────┐
        │ Model A: RF (Recall)    │
        └─────────┬──────────────┘
                  ▼
        ┌────────────────────────┐
        │ Model B: XGB (Meta)     │
        └─────────┬──────────────┘
                  ▼
        ┌────────────────────────┐
        │ Calibration + Kelly     │
        └─────────┬──────────────┘
                  ▼
        ┌────────────────────────┐
        │ Trade Simulation        │
        └────────────────────────┘
```

---

# 5. Repository Structure

```text
QuantTrader_XGB/
│
├── data/
│   ├── raw/                # Immutable yfinance downloads
│   ├── processed/          # Cleaned, stationary, enriched datasets
│   └── meta/               # Sector mappings and auxiliary files
│
├── models/
│   ├── saved/              # Trained model artifacts (.joblib, .json)
│   └── logs/               # Training metrics, calibration plots
│
├── src/
│   ├── data_loader.py      # Fetching, cleaning, alignment utilities
│   ├── features.py         # FracDiff, technical indicators, macro features
│   ├── labeling.py         # Triple Barrier labeling, volatility modeling
│   ├── model_factory.py    # RF (Model A) + XGBoost (Model B) definitions
│   ├── validation.py       # Purged walk-forward CV
│   └── strategy.py         # Kelly sizing, position management
│
├── notebooks/              # Research notebooks (EDA, diagnostics)
│
├── tests/                  # Unit tests for core components
│
├── config.py               # Global settings & hyperparameters
├── main.py                 # CLI runner for workflow modes
├── requirements.txt        # Dependencies for reproduction
└── README.md               # Project documentation (this file)
```

---

# 6. Installation & Dependencies

Ensure Python **3.8+** is installed.

---

### **1. Create a Virtual Environment**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

---

### **2. Install Required Libraries**

```bash
pip install numpy pandas yfinance scikit-learn xgboost fracdiff pandas_ta matplotlib seaborn scipy joblib
```

---

### **Dependency Highlights**
- `yfinance` — data acquisition  
- `fracdiff` — fractional differentiation  
- `pandas_ta` — technical indicators  
- `xgboost` — meta-model  
- `scikit-learn` — Random Forest + metrics + calibration  
- `scipy` — Kelly calculations  
- `matplotlib / seaborn` — visualization  

---

# 7. Usage Guide

## **Step 1 — Configure the Experiment**
Modify fields in `config.py`:

- `TARGET_TICKER = "MSFT"`
- `TRAIN_START = "2000-01-01"`
- `TRAIN_END = "2020-12-31"`
- `TEST_START = "2021-01-01"`

---

## **Step 2 — Build the Dataset**

```bash
python main.py --mode data
```

This performs:

- Market data fetching  
- Volatility estimation  
- Triple Barrier labeling  
- FracDiff + feature engineering  

---

## **Step 3 — Train Models**

```bash
python main.py --mode train
```

This step:

- Trains **Model A (RF)**  
- Trains **Model B (XGBoost meta-learner)**  
- Performs purged walk-forward validation  
- Calibrates probabilities (Isotonic Regression)  
- Saves models to `/models/saved/`  

---

## **Step 4 — Run Simulation**

```bash
python main.py --mode trade --initial_capital 10000
```

Outputs include:

- Equity curve data  
- Position logs  
- Basic performance summary (Sharpe, MDD, win rate)  

---

# 8. Disclaimer

This repository is for **research and internal development only**.  
It does **not** constitute financial advice.  
Do not use this system for live trading without proper validation, risk assessment, and regulatory oversight.
