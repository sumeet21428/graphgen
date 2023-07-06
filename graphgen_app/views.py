# Create your views here.
import os
import datetime
from datetime import datetime
import plotly.express as px
from django.shortcuts import redirect
from openpyxl import Workbook
from django.shortcuts import render
import plotly.graph_objects as go
from plotly.offline import plot
import numpy as np
import pandas as pd
import plotly.offline as opy
import plotly.graph_objs as go
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
from django.conf import settings
from time import sleep
import requests 

DOWNLOAD_DIRECTORY = os.path.join(settings.BASE_DIR, 'graphgen_app/files')
    
def wpi(request):
    #Code for 1st graph - WPI
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=chrome_options)

    driver.get('https://eaindustry.nic.in/download_data_1112.asp')
    # driver.implicitly_wait(1)
    wpidl = driver.find_element(By.CSS_SELECTOR, "body > div.col-md-10.offset-md-1 > div.col-md-12 > div:nth-child(2) > a")
    wpidl.click()
    # sleep(10)
    downloaded_file_path = os.path.join(DOWNLOAD_DIRECTORY, "monthly_index_202304.xls")

    driver.quit()

    WPI_ini = pd.read_excel(downloaded_file_path, sheet_name=0)
    
    column_names = WPI_ini.columns[3:]
    month_year = [datetime.strptime(col[4:], "%m%Y").strftime("%b-%Y") for col in column_names]

    WPI = pd.DataFrame()
    WPI['Month-Year'] = month_year
    comm_names = ['All Commodities', 'Primary Articles', 'Fuel and Power', 'Manufactured Products', 'Food Index']
    comm_codes = [1000000000, 1100000000, 1200000000, 1300000000, 2000000000]
    selected_rows = WPI_ini[WPI_ini['COMM_CODE'].isin(comm_codes)]

    for name, code in zip(comm_names, comm_codes):
        selected_row = selected_rows[selected_rows['COMM_CODE'] == code]
        data = selected_row.values[0, 3:]
        WPI[name] = data

    fig1 = px.line(WPI, x='Month-Year', y=WPI.columns, title='WPI Data')
    fig1.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True),
        showlegend=True,
        template='plotly_white'
    )
    graph_div1 = fig1.to_html(full_html=False, include_plotlyjs='cdn')

    WPI['Monthly_Growth_Rate'] = WPI['All Commodities'].pct_change() * 100
    WPI['6_Month_Growth_Rate'] = WPI['All Commodities'].pct_change(6) * 100
    WPI['Yearly_Growth_Rate'] = WPI['All Commodities'].pct_change(12) * 100
    WPI['Fuel and Power_Monthly_Growth'] = WPI['Fuel and Power'].pct_change() * 100
    WPI['Fuel and Power_6_Month_Growth'] = WPI['Fuel and Power'].pct_change(6) * 100
    WPI['Fuel and Power_Yearly_Growth'] = WPI['Fuel and Power'].pct_change(12) * 100
    WPI['Food Index_Monthly_Growth'] = WPI['Food Index'].pct_change() * 100
    WPI['Food Index_6_Month_Growth'] = WPI['Food Index'].pct_change(6) * 100
    WPI['Food Index_Yearly_Growth'] = WPI['Food Index'].pct_change(12) * 100

    latest_all_month_growth = round(WPI['Monthly_Growth_Rate'].iloc[-1], 1)
    latest_Fuel_and_Power_month_growth = round(WPI['Fuel and Power_Monthly_Growth'].iloc[-1], 1)
    latest_Food_Index_month_growth = round(WPI['Food Index_Monthly_Growth'].iloc[-1], 1)
    latest_all_6_month_growth = round(WPI['6_Month_Growth_Rate'].iloc[-1], 1)
    latest_Fuel_and_Power_6_month_growth = round(WPI['Fuel and Power_6_Month_Growth'].iloc[-1], 1)
    latest_Food_Index_6_month_growth = round(WPI['Food Index_6_Month_Growth'].iloc[-1], 1)
    latest_all_yearly_growth = round(WPI['Yearly_Growth_Rate'].iloc[-1], 1)
    latest_Fuel_and_Power_yearly_growth = round(WPI['Fuel and Power_Yearly_Growth'].iloc[-1], 1)
    latest_Food_Index_yearly_growth = round(WPI['Food Index_Yearly_Growth'].iloc[-1], 1)

    context1 = {
        'graph_div1': graph_div1,
        'latest_all_month_growth': latest_all_month_growth,
        'latest_Fuel_and_Power_month_growth': latest_Fuel_and_Power_month_growth,
        'latest_Food_Index_month_growth': latest_Food_Index_month_growth,
        'latest_all_6_month_growth': latest_all_6_month_growth,
        'latest_Fuel_and_Power_6_month_growth': latest_Fuel_and_Power_6_month_growth,
        'latest_Food_Index_6_month_growth': latest_Food_Index_6_month_growth,
        'latest_all_yearly_growth': latest_all_yearly_growth,
        'latest_Fuel_and_Power_yearly_growth': latest_Fuel_and_Power_yearly_growth,
        'latest_Food_Index_yearly_growth': latest_Food_Index_yearly_growth,
    }

    return render(request, 'wpi.html', context1)
    

