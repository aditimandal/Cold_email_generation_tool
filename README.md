# Cold Email Generation Tool

## 📌 Overview
The **Cold Email Generation Tool** is a Python-based application designed to streamline and automate the process of generating personalized cold emails. The tool utilizes **ChromaDB** for efficient storage and retrieval of relevant information, along with **Natural Language Processing (NLP)** techniques for text cleaning and optimization.

## 🚀 Features
- 📂 **Portfolio Management**: Stores and retrieves relevant tech stacks and links from a CSV file.
- 🔍 **Querying System**: Finds relevant links based on user-provided skills using **ChromaDB**.
- 🧹 **Text Cleaning Module**: Cleans input text by removing HTML tags, URLs, special characters, and excessive spaces.
- ⚡ **Efficient Data Handling**: Uses Pandas for structured data management.

## 🛠️ Technologies Used
- **Python** 🐍
- **Pandas** (for CSV data handling)
- **ChromaDB** (for vector-based storage and retrieval)
- **UUID** (for unique document identification)
- **Regular Expressions (re)** (for text cleaning)


## Project Structure
```
app/
│── resource/
│   ├── myportfolio.csv  # CSV file containing portfolio details
│── .env                 # Environment variables file
│── chains.py            # Contains job extraction and email generation logic
│── main.py              # Main script to run the application
│── portfolio.py         # Handles portfolio storage and querying using ChromaDB
│── utils.py             # Utility functions for text processing
```

---

## Installation
### Prerequisites
Ensure you have Python installed (version 3.8+ recommended).

### Clone the Repository
```bash
git clone https://github.com/yourusername/cold-email-generation.git
cd cold-email-generation
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Setup Environment Variables
Create a `.env` file in the `app/` directory and add the following:
```
GROQ_API_KEY=your_groq_api_key
```

---

## Usage
### 1. Load Portfolio Data
Run the following command to initialize the portfolio database:
```bash
python app/portfolio.py
```

### 2. Extract Jobs & Generate Emails
Execute the main script to extract job postings and generate cold emails:
```bash
python app/main.py
```

---

## How It Works
1. **Job Extraction**
   - `chains.py` processes job listings and extracts key details.
2. **Portfolio Management**
   - `portfolio.py` loads portfolio details into ChromaDB for quick retrieval.
3. **Cold Email Generation**
   - `chains.py` constructs personalized emails using extracted job data and portfolio links.
4. **Utility Functions**
   - `utils.py` provides text-processing functions for data cleaning.

---

## Technologies Used
- **Python** (3.8+)
- **LangChain** (LLM-powered text processing)
- **ChromaDB** (Vector database for portfolio storage)
- **Pandas** (CSV data processing)
- **dotenv** (Environment variable management)

---

## Future Enhancements
- Improve email personalization with AI-based sentiment analysis.
- Expand job extraction capabilities for multiple job sources.
- Implement a web interface for easy job search and email generation.

---



