from github import Github
import pandas as pd

def github_data_extraction(token,topics):
    # Initialize GitHub API client
    g = Github(token)

    # Search for repositories by topic
    # topics = ["machine learning", "deep learning", "NLP", "data visualization", "LLM", "GenAI"]

    # Creating an empty list for loading all the extracted data 
    data = []
    # Fetching necessary details
    for topic in topics:
        #search for repositories wrt each topic  
        repos = g.search_repositories(query=f'topic:{topic}')

        #Fetch necessary details and append to data list 
        for repo in repos[:500]:  # limiting to top 200 repos
            data.append({
                "Topic": topic,
                "Repository_Name": repo.name,
                "Owner": repo.owner.login,
                "Description": repo.description,
                "URL": repo.html_url,
                "Programming_Language": repo.language,
                "Creation_Date": repo.created_at,
                "Last_Updated_Date": repo.updated_at,
                "Number_of_Stars": repo.stargazers_count,
                "Number_of_Forks": repo.forks_count,
                "Number_of_Open_Issues": repo.open_issues_count,
                "License_Type": repo.license.spdx_id if repo.license else None
            })


    # storing the information retrieved from Github to a dataframe
    github_df=pd.DataFrame(data)

    # Checking for duplicates and removing from the dataframe
    if github_df.duplicated().sum()>0:
        github_df.drop_duplicates(inplace=True)
    
    # Reset the index after dropping the duplicates 
    github_df.reset_index(drop=True,inplace=True)

    # Checking for NaN values in the dataframe 
    Nan_columns=github_df.isna().sum()[github_df.isna().sum()>0].index

    if len(Nan_columns)>0:
        ## Filling the NaN values with 'Unknown'
        for features in Nan_columns:
            github_df[features].fillna('Unknown',inplace=True)
    
    return github_df