def cpi(request):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=chrome_options)

    def File_exporter():
        reportFrame = driver.find_element(By.TAG_NAME, "iframe")
        while True:
            print("switching to", reportFrame.get_attribute("id"))
            if reportFrame.get_attribute("id") == "webiViewFrame":
                driver.switch_to.frame(reportFrame)
                break
            driver.switch_to.frame(reportFrame)

            try:
                reportFrame = driver.find_element(By.TAG_NAME, "iframe")
            except:
                break

        export = driver.find_element(By.ID, "iconmid_iconMenu_icon__dhtmlLib_239")
        export.click()

        menu = driver.find_element(
            By.ID, "iconMenu_menu__dhtmlLib_239_text__menuAutoId_3")
        menu.click()

        expo = driver.find_element(
            By.ID, "_dhtmlLib_244_span_text__menuAutoId_5")
        expo.click()

        print("clicked")
        sleep(15)

        # Assign the direct URL to downloaded_file_path
        downloaded_file_path = os.path.join(DOWNLOAD_DIRECTORY, "RBIB_Table_No._18_ _Consumer_Price_Index_(Base _2010=100)_old.xlsx")

        # Return the downloaded file path
        return downloaded_file_path
    
    driver.get("https://dbie.rbi.org.in/DBIE/dbie.rbi?site=statistics#!1_40")
    driver.implicitly_wait(20)
    timetab = driver.find_element(By.CSS_SELECTOR, "#pettabs > ul > li:nth-child(2)")
    timetab.click()
    sleep(5)
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)

    links = driver.find_elements(By.CSS_SELECTOR, "a")
    for link in links:
        print(link.get_attribute("innerText"))
    links[2].click()

    sleep(5)
    downloaded_file_path = File_exporter()
    CPI_ini = pd.read_excel(downloaded_file_path, sheet_name=1)

    data1 = CPI_ini[CPI_ini.iloc[:, 4] == 'Final'].copy()

    #CPI : Combined Current
    CPI_combined_current = pd.DataFrame()
    columns_to_copy_a = ["General Index", "Food and beverages", "Pan, tobacco and intoxicants", "Clothing and footwear",
        "Fuel and light", "Miscellaneous", "Consumer Food Price Index"]
    columns_to_copy_b = ["General Index", "Food and beverages", "Pan, tobacco and intoxicants", "Clothing and footwear", "Housing",
        "Fuel and light", "Miscellaneous", "Consumer Food Price Index"]

    for i in range(5, 11):
        datai = data1.iloc[:, [2, 3, i]].copy()
        datai.columns = ['Month-Year', 'CommDesc', 'Columni']
        datai['Columni'] = pd.to_numeric(datai['Columni'], errors='coerce')
        datai.dropna(subset=['Columni'], inplace=True)

        data_pivot = datai.pivot_table(index='Month-Year', columns='CommDesc', values='Columni').reset_index()
        data_pivot.rename(columns={
            "A) General Index": "General Index",
            "A.1) Food and beverages": "Food and beverages",
            "A.2) Pan, tobacco and intoxicants": "Pan, tobacco and intoxicants",
            "A.3) Clothing and footwear": "Clothing and footwear",
            "A.4) Housing": "Housing",
            "A.5) Fuel and light": "Fuel and light",
            "A.6) Miscellaneous": "Miscellaneous",
            "B) Consumer Food Price Index": "Consumer Food Price Index"
        }, inplace=True)

        data_pivot['Month-Year'] = pd.to_datetime(data_pivot['Month-Year'], format='%b-%Y')
        data_pivot.sort_values(by='Month-Year', inplace=True)
        data_pivot['Month-Year'] = data_pivot['Month-Year'].dt.strftime('%b-%Y')

        if i == 9:
            CPI_combined_current = data_pivot[['Month-Year'] + columns_to_copy_b].copy()

    # Create the new graph
    fig2 = px.line(CPI_combined_current, x='Month-Year', y=CPI_combined_current.columns, title='CPI Combined Current')
    fig2.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True),
        showlegend=True,
        template='plotly_white'
    )
    graph_div2 = fig2.to_html(full_html=False, include_plotlyjs='cdn')

    CPI_combined_current['Monthly_Growth_Rate'] = CPI_combined_current['General Index'].pct_change() * 100
    CPI_combined_current['6_Month_Growth_Rate'] = CPI_combined_current['General Index'].pct_change(6) * 100
    CPI_combined_current['Yearly_Growth_Rate'] = CPI_combined_current['General Index'].pct_change(12) * 100
    CPI_combined_current['Fuel and light_Monthly_Growth'] = CPI_combined_current['Fuel and light'].pct_change() * 100
    CPI_combined_current['Fuel and light_6_Month_Growth'] = CPI_combined_current['Fuel and light'].pct_change(6) * 100
    CPI_combined_current['Fuel and light_Yearly_Growth'] = CPI_combined_current['Fuel and light'].pct_change(12) * 100
    CPI_combined_current['Consumer Food Price Index_Monthly_Growth'] = CPI_combined_current['Consumer Food Price Index'].pct_change() * 100
    CPI_combined_current['Consumer Food Price Index_6_Month_Growth'] = CPI_combined_current['Consumer Food Price Index'].pct_change(6) * 100
    CPI_combined_current['Consumer Food Price Index_Yearly_Growth'] = CPI_combined_current['Consumer Food Price Index'].pct_change(12) * 100

    latest_general_month_growth_comb_current = round(CPI_combined_current['Monthly_Growth_Rate'].iloc[-1], 1)
    latest_Fuel_and_light_month_growth_comb_current = round(CPI_combined_current['Fuel and light_Monthly_Growth'].iloc[-1], 1)
    latest_Food_Index_month_growth_comb_current = round(CPI_combined_current['Consumer Food Price Index_Monthly_Growth'].iloc[-1], 1)
    latest_general_6_month_growth_comb_current = round(CPI_combined_current['6_Month_Growth_Rate'].iloc[-1], 1)
    latest_Fuel_and_light_6_month_growth_comb_current = round(CPI_combined_current['Fuel and light_6_Month_Growth'].iloc[-1], 1)
    latest_Food_Index_6_month_growth_comb_current = round(CPI_combined_current['Consumer Food Price Index_6_Month_Growth'].iloc[-1], 1)
    latest_general_yearly_growth_comb_current = round(CPI_combined_current['Yearly_Growth_Rate'].iloc[-1], 1)
    latest_Fuel_and_light_yearly_growth_comb_current = round(CPI_combined_current['Fuel and light_Yearly_Growth'].iloc[-1], 1)
    latest_Food_Index_yearly_growth_comb_current = round(CPI_combined_current['Consumer Food Price Index_Yearly_Growth'].iloc[-1], 1)
    
    

    #Code for the 3rd graph - CPI : Combined Inflyoy
    CPI_ini = pd.read_excel("graphgen_app/files/RBIB_Table_No._18_ _Consumer_Price_Index_(Base _2010=100)_old.xlsx", sheet_name=1)
    data1 = CPI_ini[CPI_ini.iloc[:, 4] == 'Final'].copy()

    CPI_combined_yoy = pd.DataFrame()
    columns_to_copy_b = ["General Index", "Food and beverages", "Pan, tobacco and intoxicants", "Clothing and footwear", "Housing",
        "Fuel and light", "Miscellaneous", "Consumer Food Price Index"]

    for i in range(5, 11):
        datai = data1.iloc[:, [2, 3, i]].copy()
        datai.columns = ['Month-Year', 'CommDesc', 'Columni']
        datai['Columni'] = pd.to_numeric(datai['Columni'], errors='coerce')
        datai.dropna(subset=['Columni'], inplace=True)

        data_pivot = datai.pivot_table(index='Month-Year', columns='CommDesc', values='Columni').reset_index()
        data_pivot.rename(columns={
            "A) General Index": "General Index",
            "A.1) Food and beverages": "Food and beverages",
            "A.2) Pan, tobacco and intoxicants": "Pan, tobacco and intoxicants",
            "A.3) Clothing and footwear": "Clothing and footwear",
            "A.4) Housing": "Housing",
            "A.5) Fuel and light": "Fuel and light",
            "A.6) Miscellaneous": "Miscellaneous",
            "B) Consumer Food Price Index": "Consumer Food Price Index"
        }, inplace=True)

        data_pivot['Month-Year'] = pd.to_datetime(data_pivot['Month-Year'], format='%b-%Y')
        data_pivot.sort_values(by='Month-Year', inplace=True)
        data_pivot['Month-Year'] = data_pivot['Month-Year'].dt.strftime('%b-%Y')

        if i == 10:
            CPI_combined_yoy = data_pivot[['Month-Year'] + columns_to_copy_b].copy()

    # Create the new graph
    fig3 = px.line(CPI_combined_yoy, x='Month-Year', y=CPI_combined_yoy.columns, title='CPI Combined Inflation - Y-o-Y')
    fig3.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True),
        showlegend=True,
        template='plotly_white'
    )
    graph_div3 = fig3.to_html(full_html=False, include_plotlyjs='cdn')
    
    # Code for the 4th graph - CPI : Rural Current
    CPI_ini = pd.read_excel("graphgen_app/files/RBIB_Table_No._18_ _Consumer_Price_Index_(Base _2010=100)_old.xlsx", sheet_name=1)
    data1 = CPI_ini[CPI_ini.iloc[:, 4] == 'Final'].copy()

    CPI_rural_current = pd.DataFrame()
    CPI_rural_inflyoy = pd.DataFrame()
    CPI_urban_current = pd.DataFrame()
    CPI_urban_inflyoy = pd.DataFrame()
    CPI_combined_current = pd.DataFrame()
    CPI_combined_yoy = pd.DataFrame()
    columns_to_copy_a = ["General Index", "Food and beverages", "Pan, tobacco and intoxicants", "Clothing and footwear",
        "Fuel and light", "Miscellaneous", "Consumer Food Price Index"]
    columns_to_copy_b = ["General Index", "Food and beverages", "Pan, tobacco and intoxicants", "Clothing and footwear", "Housing",
        "Fuel and light", "Miscellaneous", "Consumer Food Price Index"]

    for i in range(5,11):
        datai = data1.iloc[:, [2,3,i]].copy()
        datai.columns = ['Month-Year', 'CommDesc', 'Columni']
        datai['Columni'] = pd.to_numeric(datai['Columni'], errors='coerce')
        datai.dropna(subset=['Columni'], inplace=True)

        data_pivot = datai.pivot_table(index='Month-Year', columns='CommDesc', values='Columni').reset_index()
        data_pivot.rename(columns={
        "A) General Index": "General Index",
        "A.1) Food and beverages": "Food and beverages",
        "A.2) Pan, tobacco and intoxicants": "Pan, tobacco and intoxicants",
        "A.3) Clothing and footwear": "Clothing and footwear",
        "A.4) Housing": "Housing",
        "A.5) Fuel and light": "Fuel and light",
        "A.6) Miscellaneous": "Miscellaneous",
        "B) Consumer Food Price Index": "Consumer Food Price Index"
        }, inplace=True)

        data_pivot['Month-Year'] = pd.to_datetime(data_pivot['Month-Year'], format='%b-%Y')
        data_pivot.sort_values(by='Month-Year', inplace=True)
        data_pivot['Month-Year'] = data_pivot['Month-Year'].dt.strftime('%b-%Y')
        if i == 5 or i == 6:
            data_copy = data_pivot[['Month-Year'] + columns_to_copy_a].copy()
        else:
            data_copy = data_pivot[['Month-Year'] + columns_to_copy_b].copy()
        
        if i == 5:
            CPI_rural_current = data_copy
        elif i == 6:
            CPI_rural_inflyoy = data_copy
        elif i == 7:
            CPI_urban_current = data_copy
        elif i == 8:
            CPI_urban_inflyoy = data_copy
        elif i == 9:
            CPI_combined_current = data_copy
        elif i == 10:
            CPI_combined_yoy = data_copy

    fig4 = px.line(CPI_rural_current, x='Month-Year', y=CPI_rural_current.columns, title='CPI Rural Current')
    fig4.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True),
        showlegend=True,
        template='plotly_white'
    )
    graph_div4 = fig4.to_html(full_html=False, include_plotlyjs='cdn')

    CPI_rural_current['Monthly_Growth_Rate'] = CPI_rural_current['General Index'].pct_change() * 100
    CPI_rural_current['6_Month_Growth_Rate'] = CPI_rural_current['General Index'].pct_change(6) * 100
    CPI_rural_current['Yearly_Growth_Rate'] = CPI_rural_current['General Index'].pct_change(12) * 100
    CPI_rural_current['Fuel and light_Monthly_Growth'] = CPI_rural_current['Fuel and light'].pct_change() * 100
    CPI_rural_current['Fuel and light_6_Month_Growth'] = CPI_rural_current['Fuel and light'].pct_change(6) * 100
    CPI_rural_current['Fuel and light_Yearly_Growth'] = CPI_rural_current['Fuel and light'].pct_change(12) * 100
    CPI_rural_current['Consumer Food Price Index_Monthly_Growth'] = CPI_rural_current['Consumer Food Price Index'].pct_change() * 100
    CPI_rural_current['Consumer Food Price Index_6_Month_Growth'] = CPI_rural_current['Consumer Food Price Index'].pct_change(6) * 100
    CPI_rural_current['Consumer Food Price Index_Yearly_Growth'] = CPI_rural_current['Consumer Food Price Index'].pct_change(12) * 100

    latest_general_month_growth_rural_current = round(CPI_rural_current['Monthly_Growth_Rate'].iloc[-1], 1)
    latest_Fuel_and_light_month_growth_rural_current = round(CPI_rural_current['Fuel and light_Monthly_Growth'].iloc[-1], 1)
    latest_Food_Index_month_growth_rural_current = round(CPI_rural_current['Consumer Food Price Index_Monthly_Growth'].iloc[-1], 1)
    latest_general_6_month_growth_rural_current = round(CPI_rural_current['6_Month_Growth_Rate'].iloc[-1], 1)
    latest_Fuel_and_light_6_month_growth_rural_current = round(CPI_rural_current['Fuel and light_6_Month_Growth'].iloc[-1], 1)
    latest_Food_Index_6_month_growth_rural_current = round(CPI_rural_current['Consumer Food Price Index_6_Month_Growth'].iloc[-1], 1)
    latest_general_yearly_growth_rural_current = round(CPI_rural_current['Yearly_Growth_Rate'].iloc[-1], 1)
    latest_Fuel_and_light_yearly_growth_rural_current = round(CPI_rural_current['Fuel and light_Yearly_Growth'].iloc[-1], 1)
    latest_Food_Index_yearly_growth_rural_current = round(CPI_rural_current['Consumer Food Price Index_Yearly_Growth'].iloc[-1], 1)

    
    
    
    
    
    #Code for the 5th graph - CPI : Rural, inflyoy
    CPI_ini = pd.read_excel("graphgen_app/files/RBIB_Table_No._18_ _Consumer_Price_Index_(Base _2010=100)_old.xlsx", sheet_name=1)
    data1 = CPI_ini[CPI_ini.iloc[:, 4] == 'Final'].copy()

    CPI_rural_inflyoy = pd.DataFrame()
    columns_to_copy_a = ["General Index", "Food and beverages", "Pan, tobacco and intoxicants", "Clothing and footwear",
        "Fuel and light", "Miscellaneous", "Consumer Food Price Index"]
    columns_to_copy_b = ["General Index", "Food and beverages", "Pan, tobacco and intoxicants", "Clothing and footwear", "Housing",
        "Fuel and light", "Miscellaneous", "Consumer Food Price Index"]

    for i in range(5, 11):
        datai = data1.iloc[:, [2, 3, i]].copy()
        datai.columns = ['Month-Year', 'CommDesc', 'Columni']
        datai['Columni'] = pd.to_numeric(datai['Columni'], errors='coerce')
        datai.dropna(subset=['Columni'], inplace=True)

        data_pivot = datai.pivot_table(index='Month-Year', columns='CommDesc', values='Columni').reset_index()
        data_pivot.rename(columns={
            "A) General Index": "General Index",
            "A.1) Food and beverages": "Food and beverages",
            "A.2) Pan, tobacco and intoxicants": "Pan, tobacco and intoxicants",
            "A.3) Clothing and footwear": "Clothing and footwear",
            "A.4) Housing": "Housing",
            "A.5) Fuel and light": "Fuel and light",
            "A.6) Miscellaneous": "Miscellaneous",
            "B) Consumer Food Price Index": "Consumer Food Price Index"
        }, inplace=True)

        data_pivot['Month-Year'] = pd.to_datetime(data_pivot['Month-Year'], format='%b-%Y')
        data_pivot.sort_values(by='Month-Year', inplace=True)
        data_pivot['Month-Year'] = data_pivot['Month-Year'].dt.strftime('%b-%Y')

        if i == 6:
            CPI_rural_inflyoy = data_pivot[['Month-Year'] + columns_to_copy_a].copy()

    # Create the new graph
    fig5 = px.line(CPI_rural_inflyoy, x='Month-Year', y=CPI_rural_inflyoy.columns, title='CPI Rural Inflation - Y-o-Y ')
    fig5.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True),
        showlegend=True,
        template='plotly_white'
    )
    graph_div5 = fig5.to_html(full_html=False, include_plotlyjs='cdn')
    
    #Code for the 6th graph - CPI: Urban Current
    CPI_ini = pd.read_excel("graphgen_app/files/RBIB_Table_No._18_ _Consumer_Price_Index_(Base _2010=100)_old.xlsx", sheet_name=1)
    data1 = CPI_ini[CPI_ini.iloc[:, 4] == 'Final'].copy()

    CPI_urban_current = pd.DataFrame()
    columns_to_copy_a = ["General Index", "Food and beverages", "Pan, tobacco and intoxicants", "Clothing and footwear",
        "Fuel and light", "Miscellaneous", "Consumer Food Price Index"]
    columns_to_copy_b = ["General Index", "Food and beverages", "Pan, tobacco and intoxicants", "Clothing and footwear", "Housing",
        "Fuel and light", "Miscellaneous", "Consumer Food Price Index"]

    for i in range(5, 11):
        datai = data1.iloc[:, [2, 3, i]].copy()
        datai.columns = ['Month-Year', 'CommDesc', 'Columni']
        datai['Columni'] = pd.to_numeric(datai['Columni'], errors='coerce')
        datai.dropna(subset=['Columni'], inplace=True)

        data_pivot = datai.pivot_table(index='Month-Year', columns='CommDesc', values='Columni').reset_index()
        data_pivot.rename(columns={
            "A) General Index": "General Index",
            "A.1) Food and beverages": "Food and beverages",
            "A.2) Pan, tobacco and intoxicants": "Pan, tobacco and intoxicants",
            "A.3) Clothing and footwear": "Clothing and footwear",
            "A.4) Housing": "Housing",
            "A.5) Fuel and light": "Fuel and light",
            "A.6) Miscellaneous": "Miscellaneous",
            "B) Consumer Food Price Index": "Consumer Food Price Index"
        }, inplace=True)

        data_pivot['Month-Year'] = pd.to_datetime(data_pivot['Month-Year'], format='%b-%Y')
        data_pivot.sort_values(by='Month-Year', inplace=True)
        data_pivot['Month-Year'] = data_pivot['Month-Year'].dt.strftime('%b-%Y')

        if i == 7:
            CPI_urban_current = data_pivot[['Month-Year'] + columns_to_copy_a].copy()

    # Create the new graph
    fig6 = px.line(CPI_urban_current, x='Month-Year', y=CPI_urban_current.columns, title='CPI Urban Current')
    fig6.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True),
        showlegend=True,
        template='plotly_white'
    )
    graph_div6 = fig6.to_html(full_html=False, include_plotlyjs='cdn')
    CPI_urban_current['Monthly_Growth_Rate'] = CPI_urban_current['General Index'].pct_change() * 100
    CPI_urban_current['6_Month_Growth_Rate'] = CPI_urban_current['General Index'].pct_change(6) * 100
    CPI_urban_current['Yearly_Growth_Rate'] = CPI_urban_current['General Index'].pct_change(12) * 100
    CPI_urban_current['Fuel and light_Monthly_Growth'] = CPI_urban_current['Fuel and light'].pct_change() * 100
    CPI_urban_current['Fuel and light_6_Month_Growth'] = CPI_urban_current['Fuel and light'].pct_change(6) * 100
    CPI_urban_current['Fuel and light_Yearly_Growth'] = CPI_urban_current['Fuel and light'].pct_change(12) * 100
    CPI_urban_current['Consumer Food Price Index_Monthly_Growth'] = CPI_urban_current['Consumer Food Price Index'].pct_change() * 100
    CPI_urban_current['Consumer Food Price Index_6_Month_Growth'] = CPI_urban_current['Consumer Food Price Index'].pct_change(6) * 100
    CPI_urban_current['Consumer Food Price Index_Yearly_Growth'] = CPI_urban_current['Consumer Food Price Index'].pct_change(12) * 100

    latest_general_month_growth_urban_current = round(CPI_urban_current['Monthly_Growth_Rate'].iloc[-1], 1)
    latest_Fuel_and_light_month_growth_urban_current = round(CPI_urban_current['Fuel and light_Monthly_Growth'].iloc[-1], 1)
    latest_Food_Index_month_growth_urban_current = round(CPI_urban_current['Consumer Food Price Index_Monthly_Growth'].iloc[-1], 1)
    latest_general_6_month_growth_urban_current = round(CPI_urban_current['6_Month_Growth_Rate'].iloc[-1], 1)
    latest_Fuel_and_light_6_month_growth_urban_current = round(CPI_urban_current['Fuel and light_6_Month_Growth'].iloc[-1], 1)
    latest_Food_Index_6_month_growth_urban_current = round(CPI_urban_current['Consumer Food Price Index_6_Month_Growth'].iloc[-1], 1)
    latest_general_yearly_growth_urban_current = round(CPI_urban_current['Yearly_Growth_Rate'].iloc[-1], 1)
    latest_Fuel_and_light_yearly_growth_urban_current = round(CPI_urban_current['Fuel and light_Yearly_Growth'].iloc[-1], 1)
    latest_Food_Index_yearly_growth_urban_current = round(CPI_urban_current['Consumer Food Price Index_Yearly_Growth'].iloc[-1], 1)

    
    #Code for the 7th graph - CPI : Urban Infloyoy
    CPI_ini = pd.read_excel("graphgen_app/files/RBIB_Table_No._18_ _Consumer_Price_Index_(Base _2010=100)_old.xlsx", sheet_name=1)

    data1 = CPI_ini[CPI_ini.iloc[:, 4] == 'Final'].copy()

    
    CPI_urban_inflyoy = pd.DataFrame()
    
    columns_to_copy_a = ["General Index", "Food and beverages", "Pan, tobacco and intoxicants", "Clothing and footwear",
        "Fuel and light", "Miscellaneous", "Consumer Food Price Index"]
    columns_to_copy_b = ["General Index", "Food and beverages", "Pan, tobacco and intoxicants", "Clothing and footwear", "Housing",
        "Fuel and light", "Miscellaneous", "Consumer Food Price Index"]

    for i in range(5,11):
        datai = data1.iloc[:, [2,3,i]].copy()
        datai.columns = ['Month-Year', 'CommDesc', 'Columni']
        datai['Columni'] = pd.to_numeric(datai['Columni'], errors='coerce')
        datai.dropna(subset=['Columni'], inplace=True)

        data_pivot = datai.pivot_table(index='Month-Year', columns='CommDesc', values='Columni').reset_index()
        data_pivot.rename(columns={
        "A) General Index": "General Index",
        "A.1) Food and beverages": "Food and beverages",
        "A.2) Pan, tobacco and intoxicants": "Pan, tobacco and intoxicants",
        "A.3) Clothing and footwear": "Clothing and footwear",
        "A.4) Housing": "Housing",
        "A.5) Fuel and light": "Fuel and light",
        "A.6) Miscellaneous": "Miscellaneous",
        "B) Consumer Food Price Index": "Consumer Food Price Index"
        }, inplace=True)

        data_pivot['Month-Year'] = pd.to_datetime(data_pivot['Month-Year'], format='%b-%Y')
        data_pivot.sort_values(by='Month-Year', inplace=True)
        data_pivot['Month-Year'] = data_pivot['Month-Year'].dt.strftime('%b-%Y')
        if i == 5 or i == 6:
            data_copy = data_pivot[['Month-Year'] + columns_to_copy_a].copy()
        else:
            data_copy = data_pivot[['Month-Year'] + columns_to_copy_b].copy()
        
        if i == 5:
            CPI_rural_current = data_copy
        elif i == 6:
            CPI_rural_inflyoy = data_copy
        elif i == 7:
            CPI_urban_current = data_copy
        elif i == 8:
            CPI_urban_inflyoy = data_copy
        elif i == 9:
            CPI_combined_current = data_copy
        elif i == 10:
            CPI_combined_yoy = data_copy
    
    fig7 = px.line(CPI_urban_inflyoy, x='Month-Year', y=CPI_urban_current.columns, title='CPI Urban Current Data - YoY')
    fig7.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True),
        showlegend=True,
        template='plotly_white'
    )
    graph_div7 = fig7.to_html(full_html=False, include_plotlyjs='cdn')
        
    context= {
        'graph_div2': graph_div2,
        'graph_div3': graph_div3,
        'graph_div4': graph_div4,
        'graph_div5': graph_div5,
        'graph_div6': graph_div6,
        'graph_div7': graph_div7,
        'latest_general_month_growth_comb_current': latest_general_month_growth_comb_current,
        'latest_Fuel_and_light_month_growth_comb_current': latest_Fuel_and_light_month_growth_comb_current,
        'latest_Food_Index_month_growth_comb_current': latest_Food_Index_month_growth_comb_current,
        'latest_general_6_month_growth_comb_current': latest_general_6_month_growth_comb_current,
        'latest_Fuel_and_light_6_month_growth_comb_current': latest_Fuel_and_light_6_month_growth_comb_current,
        'latest_Food_Index_6_month_growth_comb_current': latest_Food_Index_6_month_growth_comb_current,
        'latest_general_yearly_growth_comb_current': latest_general_yearly_growth_comb_current,
        'latest_Fuel_and_light_yearly_growth_comb_current': latest_Fuel_and_light_yearly_growth_comb_current,
        'latest_Food_Index_yearly_growth_comb_current': latest_Food_Index_yearly_growth_comb_current,
        'latest_general_month_growth_rural_current': latest_general_month_growth_rural_current,
        'latest_Fuel_and_light_month_growth_rural_current': latest_Fuel_and_light_month_growth_rural_current ,
        'latest_Food_Index_month_growth_rural_current': latest_Food_Index_month_growth_rural_current,
        'latest_general_6_month_growth_rural_current': latest_general_6_month_growth_rural_current, 
        'latest_Fuel_and_light_6_month_growth_rural_current': latest_Fuel_and_light_6_month_growth_rural_current, 
        'latest_Food_Index_6_month_growth_rural_current': latest_Food_Index_6_month_growth_rural_current, 
        'latest_general_yearly_growth_rural_current': latest_general_yearly_growth_rural_current, 
        'latest_Fuel_and_light_yearly_growth_rural_current': latest_Fuel_and_light_yearly_growth_rural_current,
        'latest_Food_Index_yearly_growth_rural_current': latest_Food_Index_yearly_growth_rural_current,
        'latest_general_month_growth_urban_current' : latest_general_month_growth_urban_current ,
        'latest_Fuel_and_light_month_growth_urban_current' : latest_Fuel_and_light_month_growth_urban_current ,
        'latest_Food_Index_month_growth_urban_current' : latest_Food_Index_month_growth_urban_current ,
        'latest_general_6_month_growth_urban_current' : latest_general_6_month_growth_urban_current ,
        'latest_Fuel_and_light_6_month_growth_urban_current' : latest_Fuel_and_light_6_month_growth_urban_current ,
        'latest_Food_Index_6_month_growth_urban_current' : latest_Food_Index_6_month_growth_urban_current ,
        'latest_general_yearly_growth_urban_current' : latest_general_yearly_growth_urban_current ,
        'latest_Fuel_and_light_yearly_growth_urban_current' : latest_Fuel_and_light_yearly_growth_urban_current ,
        'latest_Food_Index_yearly_growth_urban_current' : latest_Food_Index_yearly_growth_urban_current,
    }
    return render(request, 'cpi.html',context) 


    
