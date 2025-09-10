# 🚀 NASA APOD Data Pipeline
A personal data collection and engineering project designed to scrape, store, and prepare NASA’s Astronomy Picture of the Day (APOD) metadata and images for analysis. This project is a work in progress, serving both as a learning exercise in Python, data engineering, and Git version control, and as a foundation for future data analysis.

# 📌 Project Overview

## The NASA APOD Data Pipeline automates the process of:
Scraping metadata and images from the official NASA APOD website using BeautifulSoup.\
Parsing & Normalizing the data for structured storage.\
Storing the results in a lightweight, serverless SQLite database for portability and ease of setup.\
Version Controlling the codebase with Git, including documentation, commits, and remote pushes.

## 🛠️ Tech Stack
Languages: Python, Bash Scripting, and limited SQL/regex integrated into project code\
Libraries & Tools: BeautifulSoup (bs4), SQLite3, requests, re (regex), tqdm (progress bar), Git (basic version control)\
Planned Additions: Pandas, NumPy, Jupyter Notebooks (for analysis)

## 📂 Project Structure
<pre>
nasa-apod-pipeline/
│
├── data/                # SQLite database and downloaded images
├── notebooks/           # Planned Jupyter notebooks for analysis
├── src/                 # Python scripts for scraping and parsing
├── README.md            # Project documentation
└── requirements.txt     # Python dependencies
</pre>
## ⚙️ How It Works
Scraping: Retrieves APOD pages and extracts metadata (link, image URL, title, date, author, credit, description) using BeautifulSoup.
Storage: Saves parsed data into a normalized SQLite database for lightweight, portable querying.

## 📊 Planned Next Steps
Data Analysis – Use Pandas and NumPy in Jupyter Notebooks to explore:
* Trends in image types (e.g., telescope images vs. photographs)
* Frequency of specific astronomical subjects
* Patterns and changes in metadata over time

Visualization – Create charts and graphs with Matplotlib and/or Seaborn to present findings in a clear, engaging way.\
Automation – Implement periodic scraping using schedule or APScheduler to continuously collect and update APOD data.

## 🎯 Learning Goals
Strengthen Python scripting and data parsing skills.
Gain hands-on experience with database design and normalization.
Apply Git workflows in a real project.
Build a foundation for data analysis and visualization.
