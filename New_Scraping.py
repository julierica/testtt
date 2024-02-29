import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import matplotlib.pyplot as plt

# Function to scrape LinkedIn job data

def linkedInScraper(scraping_option, max_jobs):
    # URL based on scraping option
    urls = {
        'Software Engineer USA': 'https://www.linkedin.com/jobs/search/?currentJobId=3804821214&keywords=software%20engineer&origin=JOBS_HOME_KEYWORD_AUTOCOMPLETE&refresh=true',
        'Data Scientist USA': 'https://www.linkedin.com/jobs/search/?currentJobId=3823230643&geoId=103644278&keywords=data%20scientist&location=United%20States&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true',
        'Data Engineer USA': 'https://www.linkedin.com/jobs/search/?currentJobId=3827215573&geoId=103644278&keywords=data%20engineer&location=United%20States&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true',
        'Data Analyst USA': 'https://www.linkedin.com/jobs/search/?currentJobId=3823250764&geoId=103644278&keywords=data%20analyst&location=United%20States&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true',
        'Project Manager USA': 'https://www.linkedin.com/jobs/search/?currentJobId=3798672879&geoId=103644278&keywords=project%20manager&location=United%20States&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true',
    }
    url = urls.get(scraping_option, '')
    try:
        if url:
            driver = webdriver.Chrome()
            driver.get(url)

            # Scroll to load more jobs
            while len(driver.find_elements(By.CSS_SELECTOR, 'li')) < max_jobs:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

            # Extract job details
            job_lists = driver.find_element(By.CLASS_NAME, 'jobs-search__results-list')
            jobs = job_lists.find_elements(By.TAG_NAME, 'li')

            job_data = []
            for job in jobs[:max_jobs]:
                job_title = job.find_element(By.CSS_SELECTOR, 'h3').get_attribute('innerText')
                company_name = job.find_element(By.CSS_SELECTOR, 'h4').get_attribute('innerText')
                location = job.find_element(By.CSS_SELECTOR, '[class="job-search-card__location"]').get_attribute('innerText')
                date = job.find_element(By.CSS_SELECTOR, 'div>div>time').get_attribute('datetime')
                job_link = job.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')


                job_data.append({'Title': job_title, 'Company': company_name, 'Location': location, 'Date': date, 'Link': job_link})

            # Save data to CSV
            filename = f'LinkedIn_{scraping_option.replace(" ", "_")}.csv'
            job_df = pd.DataFrame(job_data)
            job_df.to_csv(filename, index=False)

            st.success(f"Scraping done for {scraping_option}, Data stored in CSV File: {filename}")
            plotGraph(filename)
        else:
            st.error('Invalid scraping option')
    except:
        st.error('Try again')


def plotGraph(filename):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(filename)

    # Count the occurrences of each location
    location_counts = df['Location'].value_counts()

    # Plot the locations
    plt.figure(figsize=(12, 12))
    location_counts.plot(kind='bar', color='skyblue')
    plt.title('Job Postings by Location')
    plt.xlabel('Location')
    plt.ylabel('Number of Job Postings')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    # Display the plot in Streamlit
    st.pyplot(plt)


# Streamlit UI
def graph_linkedin():
    st.title('LinkedIn Job Scraper')
    scraping_option = st.selectbox('Select an option:', [
        'Software Engineer USA',
        'Data Scientist USA',
        'Data Engineer USA',
        'Data Analyst USA',
        'Project Manager USA'
    ])

    if st.button('Scrape Jobs'):
        linkedInScraper(scraping_option, max_jobs=100)

 #   filename = f'LinkedIn_{scraping_option.replace(" ", "_")}.csv'
# plotGraph(filename)