def exchange(request):
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=chrome_options)

    def File_exporter():
        reportFrame = driver.find_element(By.TAG_NAME, "iframe")
        while True:
            print("switching to", reportFrame.get_attribute("id"))
            if reportFrame.get_attribute("id") == "webiViewFrame":
                driver.switch_to.frame(reportFrame)
                break
            driver.switch_to.frame(reportFrame)

            try:
                reportFrame = driver.find_element(By.TAG_NAME, "iframe")
            except:
                break

        export = driver.find_element(By.ID, "iconmid_iconMenu_icon__dhtmlLib_239")
        export.click()

        menu = driver.find_element(
            By.ID, "iconMenu_menu__dhtmlLib_239_text__menuAutoId_3")
        menu.click()

        expo = driver.find_element(
            By.ID, "_dhtmlLib_244_span_text__menuAutoId_5")
        expo.click()

        print("clicked")
        sleep(15)
        # Assign the direct URL to downloaded_file_path
        downloaded_file_path = os.path.join(DOWNLOAD_DIRECTORY, "HBS_Table_No._215_ _Daily_Exchange_Rate_of_the_Indian_Rupee.xlsx")
        
        # Return the downloaded file path
        return downloaded_file_path
    
    driver.get("https://dbie.rbi.org.in/DBIE/dbie.rbi?site=statistics#!4_6")
    driver.implicitly_wait(20)
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)

    links = driver.find_elements(By.CSS_SELECTOR, "a")
    for link in links:
        print(link.get_attribute("innerText"))
    links[0].click()

    sleep(5)
    downloaded_file_path = File_exporter()
    # Code for the graph - Exchange rates
    exrate = pd.read_excel(downloaded_file_path, sheet_name=0)
    exrate.iloc[:, 1] = pd.to_datetime(exrate.iloc[:, 1], errors='coerce') 
    exrate = exrate.dropna(subset=[exrate.columns[1]])
    exrate = exrate.drop(columns=exrate.columns[0])

    exrate = exrate.rename(columns={
        exrate.columns[0]: "Date",
        exrate.columns[1]: "US Dollar",
        exrate.columns[2]: "Pound Sterling",
        exrate.columns[3]: "Euro",
        exrate.columns[4]: "Japanese Yen"
    })
    exrate = exrate.sort_values("Date")

    fig8 = px.line(exrate, x='Date', y=exrate.columns[1:], title='Exchange Rate Data')
    fig8.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True),
        showlegend=True,
        template='plotly_white'
    )
    graph_div8 = fig8.to_html(full_html=False)
    
    exrate[exrate.columns[1:]] = exrate[exrate.columns[1:]].apply(pd.to_numeric, errors='coerce')

    exrate['Daily_Growth_USD'] = exrate['US Dollar'].pct_change()
    exrate['Daily_Growth_Pound'] = exrate['Pound Sterling'].pct_change()
    exrate['Daily_Growth_Euro'] = exrate['Euro'].pct_change()
    exrate['Daily_Growth_Yen'] = exrate['Japanese Yen'].pct_change()

    daily_usd_growth = round(exrate['Daily_Growth_USD'].iloc[-1], 3)
    daily_pound_growth = round(exrate['Daily_Growth_Pound'].iloc[-1], 3)
    daily_euro_growth = round(exrate['Daily_Growth_Euro'].iloc[-1], 3)
    daily_yen_growth = round(exrate['Daily_Growth_Yen'].iloc[-1], 3)

    context = {
        'graph_div8': graph_div8,
        'daily_usd_growth': daily_usd_growth,
        'daily_pound_growth': daily_pound_growth,
        'daily_euro_growth': daily_euro_growth,
        'daily_yen_growth': daily_yen_growth,
    }
    return render(request, 'exchange-rate.html', context)


