import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


def plot_dataword():
    url = 'https://query.data.world/s/n6x7ku2oooggzxrm4ewpzddpdtfamn?dws=00000'
    dw = pd.read_csv(url)

    # Replace non-numeric values with zero
    dw['Salary Range From'] = pd.to_numeric(dw['Salary Range From'], errors='coerce').fillna(0)
    dw['Salary Range To'] = pd.to_numeric(dw['Salary Range To'], errors='coerce').fillna(0)

    dw['Average Salary'] = (dw['Salary Range From'] + dw['Salary Range To']) / 2

    # remove a few odd salaries
    dw = dw[dw['Average Salary'] >= 1000]

    gov_engineer_jobs = dw[dw['Business Title'].str.contains('Engineer', case=False)]

    # vertical line calculation
    overall_avg_salary = gov_engineer_jobs['Average Salary'].mean()

    st.dataframe(gov_engineer_jobs[['Business Title','Agency','Salary Range From', 'Salary Range To']])

    # Display job postings:
    #print(gov_engineer_jobs[['Business Title','Agency','Salary Range From', 'Salary Range To']])

    # Plot
    plt.figure(figsize=(10, 6))
    plt.hist(gov_engineer_jobs['Average Salary'], bins=20, color='skyblue', edgecolor='black')
    plt.axvline(x=overall_avg_salary, color='red', linestyle='--', linewidth=2, label='Overall Average Salary')
    plt.xlabel('Average Salary')
    plt.ylabel('Number of Jobs')
    plt.title('Distribution of Average Salaries for Government Engineer Jobs')
    plt.legend()
    plt.grid(True)
    plt.show()

    