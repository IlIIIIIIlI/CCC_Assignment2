from datetime import date, datetime
import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import requests
import random
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import json
@st.cache_data
def load_data():
    df = pd.read_csv('./utils/data/marital.csv', na_values=[' ', 'NA', 'na', 'N/A', 'n/a'])
    df = df.fillna(0)
    # Groupby lga_code_2021 and sum
    df = df.groupby('lga_code_2021').sum().reset_index()
    # twitter marriage
    # df_t = pd.read_csv('./utils/data/page3-data.csv')
    #----------------------------------------------------------------
    with open('config.json') as f:
        localhost = json.load(f)['IP']

    # Fetch data from server
    r = requests.get(f'http://{localhost}:8000/page3data', timeout=200)
    # parse json
    df_t = r.json()
    df_t = pd.json_normalize(df_t)
    # ----------------------------------------------------------------

    df_income = pd.read_csv('./utils/data/income.csv')
    df_income2 = df_income.copy()
    df_mortgage = pd.read_csv('./utils/data/mortgage.csv')

    for col in df_income.columns[2:]:
        df_income[col] = df_income[col].str.replace(',', '').astype(int)

    df_income['$0-$399'] = df_income['Negative income'] + df_income['Nil income'] + df_income['$1-$149'] + df_income['$150-$299'] + df_income['$300-$399']
    df_income['$400-$999'] = df_income['$400-$499'] + df_income['$500-$649'] + df_income['$650-$799'] + df_income['$800-$999']
    df_income['$1,000-$1,999'] = df_income['$1,000-$1,249'] + df_income['$1,250-$1,499'] + df_income['$1,500-$1,749'] + df_income['$1,750-$1,999']
    df_income['$2,000 or more'] = df_income['$2,000-$2,999'] + df_income['$3,000 or more']

    df_income = df_income[['city', '$0-$399', '$400-$999', '$1,000-$1,999', '$2,000 or more']]

    return df, df_t, df_income, df_mortgage,df_income2