def foreignreserves(request):
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=chrome_options)
    
    def File_exporter():
        reportFrame = driver.find_element(By.TAG_NAME, "iframe")
        while True:
            print("switching to", reportFrame.get_attribute("id"))
            if reportFrame.get_attribute("id") == "webiViewFrame":
                driver.switch_to.frame(reportFrame)
                break
            driver.switch_to.frame(reportFrame)

            try:
                reportFrame = driver.find_element(By.TAG_NAME, "iframe")
            except:
                break

        export = driver.find_element(By.ID, "iconmid_iconMenu_icon__dhtmlLib_239")
        export.click()

        menu = driver.find_element(
            By.ID, "iconMenu_menu__dhtmlLib_239_text__menuAutoId_3")
        menu.click()

        expo = driver.find_element(
            By.ID, "_dhtmlLib_244_span_text__menuAutoId_5")
        expo.click()

        print("clicked")
        sleep(15)
        # Assign the direct URL to downloaded_file_path
        downloaded_file_path = os.path.join(DOWNLOAD_DIRECTORY, "RBIB_Table_No._32_ _Foreign_Exchange_Reserves.xlsx")

        # Return the downloaded file path
        return downloaded_file_path
    
    driver.get("https://dbie.rbi.org.in/DBIE/dbie.rbi?site=statistics#!5_31")
    driver.implicitly_wait(20)
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)

    links = driver.find_elements(By.CSS_SELECTOR, "a")
    for link in links:
        print(link.get_attribute("innerText"))
    links[0].click()

    sleep(5)
    downloaded_file_path = File_exporter()
    # Code for the graph : Foreign exchange reserves
    forex_ini = pd.read_excel(downloaded_file_path, sheet_name=0)
    empty_rows = forex_ini[(forex_ini.iloc[:, 3:14].isnull()).all(axis=1)]
    forex = forex_ini.drop(empty_rows.index)
    forex = forex.iloc[3:]
    forex = forex.iloc[:, 2:]
    columns_to_drop = [1, 3, 5, 7, 9, 10]
    forex = forex.drop(forex.columns[columns_to_drop], axis=1)

    column_names = ["Date","Foreign Currency Assets", "Gold", "Reserve Tranch Position", "SDRs", "Total"]
    forex.columns = column_names

    fig9 = px.line(forex, x='Date', y=forex.columns[1:],)
    fig9.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True),
        showlegend=True,
        template='plotly_white'
    )
    graph_div9 = fig9.to_html(full_html=False, include_plotlyjs='cdn')

    forex[column_names[1:]] = forex[column_names[1:]].apply(pd.to_numeric, errors='coerce')
    forex['Weekly_Growth_Rate'] = forex['Total'].pct_change() * 100
    forex['Monthly_Growth_Rate'] = forex['Total'].pct_change(4) * 100
    forex['6_Month_Growth_Rate'] = forex['Total'].pct_change(24) * 100
    forex['Yearly_Growth_Rate'] = forex['Total'].pct_change(52) * 100

    latest_general_weekly_growth = round(forex['Weekly_Growth_Rate'].iloc[-1], 1)
    latest_general_month_growth = round(forex['Monthly_Growth_Rate'].iloc[-1], 1)
    latest_general_6_month_growth = round(forex['6_Month_Growth_Rate'].iloc[-1], 1)
    latest_general_yearly_growth = round(forex['Yearly_Growth_Rate'].iloc[-1], 1)

    context = {
        'graph_div9': graph_div9,
        'latest_general_weekly_growth': latest_general_weekly_growth,
        'latest_general_month_growth': latest_general_month_growth,
        'latest_general_6_month_growth': latest_general_6_month_growth,
        'latest_general_yearly_growth': latest_general_yearly_growth,
        
    }
    return render(request, 'foreign-reserves.html', context)

def keyrates(request):
    #Code for the 10th graph - Key rates
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode

    driver = webdriver.Chrome(options=chrome_options)

    def File_exporter():
        reportFrame = driver.find_element(By.TAG_NAME, "iframe")
        while True:
            print("switching to", reportFrame.get_attribute("id"))
            if reportFrame.get_attribute("id") == "webiViewFrame":
                driver.switch_to.frame(reportFrame)
                break
            driver.switch_to.frame(reportFrame)

            try:
                reportFrame = driver.find_element(By.TAG_NAME, "iframe")
            except:
                break

        export = driver.find_element(By.ID, "iconmid_iconMenu_icon__dhtmlLib_239")
        export.click()

        menu = driver.find_element(
            By.ID, "iconMenu_menu__dhtmlLib_239_text__menuAutoId_3")
        menu.click()

        expo = driver.find_element(
            By.ID, "_dhtmlLib_244_span_text__menuAutoId_5")
        expo.click()

        print("clicked")
        sleep(15)

        downloaded_file_path = os.path.join(DOWNLOAD_DIRECTORY, "HBS_Table_No._44_ _Major_Monetary_Policy_Measures_-_Bank_Rate,_CRR_&_SLR.xlsx")
        return downloaded_file_path
        
    #KeyRates

    driver.get("https://dbie.rbi.org.in/DBIE/dbie.rbi?site=statistics#!3_41")
    driver.implicitly_wait(20)
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)

    links = driver.find_elements(By.CSS_SELECTOR, "a")
    for link in links:
        print(link.get_attribute("innerText"))
    links[0].click()

    sleep(5)
    downloaded_file_path = File_exporter()

    # Close the webdriver
    driver.quit()
    
    keyrate = pd.read_excel(downloaded_file_path, sheet_name=0)
    keyrate = keyrate.drop(range(6))
    keyrate = keyrate.iloc[:-1]
    keyrate = keyrate.drop(keyrate.columns[:2], axis=1)
    keyrate = keyrate.rename(columns={
        keyrate.columns[0]: "Date",
        keyrate.columns[1]: "Bank Rate",
        keyrate.columns[2]: "Repo Rate",
        keyrate.columns[3]: "Reverse Repo Rate",
        keyrate.columns[4]: "Standing Deposit Facility Rate",
        keyrate.columns[5]: "Marginal Standing Facility",
        keyrate.columns[6]: "Cash Reserve Ratio",
        keyrate.columns[7]: "Statutory Liquidity Ratio"
    })
    keyrate["Date"] = pd.to_datetime(keyrate["Date"])
    keyrate = keyrate.sort_values("Date")
    keyrate = keyrate.replace('-', np.nan)
    keyrate = keyrate.ffill()
    for col in keyrate.columns[1:]:
        keyrate[col] = pd.to_numeric(keyrate[col], errors='coerce')
    # Create the new graph
    fig10 = px.line(keyrate, x='Date', y=keyrate.columns, title='Key Rates Data')
    fig10.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True),
        showlegend=True,
        template='plotly_white'
    )
    graph_div10 = fig10.to_html(full_html=False)

    context = {
        'graph_div10': graph_div10,
    }
    return render(request, 'key-rates.html', context)

    

