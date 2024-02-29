#top salaries by country
import pandas as pd
import requests
import zipfile
import io
import matplotlib.pyplot as plt
import os

def graph_stack():

    so_data_directory = "data"

    if not os.path.exists(so_data_directory):
        os.makedirs(so_data_directory)

    #download data from stackoverflow and extract it 
    url = 'https://info.stackoverflowsolutions.com/rs/719-EMH-566/images/stack-overflow-developer-survey-2022.zip'
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(so_data_directory)

    #load to dataframe
    dw = pd.read_csv(f'{so_data_directory}/survey_results_public.csv')
    fulltime_employees = dw[dw['Employment'] == 'Employed, full-time'] #only look at Full time employees
    makes_money = fulltime_employees[pd.notnull(fulltime_employees['ConvertedCompYearly'])] #filter out null income

    #remove outliers from comptotal
    q_low = makes_money['ConvertedCompYearly'].quantile(0.1)
    q_hi = makes_money['ConvertedCompYearly'].quantile(0.9)
    makes_money_filtered = makes_money[(makes_money['ConvertedCompYearly'] < q_hi) & (makes_money['ConvertedCompYearly'] > q_low)] #filter out outliers

    #filter countries with at least 20 responses, calculate mean slary 
    makes_money_filtered = makes_money_filtered.groupby('Country').filter(lambda x: len(x) >= 20) #filter out less than 20 responses

    mean_comp_country_filtered = makes_money_filtered.groupby('Country')['ConvertedCompYearly'].mean()

    #dataframe convert and sort 
    top_mean_comp_country_df_filtered = pd.DataFrame(mean_comp_country_filtered).sort_values(by='ConvertedCompYearly', ascending=False)


    #show top 15 countries
    N = 15
    top_mean_comp_country_df_filtered = top_mean_comp_country_df_filtered.head(N)

    #plot
    plt.figure(figsize=(8, 6))  # Set the figure size
    ax = top_mean_comp_country_df_filtered.plot(kind='bar', rot=25, title='Average Salary by Country for Top 15 Countries')
    ax.set_title('Average Salary by Country for Top 15 Countries', fontsize=8)
    ax.set_ylabel('Average Salary', fontsize=7)
    ax.set_xlabel('Country', fontsize=9)
    ax.tick_params(axis='x', which='major', labelsize=6)
    ax.tick_params(axis='y', which='major', labelsize=6)

    #add the $ value of each bar into the plot 
    for bar in ax.patches:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'${bar.get_height():.0f}', 
                ha='center', va='bottom', fontsize=6)


    #shorten country names for readability 
    Q = 14
    ax.set_xticklabels([(label.get_text()[:Q] + '...') if len(label.get_text()) > Q else label.get_text() for label in ax.get_xticklabels()], ha='right')

    #add a legend to the plot
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, ['Annual Comp Converted to USD'], fontsize=6)

    # display plt
    plt.tight_layout()
    plt.show()
