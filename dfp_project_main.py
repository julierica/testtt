
import requests
import json
import prettytable

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import DatWorldJobs as dw
import New_Scraping as ns
import stackoverflow_plot as stack



def graph_bls():
    #seriesID='WMU48000001020000001512522500'
   # newSeris='NWU489909920200001510300009000'
    #n='NWU489909920200000000000009000'
    #m='NWU009999920200000000002505000'
    hourMedianWageTexas='OEUS480000000000015125208'
    hour10thWageTexas='OEUS480000000000015125206'
    hour25thWageTexas='OEUS480000000000015125207'
    hour75thWageTexas='OEUS480000000000015125209'
    hour90thWageTexas='OEUS480000000000015125210'
    hourMeanWageTexas='OEUS480000000000015125203'

    headers = {'Content-type': 'application/json'}

    dataBLS = json.dumps({"seriesid": [hour10thWageTexas,hour25thWageTexas,hourMedianWageTexas,hour75thWageTexas,hour90thWageTexas,hourMeanWageTexas],"startyear":"2022", "endyear":"2022", "registrationkey":"ccce73d5ed9b4e828eacf99cc6ac0047"})

    p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=dataBLS, headers=headers)

    json_data = json.loads(p.text)
    dataBLSWage=[]
    if(json_data['status']=='REQUEST_NOT_PROCESSED'):
        print("yea")
        st.text("Unfortuantely BLS blocks you out if you access its data too many times per day... Wait til tmrw.")
        fig, ax = plt.subplots()
        st.pyplot(fig)

    else:
        for series in json_data['Results']['series']:
            x=prettytable.PrettyTable(["series id","year","period","value","footnotes"])
            seriesId = series['seriesID']
            for item in series['data']:
                year = item['year']
                period = item['period']
                value = item['value']
                #print(value)
                footnotes=""
                dataBLSWage.append(float(value))

        data=dataBLSWage
        plt.plot([0.1,0.25,0.5,0.75,0.9], data[:-1])
        plt.title('Graph 1')
        plt.axhline(y=data[-1], color='r', linestyle='--', label='Mean Wage from BLS')
        plt.axhline(y=59.55, color='blue', linestyle='--', label='Mean Wage from Stack Overflow')
        for x, y in zip([0.1,0.25,0.5,0.75,0.9], data[:-1]):
            plt.text(x, y, f'({y})', ha='right', va='bottom')
        st.text("This graph shows the data we collected from the Beauru of Labor Statistics, which \n displays the wage of software developers in Texas according to percentiles.\n The red line is the average wage of software developer in texas from BLS. \n The blue line is the average wage of us developers from stack overflow.")
        st.pyplot()

# Function to create graphs
def create_graph(option):
    data = [0]
    if option == 'Home':
        text="""This project is created by Zhijie Gao, Cody Campbel, Kasie Yang, Tanishq Kandoi, Rheann Erica Squeria.
                We are focused on labor statistics of software developers in
                texas.We collected data from multiple data sources.  \n
                Our first source of data is from the surveys conducted by stack_overflow. These data tells how software engineers are
                paid around the world
                Our second source of data is the Beauru of labor statistics in the US. These offical data, though limited in access, 
                provide useful insights on the salary level of software engineers specifically in texas. \n
                Our third source of data is scraped from linkedin. These data should explain the number of software engineer jobs 
                posted across different states in the US. We also found interesting relationship between the hour of a day and job
                postings. \n
                Our fourth source of data is obtained from the platform DataWorld. It provides wage statistics of government engineer
                jobs in texas: a useful comparison with software engineers in the same region. \n
                
                """
        st.markdown(f"<pre>{text}</pre>", unsafe_allow_html=True)
    elif option == 'BLS data':
        graph_bls()
        
    elif option == 'Dataworld data':
        dw.plot_dataword()
        st.text("The histogram illustrates the distribution of average salaries for government engineering \n jobs. A dashed red line indicates the overall average salary.")
        st.pyplot()
    elif option == 'Linkedin data':
        ns.graph_linkedin()
    elif option == 'StackOverflow data':
        stack.graph_stack()
        st.text("The bar plot illustrates the average wage for software developer across the world. \n. It is clear that developers in the US earn the most.")
        st.pyplot()
        


st.title('Welcome to our DFP Project!')

# This gets rid of annoying warnings in streamlit 
st.set_option('deprecation.showPyplotGlobalUse', False)
# Sidebar with options
option = st.sidebar.selectbox('Menu', ['Home','StackOverflow data', 'BLS data', 'Linkedin data', 'Dataworld data'])

create_graph(option)