def gdp(request):
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=chrome_options)
    
    def File_exporter_const():
        reportFrame = driver.find_element(By.TAG_NAME, "iframe")
        while True:
            print("switching to", reportFrame.get_attribute("id"))
            if reportFrame.get_attribute("id") == "webiViewFrame":
                driver.switch_to.frame(reportFrame)
                break
            driver.switch_to.frame(reportFrame)

            try:
                reportFrame = driver.find_element(By.TAG_NAME, "iframe")
            except:
                break

        export = driver.find_element(By.ID, "iconmid_iconMenu_icon__dhtmlLib_239")
        export.click()

        menu = driver.find_element(
            By.ID, "iconMenu_menu__dhtmlLib_239_text__menuAutoId_3")
        menu.click()

        expo = driver.find_element(
            By.ID, "_dhtmlLib_244_span_text__menuAutoId_5")
        expo.click()

        print("clicked")
        sleep(15)
        # Assign the direct URL to downloaded_file_path
        downloaded_file_path = os.path.join(DOWNLOAD_DIRECTORY, "HBS_Table_No._156_ _Quarterly_Estimates_of_Gross_Domestic_Product_at_Market_Prices_(at_Constant_Prices)_(New_Series)_(Base _2004-05).xlsx")

        # Return the downloaded file path
        return downloaded_file_path
    
    # GDP - const

    driver.get("https://dbie.rbi.org.in/DBIE/dbie.rbi?site=statistics#!1_32")
    driver.implicitly_wait(20)
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)

    links = driver.find_elements(By.CSS_SELECTOR, "a")
    for link in links:
        print(link.get_attribute("innerText"))
    links[0].click()

    sleep(5)
    downloaded_file_path_const = File_exporter_const()
    #Code for 11th graph - GDP : constant
    GDP = pd.read_excel(downloaded_file_path_const, sheet_name=2)
    GDP = GDP.iloc[3:]
    GDP = GDP.iloc[:, 1:]
    GDP.columns = GDP.iloc[0]
    GDP['Industry/ Year'] = GDP['Industry/ Year'].fillna(method='ffill')
    GDP['Financial Year'] = GDP.apply(lambda row: f"{row['Industry/ Year']} {row['Quarter']}", axis=1)
    GDP = GDP.iloc[1:]
    GDP = GDP.iloc[:,2:]
    GDP = GDP.iloc[:-2]

    fig11 = px.line(GDP, x='Financial Year', y=list(GDP.columns), title='GDP at Constant Prices (Rupees Crore)')
    fig11.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True),
        showlegend=True,
        template='plotly_white'
    )
    
    GDP[GDP.columns[1:]] = GDP[GDP.columns[1:]].apply(pd.to_numeric, errors='coerce')

    GDP['Quarterly_Growth_Rate'] = GDP['GDP at market prices'].pct_change() * 100
    GDP['Yearly_Growth_Rate'] = GDP['GDP at market prices'].pct_change(4) * 100

    latest_general_q_month_growth_const = round(GDP['Quarterly_Growth_Rate'].iloc[-1], 1)
    latest_general_yearly_growth_const = round(GDP['Yearly_Growth_Rate'].iloc[-1], 1)
    
    
    
    #Code for 12th Graph - GDP : Current
    def File_exporter_curr():
        reportFrame = driver.find_element(By.TAG_NAME, "iframe")
        while True:
            print("switching to", reportFrame.get_attribute("id"))
            if reportFrame.get_attribute("id") == "webiViewFrame":
                driver.switch_to.frame(reportFrame)
                break
            driver.switch_to.frame(reportFrame)

            try:
                reportFrame = driver.find_element(By.TAG_NAME, "iframe")
            except:
                break

        export = driver.find_element(By.ID, "iconmid_iconMenu_icon__dhtmlLib_239")
        export.click()

        menu = driver.find_element(
            By.ID, "iconMenu_menu__dhtmlLib_239_text__menuAutoId_3")
        menu.click()

        expo = driver.find_element(
            By.ID, "_dhtmlLib_244_span_text__menuAutoId_5")
        expo.click()

        print("clicked")
        sleep(15)
        # Assign the direct URL to downloaded_file_path
        downloaded_file_path_curr = os.path.join(DOWNLOAD_DIRECTORY, "HBS_Table_No._154_ _Quarterly_Estimates_of_Gross_Domestic_Product_at_Market_Prices_(at_Current_Prices)_(New_Series)_(Base _2004-05).xlsx")

        # Return the downloaded file path
        return downloaded_file_path_curr
    
    driver.get("https://dbie.rbi.org.in/DBIE/dbie.rbi?site=statistics#!1_32")
    driver.implicitly_wait(20)
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)

    links = driver.find_elements(By.CSS_SELECTOR, "a")
    for link in links:
        print(link.get_attribute("innerText"))
    links[0].click()

    sleep(5)
    downloaded_file_path_curr = File_exporter_curr()
        
    GDP = pd.read_excel(downloaded_file_path_curr, sheet_name=2)
    GDP = GDP.iloc[3:]
    GDP = GDP.iloc[:, 1:]
    GDP.columns = GDP.iloc[0]
    GDP['Industry/ Year'] = GDP['Industry/ Year'].fillna(method='ffill')
    GDP['Financial Year'] = GDP.apply(lambda row: f"{row['Industry/ Year']} {row['Quarter']}", axis=1)
    GDP = GDP.iloc[1:]
    GDP = GDP.iloc[:,2:]
    GDP = GDP.iloc[:-2]

    fig12 = px.line(GDP, x='Financial Year', y=list(GDP.columns), title='GDP at Current Prices (Rupees Crore)')
    fig12.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True),
        showlegend=True,
        template='plotly_white'
    )
    
    GDP[GDP.columns[1:]] = GDP[GDP.columns[1:]].apply(pd.to_numeric, errors='coerce')

    GDP['Quarterly_Growth_Rate'] = GDP['GDP at market prices'].pct_change() * 100
    GDP['Yearly_Growth_Rate'] = GDP['GDP at market prices'].pct_change(4) * 100

    latest_general_q_month_growth_current = round(GDP['Quarterly_Growth_Rate'].iloc[-1], 1)
    latest_general_yearly_growth_current = round(GDP['Yearly_Growth_Rate'].iloc[-1], 1)
    
    graph_div11 = fig11.to_html(full_html=False)
    graph_div12 = fig12.to_html(full_html=False)
    
    context = {
        'graph_div11': graph_div11,
        'graph_div12': graph_div12,
        'latest_general_q_month_growth_const': latest_general_q_month_growth_const,
        'latest_general_yearly_growth_const': latest_general_yearly_growth_const,
        'latest_general_q_month_growth_current': latest_general_q_month_growth_current,
        'latest_general_yearly_growth_current': latest_general_yearly_growth_current,
    }
    return render(request, 'gdp.html', context)


def scbfoodbank(request):
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=chrome_options)
    
    def File_exporter():
        reportFrame = driver.find_element(By.TAG_NAME, "iframe")
        while True:
            print("switching to", reportFrame.get_attribute("id"))
            if reportFrame.get_attribute("id") == "webiViewFrame":
                driver.switch_to.frame(reportFrame)
                break
            driver.switch_to.frame(reportFrame)

            try:
                reportFrame = driver.find_element(By.TAG_NAME, "iframe")
            except:
                break

        export = driver.find_element(By.ID, "iconmid_iconMenu_icon__dhtmlLib_239")
        export.click()

        menu = driver.find_element(
            By.ID, "iconMenu_menu__dhtmlLib_239_text__menuAutoId_3")
        menu.click()

        expo = driver.find_element(
            By.ID, "_dhtmlLib_244_span_text__menuAutoId_5")
        expo.click()

        print("clicked")
        sleep(15)
        
        # Assign the direct URL to downloaded_file_path
        downloaded_file_path = os.path.join(DOWNLOAD_DIRECTORY, "Bank_Credit_and_Food_Credit_-_Scheduled_Commercial_Banks.xlsx")

        # Return the downloaded file path
        return downloaded_file_path
    
    driver.get("https://dbie.rbi.org.in/DBIE/dbie.rbi?site=statistics#!3_10")
    driver.implicitly_wait(20)
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)

    links = driver.find_elements(By.CSS_SELECTOR, "a")
    for link in links:
        print(link.get_attribute("innerText"))
    links[0].click()

    sleep(5)
    downloaded_file_path = File_exporter()


    #Code for 13th graph - SCB Food Bank Credit
    scb = pd.read_excel(downloaded_file_path, sheet_name=0)
    scb = scb.iloc[6:, 4:]
    scb.iloc[:, 1:4] = scb.iloc[:, 1:4].apply(pd.to_numeric, errors='coerce')
    scb = scb.dropna(subset=scb.columns[1:4], how='all')
    scb.iloc[:, 0] = pd.to_datetime(scb.iloc[:, 0])
    scb = scb.rename(columns={scb.columns[0]: "Date", scb.columns[1]: "Bank Credit", scb.columns[2]: "Food Credit",
                               scb.columns[3]: "Non Food Credit"})

    fig13 = px.line(scb, x='Date', y=scb.columns, title='SCB Food and Non Food Credit Data')
    fig13.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True),
        showlegend=True,
        template='plotly_white'
    )
    graph_div13 = fig13.to_html(full_html=False)
    return render(request, 'scb-food-bank.html', {'graph_div13': graph_div13,})


def balanceofpayments(request):
    # Code for the 14th graph - 
    # Code snippet to generate Balance of Payments graph
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=chrome_options)

    def File_exporter():
        reportFrame = driver.find_element(By.TAG_NAME, "iframe")
        while True:
            print("switching to", reportFrame.get_attribute("id"))
            if reportFrame.get_attribute("id") == "webiViewFrame":
                driver.switch_to.frame(reportFrame)
                break
            driver.switch_to.frame(reportFrame)

            try:
                reportFrame = driver.find_element(By.TAG_NAME, "iframe")
            except:
                break

        export = driver.find_element(By.ID, "iconmid_iconMenu_icon__dhtmlLib_239")
        export.click()

        menu = driver.find_element(
            By.ID, "iconMenu_menu__dhtmlLib_239_text__menuAutoId_3")
        menu.click()

        expo = driver.find_element(
            By.ID, "_dhtmlLib_244_span_text__menuAutoId_5")
        expo.click()

        print("clicked")
        sleep(15)

        downloaded_file_path = os.path.join(DOWNLOAD_DIRECTORY, "HBS_Table_No._194_ _Indias_Overall_Balance_of_Payments_-_Quarterly_-_Rupees.xlsx")
        return downloaded_file_path

    # BOP
    driver.get("https://dbie.rbi.org.in/DBIE/dbie.rbi?site=statistics#!5_4")
    driver.implicitly_wait(20)
    timetab = driver.find_element(By.CSS_SELECTOR, "#pettabs > ul > li:nth-child(2)")
    timetab.click()
    sleep(5)
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)

    links = driver.find_elements(By.CSS_SELECTOR, "a")
    for link in links:
        print(link.get_attribute("innerText"))
    links[0].click()

    sleep(5)
    downloaded_file_path = File_exporter()
    
    # Update BoP_ini with the extracted file
    BoP_ini = pd.read_excel(downloaded_file_path, sheet_name=1)
    BoP_ini = BoP_ini.iloc[4:]
    BoP_ini = BoP_ini.iloc[:, 1:]
    BoP_ini.columns = BoP_ini.iloc[0]
    req_columns = ["Year", "Quarter", "Transaction Type", "A.1) Merchandise", "A.2) Invisibles", "A) Current Account", "B.1) Foreign Investment",
            "B.2) Loans", "B.3) Banking Capital", "B.4) Rupee Debt Service", "B.5) Other Capital", "B) Capital Account", "C) Errors and Omissions",
            "D) Overall Balance", "E) Monetary Movements", "E.2) Foreign Exchange Reserves (Increase - / Decrease +)"]
    BoP_ini = BoP_ini[req_columns]

    BoP = BoP_ini[BoP_ini.iloc[:, 2] == 'Net'].copy()
    BoP['Financial Year'] = BoP.apply(lambda row: f"{row['Year']} {row['Quarter']}", axis=1)
    BoP = BoP.iloc[:,3:]
    column_names = { "A.1) Merchandise": "Merchandise", "A.2) Invisibles": "Invisibles", "A) Current Account": "Current Account",
            "B.1) Foreign Investment": "Foreign Investment", "B.2) Loans": "Loans", "B.3) Banking Capital": "Banking Capital",
            "B.4) Rupee Debt Service": "Rupee Debt Service", "B.5) Other Capital": "Other Capital", "B) Capital Account": "Capital Account",
            "C) Errors and Omissions": "Errors and Omissions", "D) Overall Balance": "Overall Balance", "E) Monetary Movements": "Monetary Movements",
            "E.2) Foreign Exchange Reserves (Increase - / Decrease +)": "Foreign Exchange Reserves (Increase - / Decrease +)"}
    BoP.rename(columns=column_names, inplace=True)
    fig14 = px.line(BoP, x='Financial Year', y=list(BoP.columns), title='Balance of Payments (Rupees Crore)')
    fig14.update_layout(
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True),
            showlegend=True,
            template='plotly_white'
    ) 
    graph_div14 = fig14.to_html(full_html=False)
    context = {
        'graph_div14': graph_div14,
    }
   
    # Close the webdriver
    driver.quit()

    return render(request, 'balance-of-payments.html', context)