def official():
    st.sidebar.markdown("# Spatial Urban Data Observatory (SUDO)")
    st.sidebar.markdown(
        "SUDO is a data platform providing official statistics for comprehensive analysis and comparison in social media analytics.")

    df, df_t, df_income, df_mortgage,df_income2 = load_data()
    st.title('🏢Sudo - Official Statistics Comparative Analysis')

    # Concatenate the city options from both datasets
    city_options = df['lga_code_2021'].unique()
    selected_cities = st.multiselect('Select City', city_options, default=['1gsyd', '2gmel', '3gbri', '4gade', '5gper'])

    df_t_filtered = df_t[df_t['city'].isin(selected_cities)]
    col1_a, col1_b, col1_c = st.columns(3)
    colors = ['#2a9d8f', '#219ebc', '#e9c46a', '#bc6c25', '#e76f51', '#9f86c0', '#ffcfd2', '#f2cc8f', '#fbf8cc']

    with col1_a:
        # Pie chart
        st.header("Marital Tweets distribution💍")
        pie_data = df_t_filtered.groupby(['city']).sum().reset_index()[['city', 'marriage_count']]
        pie_chart = alt.Chart(pie_data).mark_arc(innerRadius=50).encode(
            theta='marriage_count:Q',
            color=alt.Color('city:N', legend=alt.Legend(title='City'), scale=alt.Scale(range=colors)),
            tooltip=['city', 'marriage_count']
        ).properties(
            width=300,
            height=300
        )

        st.altair_chart(pie_chart, use_container_width=True)

        # Stack bar chart
        st.subheader("Sentiment Distribution")
        stack_data = df_t_filtered[['city', 'marriage_count', 'marriage_positive_rate']].copy()
        stack_data['marriage_positive_count'] = stack_data['marriage_count'] * stack_data['marriage_positive_rate']
        stack_data['marriage_negative_count'] = stack_data['marriage_count'] * (
                    1 - stack_data['marriage_positive_rate'])
        stack_data = pd.melt(stack_data, id_vars='city',
                             value_vars=['marriage_positive_count', 'marriage_negative_count'])
        stack_data.rename(columns={'variable': 'marriage_status'}, inplace=True)

        stack_chart = alt.Chart(stack_data).mark_bar(size=18).encode(
            y=alt.Y('city:O', title='City'),
            x=alt.X('value:Q', title='Count of Marriages'),
            color=alt.Color('marriage_status:N',
                            scale=alt.Scale(domain=['marriage_positive_count', 'marriage_negative_count'],
                                            range=['#aaf683', '#ff5c8a'])),
            tooltip=['city', 'marriage_status', 'value']
        ).properties(height=180)

        st.altair_chart(stack_chart, use_container_width=True)

    with col1_b:
        # Pie chart
        st.header("Income Tweets distribution💸")
        pie_data = df_t_filtered.groupby(['city']).sum().reset_index()[['city', 'income_count']]
        pie_chart = alt.Chart(pie_data).mark_arc(innerRadius=50).encode(
            theta='income_count:Q',
            color=alt.Color('city:N', legend=alt.Legend(title='City'), scale=alt.Scale(range=colors)),
            tooltip=['city', 'income_count']
        ).properties(
            width=300,
            height=300
        )

        st.altair_chart(pie_chart, use_container_width=True)

        # Stack bar chart
        st.header("Sentiment Distribution")
        stack_data = df_t_filtered[['city', 'income_count', 'income_positive_rate']].copy()
        stack_data['income_positive_count'] = stack_data['income_count'] * stack_data['income_positive_rate']
        stack_data['income_negative_count'] = stack_data['income_count'] * (
                1 - stack_data['income_positive_rate'])
        stack_data = pd.melt(stack_data, id_vars='city',
                             value_vars=['income_positive_count', 'income_negative_count'])
        stack_data.rename(columns={'variable': 'income_status'}, inplace=True)

        stack_chart = alt.Chart(stack_data).mark_bar(size=18).encode(
            y=alt.Y('city:O', title='City'),
            x=alt.X('value:Q', title='Count of tweets about income'),
            color=alt.Color('income_status:N',
                            scale=alt.Scale(domain=['income_positive_count', 'income_negative_count'],
                                            range=['#aaf683', '#ff5c8a'])),
            tooltip=['city', 'income_status', 'value']
        ).properties(height=180)

        st.altair_chart(stack_chart, use_container_width=True)

    with col1_c:
        # Pie chart
        st.header("Rent Tweets distribution🏘️")
        pie_data = df_t_filtered.groupby(['city']).sum().reset_index()[['city', 'rent_count']]
        pie_chart = alt.Chart(pie_data).mark_arc(innerRadius=50).encode(
            theta='rent_count:Q',
            color=alt.Color('city:N', legend=alt.Legend(title='City'), scale=alt.Scale(range=colors)),
            tooltip=['city', 'rent_count']
        ).properties(
            width=300,
            height=300
        )

        st.altair_chart(pie_chart, use_container_width=True)

        # Stack bar chart
        st.header("Sentiment Distribution")
        stack_data = df_t_filtered[['city', 'rent_count', 'rent_positive_rate']].copy()
        stack_data['rent_positive_count'] = stack_data['rent_count'] * stack_data['rent_positive_rate']
        stack_data['rent_negative_count'] = stack_data['rent_count'] * (
                1 - stack_data['rent_positive_rate'])
        stack_data = pd.melt(stack_data, id_vars='city',
                             value_vars=['rent_positive_count', 'rent_negative_count'])
        stack_data.rename(columns={'variable': 'rent_status'}, inplace=True)

        stack_chart = alt.Chart(stack_data).mark_bar(size=18).encode(
            y=alt.Y('city:O', title='City'),
            x=alt.X('value:Q', title='Count of tweets about rent'),
            color=alt.Color('rent_status:N',
                            scale=alt.Scale(domain=['rent_positive_count', 'rent_negative_count'],
                                            range=['#aaf683', '#ff5c8a'])),
            tooltip=['city', 'rent_status', 'value']
        ).properties(height=180)

        st.altair_chart(stack_chart, use_container_width=True)


    col2_a, col2_b, col2_c = st.columns((1,2,1))
    with col2_a:
        st.markdown("---")
        st.header('Marital Status - SUDO')
        df_filtered = df[df['lga_code_2021'].isin(selected_cities)] if selected_cities else df

        age_groups = ['15_19', '20_24', '25_34', '35_44', '45_54', '55_64', '65_74', '75_84', '85ov']


        for age in age_groups:
            if f'f_{age}_yr_marrd_reg_marrge' in df_filtered.columns and f'm_{age}_yr_marrd_reg_marrge' in df_filtered.columns:
                df_filtered[f'{age}_yr_married'] = df_filtered[f'f_{age}_yr_marrd_reg_marrge'] + df_filtered[
                    f'm_{age}_yr_marrd_reg_marrge']

        value_vars = [f'{age}_yr_married' for age in age_groups]
        value_vars_exist = [var for var in value_vars if var in df_filtered.columns]

        chart_data = pd.melt(df_filtered, id_vars='lga_code_2021', value_vars=value_vars_exist)
        chart_data['variable'] = chart_data['variable'].str.extract('(\d+_\d+)')[0].str.replace('_', '-')

        if 'p_tot_not_married' in df.columns:
            df_filtered['total_not_married'] = df_filtered['p_tot_not_married']

        chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('lga_code_2021:O', title='Great Capital City'),
            y=alt.Y('value:Q', title='Amount of ppl'),
            color=alt.Color('variable:O', legend=alt.Legend(title='Age Group'), scale=alt.Scale(range=colors)),
            tooltip=['lga_code_2021', 'variable', 'value']
        ).properties(width=500, height=300)

        st.altair_chart(chart, use_container_width=True)

        # Stack bar chart
        df_filtered['total_male_married'] = df_filtered[
            [col for col in df_filtered.columns if col.startswith('m_')]].sum(
            axis=1)
        df_filtered['total_female_married'] = df_filtered[
            [col for col in df_filtered.columns if col.startswith('f_')]].sum(
            axis=1)
        gender_data = df_filtered.melt(id_vars='lga_code_2021',
                                       value_vars=['total_male_married', 'total_female_married'])
        gender_data.rename(columns={'variable': 'gender'}, inplace=True)

        gender_chart = alt.Chart(gender_data).mark_bar(size=30).encode(
            y=alt.Y('lga_code_2021:O', title='Great Capital City'),
            x=alt.X('value:Q', title='Amount of ppl'),
            color=alt.Color('gender:O', scale=alt.Scale(domain=['total_male_married', 'total_female_married'],
                                                        range=['#90dbf4', '#ff4d6d'])),
            tooltip=['lga_code_2021', 'gender', 'value']
        ).properties(height=300)

        st.altair_chart(gender_chart, use_container_width=True)

    with col2_b:
        st.markdown("---")
        st.header('Income Status - SUDO')
        selected_city = st.selectbox("Select a city:", df_income['city'].unique())
        # 获取选中城市的数据
        city_data = df_income[df_income['city'] == selected_city]

        # 准备数据
        data_dict = {
            "Income Range": ['$0-$399', '$400-$999', '$1,000-$1,999', '$2,000 or more'],
            "Income": city_data[['$0-$399', '$400-$999', '$1,000-$1,999', '$2,000 or more']].values[0]
        }

        # 创建 DataFrame
        df_income_plotly = pd.DataFrame(data_dict)

        # 创建雷达图
        fig = px.line_polar(df_income_plotly, r='Income', theta='Income Range', line_close=True)

        # 设置雷达图的属性
        fig.update_traces(fill='toself', fillcolor='rgba(0,0,255,0.2)', line_color='blue')
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            polar_bgcolor='rgba(173,216,230,0.3)'  # 设置雷达图背景色为浅蓝色
        )

        st.plotly_chart(fig, use_container_width=True,theme="streamlit",width=300, height=200)  # 使用容器宽度并左对齐

        expander = st.expander("More on income distribution", expanded=False)
        with expander:
            st.write("The size of the circles in the figure below represents the number of people with negative income.")
            st.write("The color represents the median income.")
            # 将字符串数字转换为整数
            for col in df_income2.columns[1:]:
                df_income2[col] = df_income2[col].str.replace(',', '').astype(int)

            # 根据您的描述，创建散点图
            fig = px.scatter(df_income2,
                             x=['$1-$149', '$150-$299', '$300-$399', '$400-$499',
                                '$500-$649', '$650-$799', '$800-$999',
                                '$1,000-$1,249', '$1,250-$1,499', '$1,500-$1,749', '$1,750-$1,999', '$2,000-$2,999',
                                '$3,000 or more'],
                             y='city',
                             size='Negative income',
                             color='Median income',
                             hover_name='Median income',
                             log_x=True,
                             size_max=60)

            # 显示图表
            st.plotly_chart(fig, use_container_width=True,theme="streamlit",width=800, height=600)  # 使用容器宽度并左对齐

    with col2_c:
        st.markdown("---")
        st.header("Rent Payable Status - SUDO")
        scatter_data = df_mortgage.copy()
        scatter_data = scatter_data[scatter_data['gccsa_code_2021'].isin(selected_cities)]
        scatter_chart = alt.Chart(scatter_data).mark_circle(size=150).encode(
            x=alt.X('median_mortgage_repay_monthly:Q',
                    title='Median Monthly Mortgage Repayment',
                    scale=alt.Scale(domain=[1200, scatter_data['median_mortgage_repay_monthly'].max()])),

            y=alt.Y('median_tot_hhd_inc_weekly:Q',
                    title='Median Total Household Income Weekly',
                    scale=alt.Scale(domain=[1400, scatter_data['median_tot_hhd_inc_weekly'].max()])),

            color=alt.Color('gccsa_code_2021:N', legend=alt.Legend(title='City')),
            tooltip=['gccsa_code_2021', 'median_mortgage_repay_monthly', 'median_tot_hhd_inc_weekly']
        ).properties(
            width=500,
            height=500
        )

        st.altair_chart(scatter_chart, use_container_width=True)



