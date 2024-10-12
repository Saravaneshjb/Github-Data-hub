import github_data_extraction as ge
import postgresql_connector as db
import plotly.express as px
import streamlit as st
import pandas as pd

def data_extract_load(token, topics):
    st.info("Github data Extraction Process started")

    # Extract the data via the GitHub API
    github_df = ge.github_data_extraction(token, topics)
    st.success(f"Data extracted successfully with {github_df.shape[0]} records.")

    st.info("Data load to DB started !!!")
    # Establish the database connection
    data_loader = db.Dataload()

    # Create the table structure if it does not exist already
    conn = data_loader.create_connection()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS github_repos (
        id SERIAL PRIMARY KEY,
        Topic VARCHAR(255),
        Repository_Name VARCHAR(255),
        Owner VARCHAR(255),
        Description TEXT,
        URL VARCHAR(255),
        Programming_Language VARCHAR(255),
        Creation_Date TIMESTAMP,
        Last_Updated_Date TIMESTAMP,
        Number_of_Stars INT,
        Number_of_Forks INT,
        Number_of_Open_Issues INT,
        License_Type VARCHAR(255)
    );
    """
    data_loader.execute_query(conn, create_table_query)

    # Load the extracted data into the PostgreSQL table
    st.info("Loading the data into the database")
    data_loader.load_df(github_df, 'github_repos')
    st.success("Data load to DB completed.")

# Function to create visualizations from the data in the database
def create_visualizations(selected_topics=None, selected_years=None):
    data_loader = db.Dataload()

    # Filter query based on selections
    query_filter = ""
    if selected_topics:
        quoted_topics = ', '.join([f"'{t}'" for t in selected_topics]) 
        query_filter += f"WHERE topic IN ({quoted_topics})"


    if selected_years:
        if query_filter:
            query_filter += f"AND EXTRACT(YEAR FROM creation_date) IN ({', '.join([str(y) for y in selected_years])}) "
        else:
            query_filter += f"WHERE EXTRACT(YEAR FROM creation_date) IN ({', '.join([str(y) for y in selected_years])}) "

    # Top 10 Programming Languages Used
    query_lang = f"SELECT programming_language, COUNT(*) as count FROM github_repos {query_filter} GROUP BY programming_language ORDER BY count DESC LIMIT 10;"
    print(f"The query generated is {query_lang}")
    df_lang = data_loader.read_sql(query_lang)
    if not df_lang.empty:
        st.info("Top 10 Programming Languages")
        fig_lang = px.bar(df_lang, x='programming_language', y='count', title="Top 10 Programming Languages")
        st.plotly_chart(fig_lang)

    # Top 10 Repos Based on License Type
    query_license = f"SELECT license_type, COUNT(*) as count FROM github_repos {query_filter} GROUP BY license_type ORDER BY count DESC LIMIT 10;"
    df_license = data_loader.read_sql(query_license)
    if not df_license.empty:
        st.info("Top 10 Repos by License Type")
        fig_license = px.bar(df_license, x='license_type', y='count', title="Top 10 Repos by License Type")
        st.plotly_chart(fig_license)

    # Top 10 Repos Based on Number of Forks
    query_forks = f"SELECT repository_name, number_of_forks FROM github_repos {query_filter} ORDER BY number_of_forks DESC LIMIT 10;"
    df_forks = data_loader.read_sql(query_forks)
    if not df_forks.empty:
        st.info("Top 10 Repos by Forks")
        fig_forks = px.bar(df_forks, x='repository_name', y='number_of_forks', title="Top 10 Repos by Forks")
        st.plotly_chart(fig_forks)

    # Top 10 Repos Based on Number of Stars
    query_stars = f"SELECT repository_name, number_of_stars FROM github_repos {query_filter} ORDER BY number_of_stars DESC LIMIT 10;"
    df_stars = data_loader.read_sql(query_stars)
    if not df_stars.empty:
        st.info("Top 10 Repos by Stars")
        fig_stars = px.bar(df_stars, x='repository_name', y='number_of_stars', title="Top 10 Repos by Stars")
        st.plotly_chart(fig_stars)

    # Top 10 Repos Based on Open Issues
    query_issues = f"SELECT repository_name, number_of_open_issues FROM github_repos {query_filter} ORDER BY number_of_open_issues DESC LIMIT 10;"
    df_issues = data_loader.read_sql(query_issues)
    if not df_issues.empty:
        st.info("Top 10 Repos by Open Issues")
        fig_issues = px.bar(df_issues, x='repository_name', y='number_of_open_issues', title="Top 10 Repos by Open Issues")
        st.plotly_chart(fig_issues)

    # Pie Chart for Programming Language Distribution
    query_lang_dist = f"SELECT programming_language, COUNT(*) as count FROM github_repos {query_filter} GROUP BY programming_language;"
    df_lang_dist = data_loader.read_sql(query_lang_dist)
    if not df_lang_dist.empty:
        st.info("Programming Language Distribution")
        fig_lang_dist = px.pie(df_lang_dist, names='programming_language', values='count', title="Programming Language Distribution")
        st.plotly_chart(fig_lang_dist)

    # Pie Chart for Topic Distribution
    query_topic_dist = f"SELECT topic, COUNT(*) as count FROM github_repos {query_filter} GROUP BY topic;"
    df_topic_dist = data_loader.read_sql(query_topic_dist)
    if not df_topic_dist.empty:
        st.info("Topic Distribution")
        fig_topic_dist = px.pie(df_topic_dist, names='topic', values='count', title="Topic Distribution")
        st.plotly_chart(fig_topic_dist)


    # Histogram for Topics Over the Years
    query_trend_topic = f"SELECT topic, CAST(EXTRACT(YEAR FROM creation_date) AS INT) as year, COUNT(*) as count FROM github_repos {query_filter} GROUP BY topic, year;"
    df_trend_topic = data_loader.read_sql(query_trend_topic)

    # Check if the dataframe is valid
    if df_trend_topic is not None and not df_trend_topic.empty:
        st.info("Topic Trend Over the Years (Histogram)")
        
        # Ensure 'year' is treated as a category
        df_trend_topic['year'] = df_trend_topic['year'].astype(str)
        
        # Plot the histogram
        fig_hist_topic = px.histogram(
            df_trend_topic, 
            x='year', 
            y='count', 
            color='topic', 
            title="Topic Trend Histogram Over the Years", 
            category_orders={"year": sorted(df_trend_topic['year'].unique())}
        )
        
        # Display the chart
        st.plotly_chart(fig_hist_topic)


    # Data Table
    st.info("Data Table")
    query_table = f"SELECT * FROM github_repos {query_filter} LIMIT 100;"
    df_table = data_loader.read_sql(query_table)
    if not df_table.empty:
        st.dataframe(df_table)

# Streamlit Page Config
st.set_page_config(page_title="GitHub Data Dive", layout="wide")

# Sidebar Navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Home", "Extract Data", "Visualize Data"])

# Home Page
if selection == "Home":
    st.title("GitHub Data Dive")
    st.write("""
        Welcome to the GitHub Data Dive application. This app allows you to:
        - Extract data from GitHub repositories based on trending topics.
        - Visualize the extracted data using interactive charts.
        
        ## Workflow:
        1. Extract data from GitHub by entering the topics of interest.
        2. Visualize the data extracted using charts and graphs.
        
        ### About Me:
        Saravanesh - Data Science Enthusiast with experience in building interactive data applications.
    """)

# Data Extraction Page
elif selection == "Extract Data":
    st.title("GitHub Data Extraction")
    
    # User input for topics
    topics_input = st.text_input("Enter topics (comma-separated):", "")
    token_input = st.text_input("Enter GitHub Token:", type="password")

    # Extract Data Button
    if st.button("Extract Data"):
        if topics_input and token_input:
            topics = [topic.strip() for topic in topics_input.split(",")]
            data_extract_load(token_input, topics)
        else:
            st.error("Please provide both topics and GitHub token.")
    
# Visualization Page
elif selection == "Visualize Data":
    st.title("Visualize GitHub Data")
    
    # Check if data exists in the database
    data_loader = db.Dataload()
    query = "SELECT COUNT(*) as count_of_lang FROM github_repos;"
    df_count = data_loader.read_sql(query)

    # Fetch distinct topics and years for dropdowns
    query_topics = "SELECT DISTINCT topic FROM github_repos;"
    query_years = "SELECT DISTINCT EXTRACT(YEAR FROM creation_date) as year FROM github_repos ORDER BY year DESC;"
    
    df_topics = data_loader.read_sql(query_topics)
    df_years = data_loader.read_sql(query_years)
    
    if df_count.iloc[0, 0] > 0:
        st.success(f"Data found in the database. Total records: {df_count.iloc[0, 0]}")
        # Ensure data is available for dropdowns
        if df_topics.empty or df_years.empty:
            st.warning("No data available in the database. Please extract data first.")
        else:
            # Multi-select dropdowns for Topics and Years
            selected_topics = st.multiselect("Select Topics", df_topics['topic'].tolist(), default=df_topics['topic'].tolist())
            selected_years = st.multiselect("Select Years", df_years['year'].astype(int).tolist(), default=df_years['year'].astype(int).tolist())
            # Button to trigger visualizations based on selections
            if st.button("Apply Filters"):
                create_visualizations(selected_topics, selected_years)
    else:
        st.warning("No data available in the database. Please extract data first.")