import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def iip(request):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=chrome_options)

    def File_exporter():
        reportFrame = driver.find_element(By.TAG_NAME, "iframe")
        while True:
            print("switching to", reportFrame.get_attribute("id"))
            if reportFrame.get_attribute("id") == "webiViewFrame":
                driver.switch_to.frame(reportFrame)
                break
            driver.switch_to.frame(reportFrame)

            try:
                reportFrame = driver.find_element(By.TAG_NAME, "iframe")
            except:
                break

        export = driver.find_element(By.ID, "iconmid_iconMenu_icon__dhtmlLib_239")
        export.click()

        menu = driver.find_element(
            By.ID, "iconMenu_menu__dhtmlLib_239_text__menuAutoId_3")
        menu.click()

        expo = driver.find_element(
            By.ID, "_dhtmlLib_244_span_text__menuAutoId_5")
        expo.click()

        print("clicked")
        sleep(15)

        downloaded_file_path = os.path.join(DOWNLOAD_DIRECTORY, "Index_of_Industrial_Production_(Detailed).xlsx")
        return downloaded_file_path

    driver.get("https://dbie.rbi.org.in/DBIE/dbie.rbi?site=statistics#!1_30")
    driver.implicitly_wait(20)
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)

    links = driver.find_elements(By.CSS_SELECTOR, "a")
    for link in links:
        print(link.get_attribute("innerText"))
    links[0].click()

    sleep(5)
    downloaded_file_path = File_exporter()
    IIP_ini = pd.read_excel(downloaded_file_path, sheet_name=1)
    IIP_ini = IIP_ini.iloc[:, 3:]
    IIP_ini = IIP_ini.iloc[5:]
    IIP_ini = IIP_ini.iloc[:4]
    IIP_ini = IIP_ini.loc[:, ~IIP_ini.iloc[0].isna()]

    first_row = IIP_ini.iloc[0]
    numbers_vector = first_row.str.extract('(\d{4}):(\d{2})')[0] + first_row.str.extract('(\d{4}):(\d{2})')[1]
    date_series = pd.to_datetime(numbers_vector, format='%Y%m', errors='coerce')
    formatted_dates = date_series.dt.strftime('%b-%Y')
    valid_dates = formatted_dates.dropna()

    IIP = pd.DataFrame({'Date': valid_dates.values})
    IIP['Manufacturing'] = IIP_ini.iloc[1].values
    IIP['Electricity'] = IIP_ini.iloc[2].values
    IIP['General Index'] = IIP_ini.iloc[3].values

    IIP['Date'] = pd.to_datetime(IIP['Date'], format='%b-%Y')
    IIP = IIP.sort_values('Date')
    IIP['Date'] = IIP['Date'].dt.strftime('%b-%Y')

    fig15 = px.line(IIP, x='Date', y=IIP.columns)
    fig15.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True),
        showlegend=True,
        template='plotly_white'
    )
    graph_div15 = fig15.to_html(full_html=True, include_plotlyjs=True)
    
    # Calculate growth rates
    IIP['Monthly_Growth_Rate'] = round((IIP['General Index'].pct_change() * 100), 1)
    IIP['6_Month_Growth_Rate'] = round((IIP['General Index'].pct_change(6) * 100), 1)
    IIP['Yearly_Growth_Rate'] = round(IIP['General Index'].pct_change(12) * 100, 1)
    IIP['Manufacturing_Monthly_Growth'] = round(IIP['Manufacturing'].pct_change() * 100, 1)
    IIP['Manufacturing_6_Month_Growth'] = round(IIP['Manufacturing'].pct_change(6) * 100, )
    IIP['Manufacturing_Yearly_Growth'] = round(IIP['Manufacturing'].pct_change(12) * 100,1)
    IIP['Electricity_Monthly_Growth'] = round(IIP['Electricity'].pct_change() * 100, 1)
    IIP['Electricity_6_Month_Growth'] = round(IIP['Electricity'].pct_change(6) * 100, 1)
    IIP['Electricity_Yearly_Growth'] = round(IIP['Electricity'].pct_change(12) * 100, 1)

    # Get latest growth rates
    latest_general_month_growth = round(IIP['Monthly_Growth_Rate'].iloc[-1], 1)
    latest_manufacturing_month_growth = IIP['Manufacturing_Monthly_Growth'].iloc[-1]
    latest_electricity_month_growth = IIP['Electricity_Monthly_Growth'].iloc[-1]
    latest_general_6_month_growth = IIP['6_Month_Growth_Rate'].iloc[-1]
    latest_manufacturing_6_month_growth = IIP['Manufacturing_6_Month_Growth'].iloc[-1]
    latest_electricity_6_month_growth = IIP['Electricity_6_Month_Growth'].iloc[-1]
    latest_general_yearly_growth = IIP['Yearly_Growth_Rate'].iloc[-1]
    latest_manufacturing_yearly_growth = IIP['Manufacturing_Yearly_Growth'].iloc[-1]
    latest_electricity_yearly_growth = IIP['Electricity_Yearly_Growth'].iloc[-1]

    # Heatmap
    def heatmap_df(iip_column_name):
        cal_val = pd.DataFrame({'Date': valid_dates.values})
        cal_val['Month'] = pd.to_datetime(cal_val['Date'], format='%b-%Y').dt.month
        cal_val['Year'] = pd.to_datetime(cal_val['Date'], format='%b-%Y').dt.year
        cal_val['Date'] = pd.to_datetime(cal_val['Date'], format='%b-%Y')
        cal_val = cal_val.sort_values('Date')
        cal_val[iip_column_name] = IIP[iip_column_name].values

        cal_val_pivot = cal_val.pivot(index='Month', columns='Year', values=iip_column_name)

        return cal_val_pivot

    cal_Gen_Indx_pivot = heatmap_df('General Index')
    cal_Elec_pivot = heatmap_df('Electricity')
    cal_Manu_pivot = heatmap_df('Manufacturing')

    def generate_heatmap(dataframe, title):
        fig = px.imshow(dataframe, x=dataframe.columns, y=dataframe.index,
                        color_continuous_scale='RdBu', color_continuous_midpoint=130)

        fig.update_layout(
            title=title,
            xaxis=dict(showgrid=False),
            yaxis=dict(
                showgrid=False,
                tickmode='array',
                ticktext=dataframe.index.map(lambda x: pd.to_datetime(str(x), format='%m').strftime('%B')),
                tickvals=dataframe.index,
            ),
            margin=dict(l=50, r=50, t=50, b=50, pad=5),
            showlegend=False,
            template='plotly_white',
            
        )
        if title == 'Heatmap - General Index' or title == 'Heatmap - Electricity':
            fig.update_layout(coloraxis_showscale=False)
        fig.update_coloraxes(showscale=False)

        return fig


    # genindx_heatmap = generate_heatmap(cal_Gen_Indx_pivot, 'Heatmap - General Index')
    # elec_heatmap = generate_heatmap(cal_Elec_pivot, 'Heatmap - Electricity')
    # manu_heatmap = generate_heatmap(cal_Manu_pivot, 'Heatmap - Manufacturing')
    cal_Gen_Indx_pivot = heatmap_df('General Index')
    cal_Elec_pivot = heatmap_df('Electricity')
    cal_Manu_pivot = heatmap_df('Manufacturing')

    genindx_heatmap = generate_heatmap(cal_Gen_Indx_pivot, 'Heatmap - General Index')
    elec_heatmap = generate_heatmap(cal_Elec_pivot, 'Heatmap - Electricity')
    manu_heatmap = generate_heatmap(cal_Manu_pivot, 'Heatmap - Manufacturing')
    
    genindx_heatmap = genindx_heatmap.to_html(full_html=False)
    elec_heatmap = elec_heatmap.to_html(full_html=False)
    manu_heatmap = manu_heatmap.to_html(full_html=False)


    # Pass data to the template
    context = {
        'graph_div15': graph_div15,
        'latest_general_month_growth': latest_general_month_growth,
        'latest_manufacturing_month_growth': latest_manufacturing_month_growth,
        'latest_electricity_month_growth': latest_electricity_month_growth,
        'latest_general_6_month_growth': latest_general_6_month_growth,
        'latest_manufacturing_6_month_growth': latest_manufacturing_6_month_growth,
        'latest_electricity_6_month_growth': latest_electricity_6_month_growth,
        'latest_general_yearly_growth': latest_general_yearly_growth,
        'latest_manufacturing_yearly_growth': latest_manufacturing_yearly_growth,
        'latest_electricity_yearly_growth': latest_electricity_yearly_growth,
        'genindx_heatmap': genindx_heatmap,
        'elec_heatmap': elec_heatmap,
        'manu_heatmap': manu_heatmap,
    }

    return render(request, 'iip.html', context)



def fdi(request):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=chrome_options)

    def File_exporter():
        reportFrame = driver.find_element(By.TAG_NAME, "iframe")
        while True:
            print("switching to", reportFrame.get_attribute("id"))
            if reportFrame.get_attribute("id") == "webiViewFrame":
                driver.switch_to.frame(reportFrame)
                break
            driver.switch_to.frame(reportFrame)

            try:
                reportFrame = driver.find_element(By.TAG_NAME, "iframe")
            except:
                break

        export = driver.find_element(By.ID, "iconmid_iconMenu_icon__dhtmlLib_239")
        export.click()

        menu = driver.find_element(
            By.ID, "iconMenu_menu__dhtmlLib_239_text__menuAutoId_3")
        menu.click()

        expo = driver.find_element(
            By.ID, "_dhtmlLib_244_span_text__menuAutoId_5")
        expo.click()

        print("clicked")
        sleep(15)

        # Assign the direct URL to downloaded_file_path
        downloaded_file_path = os.path.join(DOWNLOAD_DIRECTORY, "RBIB_Table_No._34_ _Foreign_Investment_Inflows.xlsx")

        # Return the downloaded file path
        return downloaded_file_path
    
    driver.get("https://dbie.rbi.org.in/DBIE/dbie.rbi?site=statistics#!5_3")
    driver.implicitly_wait(20)
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)

    links = driver.find_elements(By.CSS_SELECTOR, "a")
    for link in links:
        print(link.get_attribute("innerText"))
    links[0].click()

    sleep(5)
    downloaded_file_path = File_exporter()
    FDI_ini = pd.read_excel(downloaded_file_path, sheet_name=1)
    #new code
    FDI_ini = FDI_ini.drop([0, 1, 2 , 4])
    FDI_ini = FDI_ini.drop(columns=[FDI_ini.columns[0]])
    FDI_ini.columns = FDI_ini.iloc[0]
    FDI_ini = FDI_ini.reset_index(drop=True)
    FDI_ini = FDI_ini.drop(0)
    FDI_ini = FDI_ini.reset_index(drop=True)

    req_columns = ["Month", "1.1 Net Foreign Direct Investment (1.1.1-1.1.2)", "1.1.1 Direct Investment to India (1.1.1.1-1.1.1.2)",
                "1.1.2 Foreign Direct Investment by India (1.1.2.1+1.1.2.2+1.1.2.3-1.1.2.4)", 
                    "1.2 Net Portfolio Investment (1.2.1+1.2.2+1.2.3-1.2.4)", "1.2.1 GDRs/ADRs ", "1.2.2 FIIs ",
                    "1.2.4 Portfolio investment by India", "1 Foreign Investment Inflows"]
    FDI_ini = FDI_ini[req_columns]

    column_names = { "Month": "Date", "1.1 Net Foreign Direct Investment (1.1.1-1.1.2)": "Net Foreign Direct Investment",
        "1.1.1 Direct Investment to India (1.1.1.1-1.1.1.2)": "Direct Investment to India",
        "1.1.2 Foreign Direct Investment by India (1.1.2.1+1.1.2.2+1.1.2.3-1.1.2.4)": "Foreign Direct Investment by India", 
        "1.2 Net Portfolio Investment (1.2.1+1.2.2+1.2.3-1.2.4)": "Net Portfolio Investment","1.2.1 GDRs/ADRs ": "Global/American Depository Receipts",
        "1.2.2 FIIs ": "Foreign Institutional Investors","1.2.4 Portfolio investment by India": "Portfolio Investment by India", 
        "1 Foreign Investment Inflows": "Foreign Investment Inflows"}
    FDI_ini.rename(columns=column_names, inplace=True)

    numbers_vector = FDI_ini.iloc[:, 0].str.extract('(\d{4}):(\d{2})')[0] + FDI_ini.iloc[:, 0].str.extract('(\d{4}):(\d{2})')[1]
    date_series = pd.to_datetime(numbers_vector, format='%Y%m', errors='coerce')
    formatted_dates = date_series.dt.strftime('%b-%Y')
    valid_dates = formatted_dates.dropna()

    FDI_FPI_ini = pd.DataFrame({'Date': valid_dates.values})
    columns_to_copy = FDI_ini.columns[1:]
    for column in columns_to_copy:
        FDI_FPI_ini[column] = FDI_ini[column]

    FDI_FPI = FDI_FPI_ini[['Date', 'Net Foreign Direct Investment', 'Net Portfolio Investment', 'Foreign Investment Inflows']].copy()
    FDI = FDI_FPI_ini[['Date', 'Net Foreign Direct Investment', 'Direct Investment to India',
                'Foreign Direct Investment by India']].copy()
    FPI = FDI_FPI_ini[['Date', 'Net Portfolio Investment', 'Global/American Depository Receipts', 'Foreign Institutional Investors',
                'Portfolio Investment by India']].copy()


    colors = ['red', 'green', 'blue', 'orange']
    fig16 = px.line(FDI_FPI, x='Date', y=['Net Foreign Direct Investment', 'Net Portfolio Investment', 'Foreign Investment Inflows'],
                    title='Foreign Investment Inflows', color_discrete_sequence=colors)
    fig16.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True),
        showlegend=True,
        template='plotly_white'
    )
    graph_div16 = fig16.to_html(full_html=False)

    colors = ['red', 'green', 'blue', 'orange']
    fig161 = px.line(FDI, x='Date', y=['Net Foreign Direct Investment', 'Direct Investment to India',
                                        'Foreign Direct Investment by India'], title='Direct Investments',
                      color_discrete_sequence=colors)
    fig161.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True),
        showlegend=True,
        template='plotly_white'
    )
    graph_div161 = fig161.to_html(full_html=False)

    colors = ['red', 'green', 'blue', 'orange']
    fig162 = px.line(FPI, x='Date', y=['Net Portfolio Investment', 'Global/American Depository Receipts',
                                        'Foreign Institutional Investors', 'Portfolio Investment by India'],
                      title='Portfolio', color_discrete_sequence=colors)
    fig162.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True),
        showlegend=True,
        template='plotly_white'
    )
    graph_div162 = fig162.to_html(full_html=False)

    def heatmap_df(fdi_column_name):
        cal_val = pd.DataFrame({'Date': valid_dates.values})
        cal_val['Month'] = pd.to_datetime(cal_val['Date'], format='%b-%Y').dt.month
        cal_val['Year'] = pd.to_datetime(cal_val['Date'], format='%b-%Y').dt.year
        cal_val['Date'] = pd.to_datetime(cal_val['Date'], format='%b-%Y')
        cal_val = cal_val.sort_values('Date')
        cal_val[fdi_column_name] = FDI_FPI_ini[fdi_column_name].values

        cal_val_pivot = cal_val.pivot(index='Month', columns='Year', values=fdi_column_name)

        return cal_val_pivot

    cal_FDI = heatmap_df('Net Foreign Direct Investment')
    cal_NPI = heatmap_df('Net Portfolio Investment')
    cal_net = heatmap_df('Foreign Investment Inflows')
    
    def generate_heatmap(dataframe, title):
        fig = px.imshow(dataframe, x=dataframe.columns, y=dataframe.index,
                        color_continuous_scale='RdBu', color_continuous_midpoint=0)
        
        fig.update_yaxes(ticktext=dataframe.index.map(lambda x: pd.to_datetime(str(x), format='%m').strftime('%B')),
                        tickvals=dataframe.index)
        
        fig.update_layout(
            title=title,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False, tickmode='array', ticktext=dataframe.index.map(lambda x: pd.to_datetime(str(x), format='%m').strftime('%B')),
                tickvals=dataframe.index,),
            margin=dict(l=50, r=50, t=50, b=50, pad=5),
            showlegend=False,
            template='plotly_white',
        ),
        
        return fig
    

    FDI_heatmap = generate_heatmap(cal_FDI, 'Heatmap - Foreign Direct Investment')
    FDI_heatmap.update(layout_coloraxis_showscale=False)
    NPI_heatmap = generate_heatmap(cal_NPI, 'Heatmap - Net Portfolio Investment')
    NPI_heatmap.update(layout_coloraxis_showscale=False)
    net_heatmap = generate_heatmap(cal_net, 'Heatmap - Foreign Investment Inflows')
    net_heatmap.update(layout_coloraxis_showscale=False)

    # Rest of the code...

    context = {
        'graph_div16': graph_div16,
        'graph_div161': graph_div161,
        'graph_div162': graph_div162,
        'FDI_heatmap': FDI_heatmap.to_html(full_html=False),
        'NPI_heatmap': NPI_heatmap.to_html(full_html=False),
        'net_heatmap': net_heatmap.to_html(full_html=False),
    }


    return render(request, 'fdi.html', context)

