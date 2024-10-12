# GitHub Data Dive Project

## Overview

The **GitHub Data Dive Project** aims to analyze data from GitHub repositories to uncover insights into trends, repository activity, and technology usage across various topics like Machine Learning, Data Visualization, Generative AI, and more. This project utilizes the GitHub API to extract repository details, stores the data in a PostgreSQL database, and provides an interactive Streamlit web application for visualizing the insights.

## Functionality

- **Data Extraction**: The project extracts GitHub repository data using the GitHub API, based on trending topics such as Machine Learning, Deep Learning, and others. The data includes details like repository name, stars, forks, programming language, and more.
  
- **Data Visualization**: The Streamlit application allows users to visualize various aspects of GitHub repositories using interactive charts, including top programming languages, most popular repositories, trends over time, and more.

- **Database Management**: The extracted data is stored in a PostgreSQL database, enabling efficient querying and data retrieval for analysis.

- **Dynamic Filtering**: Users can filter the visualizations based on selected topics or specific years, providing a more granular view of the data.

## Architecture

- **Frontend**: The frontend is built using Streamlit, a Python framework that allows the creation of simple, interactive web applications. Users can select topics, years, and other filters to generate relevant visualizations.
  
- **Backend**: Python scripts manage data extraction from GitHub, store data in PostgreSQL, and perform data querying and transformations for visualization. The backend handles the interaction between the frontend and the database.

- **Data Storage**: PostgreSQL is used as the database for storing the GitHub repository data. The database contains information on repository names, owners, languages, stars, forks, open issues, and more.

## Data Flow

1. **Data Extraction**: The GitHub API is used to extract repository data based on selected topics. The data is cleaned, transformed, and stored in the PostgreSQL database.

2. **Data Storage**: The cleaned and transformed data is stored in PostgreSQL with a well-defined schema. Each record includes repository details such as programming language, creation date, stars, forks, and other metrics.

3. **Data Processing**: When users interact with the Streamlit app, the backend retrieves relevant data from the database using SQL queries. The data is processed using Pandas for visualization.

4. **Visualization**: The processed data is visualized using Plotly charts. Visualizations include bar charts, pie charts, and histograms based on programming languages, topics, and repository activity.

## Usage

1. **Installation**: Clone the repository and install the required dependencies using:

   ```bash
   pip install -r requirements.txt