def process_data(df):
        df = df.iloc[2:]
        selected_rows = ['Country Code', 'USA', 'CHN', 'JPN', 'DEU', 'GBR', 'BRA', 'KOR', 'IND']
        df = df[df.iloc[:, 1].isin(selected_rows)]
        df.columns = df.iloc[0]
        df = df.iloc[1:]
        df.set_index('Country Name', inplace=True)
        df = df.iloc[:, 3:]
        df2 = df.transpose()
        df2.reset_index(inplace=True)
        df2 = df2.rename(columns={df2.columns[0]: 'Year'})
        df2 = df2.dropna(how = 'all', subset = df2.columns[1:])

        return df2

def line_plot(df, title):
        traces = []
        for column in df.columns:
            trace = go.Scatter(
                x=df['Year'],
                y=df[column],
                name=column
            )
            if column == 'India':
                trace.line.width = 2.5
                trace.mode = 'lines+markers'
                trace.marker.size = 5
                trace.line.color = "black"
            traces.append(trace)

        layout = go.Layout(
            title=title,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True),
            showlegend=True,
            template='plotly_white'
        )

        fig = go.Figure(data=traces, layout=layout)
        plot_div = opy.plot(fig, auto_open=False, output_type='div')

        return plot_div
    
def line_plot2(df, titl):
        fig = px.line(df, x='Year', y=df.columns, title=titl)
        fig.update_layout(
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True),
            showlegend=True,
            template='plotly_white'
        )
        for data in fig.data:
            if "India" in data.name:
                data.line.width = 2.5
                data.mode = 'lines+markers'
                data.marker.size = 5
                data.line.color = "black"
        graph_div18 = fig.to_html(full_html=False)
        return graph_div18

def gcpi(request):
    
    url = "https://api.worldbank.org/v2/en/indicator/FP.CPI.TOTL.ZG?downloadformat=excel"
    filename = "graphgen_app/files/API_FP.CPI.TOTL.ZG_DS2_en_excel_v2_5454868.xls"  

    response = requests.get(url)

    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print("File downloaded successfully.")
    else:
        print("Failed to download the file. Error:", response.status_code)

    GCPI_ini = pd.read_excel(filename, sheet_name=0)
    GCPI = process_data(GCPI_ini)
    
    def line_plot1(df, titl):
        fig = px.line(df, x='Year', y=df.columns, title=titl)
        fig.update_layout(
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True),
            showlegend=True,
            template='plotly_white'
        )
        fig.update_yaxes(range=[0, 30])
        for data in fig.data:
            if "India" in data.name:
                data.line.width = 2.5
                data.mode = 'lines+markers'
                data.marker.size = 5
                data.line.color = "black"
        graph_div17 = fig.to_html(full_html=False)
        return graph_div17
    graph_div17 = line_plot1(GCPI, 'Global Inflation - Consumer Prices')
    return render(request, 'gcpi.html', {'graph_div17': graph_div17})

def gfdi(request):  
    url = "https://api.worldbank.org/v2/en/indicator/BX.KLT.DINV.CD.WD?downloadformat=excel"
    filename = "API_BX.KLT.DINV.CD.WD_DS2_en_excel_v2_5454953.xls"  # Specify the filename to save the downloaded file

    response = requests.get(url)

    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print("File downloaded successfully.")
    else:
        print("Failed to download the file. Error:", response.status_code)  
        
    GFDI_ini = pd.read_excel(filename, sheet_name=0)
    GFDI = process_data(GFDI_ini)
    graph_div18 = line_plot2(GFDI, 'Global Foreign Direct Investment Inflows')
    return render(request, 'gfdi.html', {'graph_div18': graph_div18})

def process_chorodata(df):
    df = df.iloc[2:]
    df.columns = df.iloc[0]
    df = df.iloc[1:]
    
    df2 = pd.DataFrame(columns=['Country'] + ['Country Code'] + list(range(1960, 1960 + (len(df.columns)-4))))
    df2['Country'] = df.iloc[:, 0]
    df = df.iloc[:, 1:]
    df2['Country Code'] = df.iloc[:, 0]
    df = df.iloc[:, 3:]
    
    num_columns = len(df.columns)
    df2.iloc[:, 2:] = df.iloc[:, :num_columns]
    df2.dropna(axis=1, how='all', inplace=True)
    df2.columns = df2.columns.astype(str)
    df2 = df2.reset_index(drop=True)
    
    return df2

import plotly.graph_objects as go

def choropleth_plotter_ggdp(data, year, titl):
    data_temp = data[['Country', 'Country Code', year]].dropna()
    data_temp['logval'] = data_temp[year].apply(lambda x: np.log10(x) if pd.notnull(x) else np.nan)

    fig = go.Figure(data=go.Choropleth(
        locations=data_temp['Country Code'],
        z=data_temp['logval'],
        text=data_temp['Country'],
        hovertemplate='%{text}<br>GDP: $%{customdata: .2e}',
        customdata=data_temp[year],
        colorscale='RdBu',
        marker_line_color='white',
        zmin=8.5,
        zmax=13.5
    ))

    fig.update_layout(
        title=titl,
        geo=dict(
            showcountries=True,
            countrycolor='white'
        ),
        coloraxis=dict(
            colorbar=dict(
                title='Log Scale'
            )
        ),
        
        width=1000,  # Set the width of the figure to 800 pixels
        height=600 
    )
    
    return fig.to_html(full_html=False, include_plotlyjs=False)




def choropleth_plotter_ggdp_pcap(data, year, titl):
    data_temp = data[['Country', 'Country Code', year]].dropna()

    fig = go.Figure(data=go.Choropleth(
        locations=data_temp['Country Code'],
        z=data_temp[year],
        text=data_temp['Country'],
        hovertemplate='%{text}<br>GDP Per Capita: $%{z:.2f}',
        colorscale='RdBu',
        marker_line_color='white',
        zmin=0,
        zmax=60000
    ))

    fig.update_layout(
        title=titl,
        geo=dict(
            showcountries=True,
            countrycolor='white'
        ),
        width=1000,  # Set the width of the figure to 800 pixels
        height=600,
        coloraxis=dict(
        colorbar=None)  # Remove the colorbar
    )

    return fig.to_html(full_html=False, include_plotlyjs=False)

def ggdp(request):
    
    #for ggdp
    url = "https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.CD?downloadformat=excel"
    filename = "API_NY.GDP.MKTP.CD_DS2_en_excel_v2_5454813.xls"  

    response = requests.get(url)

    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print("File downloaded successfully.")
    else:
        print("Failed to download the file. Error:", response.status_code)
        
    url = "https://api.worldbank.org/v2/en/indicator/NY.GDP.PCAP.CD?downloadformat=excel"
    filename_pcap = "graphgen_app/files/API_NY.GDP.PCAP.CD_DS2_en_excel_v2_5454823.xls"  

    response = requests.get(url)

    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print("File downloaded successfully.")
    else:
        print("Failed to download the file. Error:", response.status_code)
    
    
    
    GGDP_ini = pd.read_excel(filename, sheet_name=0)
    GGDP_pcap_ini = pd.read_excel(filename_pcap, sheet_name=0)
    GGDP = process_data(GGDP_ini)
    GGDP_pcap = process_data(GGDP_pcap_ini)
    graph_div19 = line_plot2(GGDP, 'Global GDP')
    graph_div191 = line_plot2(GGDP_pcap, 'Gross Domestic Product Per Capita - Current USD')
    graph_div_choro = None  # Initialize the variable with None

    if request.method == 'POST':
        year = request.POST.get('year')
        indicator = request.POST.get('indicator')
        if year and year.isdigit() and int(year) >= 1960 and int(year) <= 2021:
            if indicator == 'ggdp':
                data_ini = pd.read_excel("graphgen_app/files/API_NY.GDP.MKTP.CD_DS2_en_excel_v2_5454813.xls", sheet_name=0)
                data = process_chorodata(data_ini)
                graph_div_choro = choropleth_plotter_ggdp(data, year, f'GDP: {year} (log scale)')
            elif indicator == 'ggdp_pcap':
                data_ini = pd.read_excel("graphgen_app/files/API_NY.GDP.PCAP.CD_DS2_en_excel_v2_5454823.xls", sheet_name=0)
                data = process_chorodata(data_ini)
                graph_div_choro = choropleth_plotter_ggdp_pcap(data, year, f'GDP per capita: {year} (log scale)')

            available_years = GGDP.columns[1:].tolist()

            context = {
                'graph_div19': graph_div19,
                'graph_div191': graph_div191,
                'available_years': available_years,
                'selected_year': year,
                'selected_indicator': indicator,
                'generated_choropleth': graph_div_choro,
            }

            return render(request, 'ggdp.html', context)

    available_years = GGDP.columns[1:].tolist()

    context = {
        'graph_div19': graph_div19,
        'graph_div191': graph_div191,
        'available_years': available_years,
    }

    return render(request, 'ggdp.html', context)






def choropleth_plotter_ggni(data, year, titl):
    data_temp = data[['Country', 'Country Code', year]].dropna()
    data_temp['logval'] = data_temp[year].apply(lambda x: np.log10(x) if pd.notnull(x) else np.nan)

    fig = px.choropleth(
        data_frame=data_temp,
        locations='Country Code',
        color='logval',
        hover_name='Country',
        hover_data={year: ':.2e'},
        color_continuous_scale='RdBu',
        range_color=(8.5, 13.5),
        labels={'logval': 'Log Scale'},
        title=titl
    )

    fig.update_geos(showcountries=True, countrycolor='white')
    fig.update_coloraxes(colorbar=None),
    fig.update_layout(width=1000, height=600)

    return fig.to_html(full_html=False, include_plotlyjs=False)





def choropleth_plotter_ggni_pcap(data, year, titl):
    data_temp = data[['Country', 'Country Code', year]].dropna()
    
    fig = px.choropleth(
        data_frame=data_temp,
        locations='Country Code',
        color=year,
        hover_name='Country',
        hover_data={year: ':.2f'},
        color_continuous_scale='RdBu',
        labels={'Nominal Scale': 'GNI Per Capita'},
        title=titl
    )
    
    fig.update_geos(showcountries=True, countrycolor='white')
    fig.update_layout(width=1000, height=600)

    return fig.to_html(full_html=False, include_plotlyjs=False)

def ggni(request):  
    
    #ggni 
    url = "https://api.worldbank.org/v2/en/indicator/NY.GNP.ATLS.CD?downloadformat=excel"
    filename = "graphgen_app/files/API_NY.GNP.ATLS.CD_DS2_en_excel_v2_5455179.xls"  # Specify the filename to save the downloaded file

    response = requests.get(url)

    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print("File downloaded successfully.")
    else:
        print("Failed to download the file. Error:", response.status_code)
        
    #ggni - pcap
    url = "https://api.worldbank.org/v2/en/indicator/NY.GNP.PCAP.CD?downloadformat=excel"
    filename_pcap = "graphgen_app/files/API_NY.GNP.PCAP.CD_DS2_en_excel_v2_5455395 (1).xls"  # Specify the filename to save the downloaded file

    response = requests.get(url)

    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print("File downloaded successfully.")
    else:
        print("Failed to download the file. Error:", response.status_code)
         
    GGNI_ini = pd.read_excel(filename, sheet_name=0)
    GGNI_pcap_ini = pd.read_excel(filename_pcap, sheet_name=0)
    GGNI = process_data(GGNI_ini)
    GGNI_pcap = process_data(GGNI_pcap_ini)
    graph_div21 = line_plot2(GGNI, 'Gross National Income - Atlas Method, Current USD')
    graph_div211 = line_plot2(GGNI_pcap, 'Gross National Income Per Capita - Atlas Method, Current USD')
    
    choro_GGNI = process_chorodata(GGNI_ini)
    choro_GGNI_pcap = process_chorodata(GGNI_pcap_ini)
    
    graph_div1990 = choropleth_plotter_ggni(choro_GGNI, '1990', 'GNI, Atlas Method: 1990 (log scale)')
    graph_div2000 = choropleth_plotter_ggni(choro_GGNI, '2000', 'GNI, Atlas Method: 2000 (log scale)')
    graph_div2010 = choropleth_plotter_ggni(choro_GGNI, '2010', 'GNI, Atlas Method: 2010 (log scale)')
    graph_div2021 = choropleth_plotter_ggni(choro_GGNI, '2021', 'GNI, Atlas Method: 2021 (log scale)')
    graph_div1990_pcap = choropleth_plotter_ggni_pcap(choro_GGNI_pcap, '1990', 'GDP Per Capita, Atlas Method: 1990 (nominal scale)')
    graph_div2000_pcap = choropleth_plotter_ggni_pcap(choro_GGNI_pcap, '2000', 'GDP Per Capita, Atlas Method: 2000 (nominal scale)')
    graph_div2010_pcap = choropleth_plotter_ggni_pcap(choro_GGNI_pcap, '2010', 'GDP Per Capita, Atlas Method: 2010 (nominal scale)')
    graph_div2021_pcap = choropleth_plotter_ggni_pcap(choro_GGNI_pcap, '2021', 'GDP Per Capita, Atlas Method: 2021 (nominal scale)')

    
    context = {
        'graph_div21' : graph_div21,
        'graph_div211' : graph_div211,
        'graph_div1990' : graph_div1990,
        'graph_div2000' : graph_div2000,
        'graph_div2010' : graph_div2010,
        'graph_div2021' : graph_div2021,
        'graph_div1990_pcap' : graph_div1990_pcap,
        'graph_div2000_pcap' : graph_div2000_pcap,
        'graph_div2010_pcap' : graph_div2010_pcap,
        'graph_div2021_pcap' : graph_div2021_pcap,
    }
    return render(request, 'ggni.html', context)

def GForex(request):    
    url = "https://api.worldbank.org/v2/en/indicator/FI.RES.TOTL.CD?downloadformat=excel"
    filename = "graphgen_app/files/API_FI.RES.TOTL.CD_DS2_en_excel_v2_5455044.xls"  # Specify the filename to save the downloaded file

    response = requests.get(url)

    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print("File downloaded successfully.")
    else:
        print("Failed to download the file. Error:", response.status_code)
        
    Gforex_ini = pd.read_excel(filename, sheet_name=0)
    Gforex = process_data(Gforex_ini)
    graph_div20 = line_plot2(Gforex, 'Global Forex Reserves (Including Gold)')
    return render(request, 'GForex.html', {'graph_div20': graph_div20})

def GEmissions(request):    
    Emm_ini = pd.read_excel("graphgen_app/files/API_EN.ATM.GHGT.KT.CE_DS2_en_excel_v2_5455104.xls", sheet_name=0)
    CO2_ini = pd.read_excel("graphgen_app/files/API_EN.ATM.CO2E.KT_DS2_en_excel_v2_5455447.xls", sheet_name=0)
    CO2_pcap_ini = pd.read_excel("graphgen_app/files/API_EN.ATM.CO2E.PC_DS2_en_excel_v2_5455036.xls", sheet_name=0)
    Meth_ini = pd.read_excel("graphgen_app/files/API_EN.ATM.METH.KT.CE_DS2_en_excel_v2_5455345.xls", sheet_name=0)
    Nox_ini = pd.read_excel("graphgen_app/files/API_EN.ATM.NOXE.KT.CE_DS2_en_excel_v2_5456130.xls", sheet_name=0)
    
    Emm = process_data(Emm_ini)
    CO2 = process_data(CO2_ini)
    CO2_pcap = process_data(CO2_pcap_ini)
    Meth = process_data(Meth_ini)
    Nox = process_data(Nox_ini)
    
    graph_div22 = line_plot2(Emm, 'Total Greenhouse Gas Emmissions (kt of CO2 equivalent)')
    graph_div221 = line_plot2(CO2, 'CO2 Emissions (kt)')
    graph_div222 = line_plot2(CO2_pcap, 'CO2 Emissions (metric tons per capita)')
    graph_div223 = line_plot2(Meth, 'Methane Emissions (kt of CO2 equivalent)')
    graph_div224 = line_plot2(Nox, 'Nitrous Oxide Emissions (thousand metric tons of CO2 equivalent)')
    
    context = {
        'graph_div22' : graph_div22,
        'graph_div221' : graph_div221,
        'graph_div222' : graph_div222,
        'graph_div223' : graph_div223,
        'graph_div224' : graph_div224,
    }
    
    return render(request, 'GEmissions.html', context)

def GForest(request):    
    forest_ini = pd.read_excel("graphgen_app/files/API_AG.LND.FRST.K2_DS2_en_excel_v2_5457123.xls", sheet_name=0)
    forest_per_ini = pd.read_excel("graphgen_app/files/API_AG.LND.FRST.ZS_DS2_en_excel_v2_5455353.xls", sheet_name=0)
    
    forest = process_data(forest_ini)
    forest_per = process_data(forest_per_ini)
    
    graph_div23 = line_plot2(forest, 'Forest Area (sq. km)')
    graph_div231 = line_plot2(forest_per, 'Forest Area (Percentage of land area)')
    
    context = {
        'graph_div23' : graph_div23,
        'graph_div231' : graph_div231,
    }
    
    return render(request, 'GForest.html', context)

def GRenewables(request):    
    renew_ini = pd.read_excel("graphgen_app/files/API_EG.ELC.RNEW.ZS_DS2_en_excel_v2_5456820.xls", sheet_name=0)
    
    renew = process_data(renew_ini)
    
    graph_div24 = line_plot2(renew, 'Renewable Energy Output (Percentage of total energy output)')
    
    
    context = {
        'graph_div24' : graph_div24,
    }
    
    return render(request, 'GRenewables.html', context)


# def about(request):
#     return render(request, "about.html",)
#     #return HttpResponse("This is the about Page. Welcome!!")

def services(request):
    return render(request, "services.html", )
    #return HttpResponse("This is the services Page. Welcome!!")

def contacts(request):
    return render(request, "contacts.html", )
    #return HttpResponse("This is the contacts Page. Welcome!!")
    
def documentation(request):
    return render(request, "documentation.html")

def search_results(request):
    query = request.GET.get('query', '').lower()
    
    if query in 'wpi':
        return redirect('wpi')
    elif query in 'cpi':
        return redirect('cpi')
    elif query in 'exchange rates':
        return redirect('exchange-rate')
    elif query in 'foreign reserves':
        return redirect('foreign-reserves')
    elif query in 'key rates':
        return redirect('key-rates')
    elif query in 'gdp rates':
        return redirect('gdp-rates')
    elif query in 'scb food bank credit':
        return redirect('scb-food-bank')
    elif query in 'balance of payments':
        return redirect('balance-of-payments')
    elif query in 'index of industrial production':
        return redirect('iip')
    elif query in 'foreign direct investments fdi':
        return redirect('fdi')
    elif query in 'global consumer price index'  or query in 'global cpi':
        return redirect('gcpi')
    elif query in 'global fdis' or query in 'global foreign direct investments':
        return redirect('gfdi')
    elif query in 'global gdp' or query in 'global gross domestic product':
        return redirect('ggdp')
    elif query in 'global forex':
        return redirect('GForex')
    elif query in 'global gni' or query in 'global gross national income':
        return redirect('ggni')
    elif query in 'global emmmisions':
        return redirect('GEmissions')
    elif query in 'global forest area cover':
        return redirect('GForest')
    elif query in 'global renewable energy':
        return redirect('GRenewable')
    
    # Default case, no match found
    return redirect('')  # Redirect to the homepage or any other appropriate URL

def graph_view(request):
    return render(request, "base.html",)

