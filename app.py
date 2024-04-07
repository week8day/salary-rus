import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st

DATA_SOURCE = 'remote' # 'local' or 'local'
DATA_DIR = 'data/csv/'
IMAGE_DIR = 'data/images/'
WORK_DICT = {
    'rus': {
        'total': 'Всего по экономике',
        'construct': 'Строительство',
        'horeca': 'Гостиницы, кафе',
        'fin': 'Финансы',
        'med': 'Здравоохранение'
    },
    'eng': {
        'total': 'All',
        'construct': 'Construction',
        'horeca': 'HoReCa',
        'fin': 'Finance',
        'med': 'Healthcare'
    }
}
COLORS = ['#aaaaaa', '#2ed573', '#2e73d5', '#d52e73', '#732ed5', '#73d52e', '#d5732e']
INTERFACE_LANG = 'rus'

interface_lang = INTERFACE_LANG
interface_dict = {
    'app_title': {
        'eng': "Salary analysis in Russia",
        'rus': "Анализ зарплат в России"
    },
    'app_slogan': {
        'eng': "The impact of inflation on salary",
        'rus': "Влияние инфляции на уровень заработной платы"
    },
    'inflation_title': {
        'eng': "Inflation, %",
        'rus': "Инфляция, %"
    },
    'unrate_title': {
        'eng': "Unemployment rate, %",
        'rus': "Уровень безработицы, %"
    },
    'chart_title': {
        'eng': "Average salary, RUB",
        'rus': "Средняя заработная плата, руб."
    },
    'chart_title_inf': {
        'eng': "Average salary adjusted for inflation relative to year 2000, RUB",
        'rus': "Средняя заработная плата с учетом инфляции относительно 2000 года, руб."
    },
    'dataframe_title': {
        'eng': "Average salary table",
        'rus': "Таблица средних зарплат"
    },
    'conclusion_title': {
        'eng': "Conclusion",
        'rus': "Выводы"
    },
    'form_title': {
        'eng': "Charts Data",
        'rus': "Параметры графиков"
    },
    'form_input_workcat': {
        'eng': "Select work categories",
        'rus': "Выберите сферы деятельности"
    },
    'form_input_showdata': {
        'eng': "show dataframe",
        'rus': "показать таблицу"
    },
    'form_input_showinflation': {
        'eng': "show inflation",
        'rus': "показать инфляцию"
    },
    'form_input_showunrate': {
        'eng': "show unemployment rate",
        'rus': "показать уровень безработицы"
    },
    'form_input_showreal': {
        'eng': "adjusted salary",
        'rus': "з/п с учетом инфляции"
    },
    'links_title': {
        'eng': "Links",
        'rus': "Ссылки"
    }
}
conclusion_dict = {
    'eng': [
        "With an increased level of inflation, real wages grow more slowly or even decrease with a formal increase in nominal wages.",
        "Until 2008 (the year of the economic crisis), wages in the construction sector were higher than the average in the economy, then there was a downward jump, and since 2013 it has become lower than the average.",
        "In 2020 (the year of the COVID-19 pandemic), there is a marked increase in salaries in the healthcare sector against the background of a slight increase or even decrease in salaries in other areas."
    ],
    'rus': [
        "При повышенном уровне инфляции реальная заработная плата растет медленнее или даже снижается при формальном росте номинальной заработной платы.",
        "До 2008 года (год экономического кризиса) зарплата в сфере строительства была больше средней по экономике, затем был скачок вниз, и с 2013 года она стала ниже средней.",
        "В 2020 году (год пандемии COVID-19) можно отметить выраженный рост зарплаты в сфере здравоохранения на фоне незначительного роста или даже снижения зарплаты в других сферах."
    ]
}


def load_data(source='local'):
    if source == 'remote':
        # Initialize connection
        conn = st.connection("postgresql", type="sql")

        # Perform query
        df = conn.query('SELECT * FROM salary;', ttl="10m")

    else:
        # Salary
        salary_file = DATA_DIR + 'salary.csv'
        df_salary = pd.read_csv(salary_file, delimiter=';', decimal=',', index_col='year')

        # Inflation
        inflation_file = DATA_DIR + 'inflation.csv'
        df_inflation = pd.read_csv(inflation_file, delimiter=';', decimal=',', index_col='year', usecols=['year', 'inf'])

        # Unemployment rate
        unrate_file = DATA_DIR + 'unrate.csv'
        df_unrate = pd.read_csv(unrate_file, delimiter=';', decimal=',', index_col='year')

        # Concatenation
        df = pd.concat([df_salary, df_inflation, df_unrate], axis=1).reindex(df_salary.index)

    return df


def calculate_real_salary(df):

    start_year = min(df.index)
    columns = df.columns

    df_inf = pd.DataFrame(columns=columns, index=df.index)

    for col in columns:
        col_real = [df[col][start_year]]
        col_inf = [df[col][start_year]]

        for i in range(start_year + 1, start_year + len(df)):
            r = col_inf[i - start_year - 1] * (1 + df['inf'][i] / 100)
            col_inf.append(r)
            col_real.append(round(df[col][start_year] * df[col][i] / r, 1))

        df_inf[col] = col_real

    return df_inf


def process_main_page():
    show_main_page()
    process_side_bar_inputs()


def show_main_page():
    global df, df_inf

    logo_image = Image.open(IMAGE_DIR + 'logo.png')
    icon_image = Image.open(IMAGE_DIR + 'icon.png')

    st.set_page_config(
        layout="wide",
        initial_sidebar_state="auto",
        page_title=interface_dict['app_title'][interface_lang],
        page_icon=icon_image
    )

    col1, col2 = st.columns((1, 4))
    col1.image(logo_image, width=120)
    col2.title(interface_dict['app_title'][interface_lang])

    st.text(interface_dict['app_slogan'][interface_lang])

    df = load_data(DATA_SOURCE).rename(columns=WORK_DICT[interface_lang])

    df_inf = calculate_real_salary(df)


def write_user_data(user_data):
    if user_data['ShowInflation']:
        st.subheader(interface_dict['inflation_title'][interface_lang])
        chart_inflation_data = df['inf']
        st.line_chart(data=chart_inflation_data, color='#ff00aa', height=150)

    if user_data['ShowUnrate']:
        st.subheader(interface_dict['unrate_title'][interface_lang])
        chart_unrate_data = df['unrate']
        st.line_chart(data=chart_unrate_data, color='#00dd99', height=150)

    if user_data['ShowReal']:
        st.subheader(interface_dict['chart_title_inf'][interface_lang])
        chart_data = df_inf[user_data['WorkCat'] + [WORK_DICT[interface_lang]['total']]]
    else:
        st.subheader(interface_dict['chart_title'][interface_lang])
        chart_data = df[user_data['WorkCat'] + [WORK_DICT[interface_lang]['total']]]
    # chart_data.rename(index={'b': '21 - 34', 'c': '35 - 49', 'd': '50 - 64', 'e': '> 65'}, inplace=True)
    st.line_chart(data=chart_data, color=COLORS[:len(user_data['WorkCat']) + 1], height=350)

    if user_data['ShowData']:
        df_salary_cols = list(WORK_DICT[interface_lang].values())
        st.subheader(interface_dict['dataframe_title'][interface_lang])
        if user_data['ShowReal']:
            st.write(df_inf[df_salary_cols])
        else:
            st.write(df[df_salary_cols])

    st.subheader(interface_dict['conclusion_title'][interface_lang])
    for i, p in enumerate(conclusion_dict[interface_lang]):
        st.write(str(i + 1) + '. ' + p)


def process_side_bar_inputs():
    global interface_lang
    st.sidebar.header(interface_dict['form_title'][interface_lang])
    user_input_df = sidebar_input_features()

    write_user_data(user_input_df)


def sidebar_input_features():
    work_cat = list(WORK_DICT[interface_lang].values())
    WorkCat = st.sidebar.multiselect(
        interface_dict['form_input_workcat'][interface_lang],
        work_cat[1:],
        work_cat[1:]
    )

    ShowData = st.sidebar.toggle(
        interface_dict['form_input_showdata'][interface_lang],
        value=True
    )

    ShowInflation = st.sidebar.toggle(
        interface_dict['form_input_showinflation'][interface_lang],
        value=True
    )

    ShowUnrate = st.sidebar.toggle(
        interface_dict['form_input_showunrate'][interface_lang],
        value=False
    )

    ShowReal = st.sidebar.toggle(
        interface_dict['form_input_showreal'][interface_lang],
        value=False
    )

    data = {
        "WorkCat": WorkCat,
        "ShowData": ShowData,
        "ShowReal": ShowReal,
        "ShowInflation": ShowInflation,
        "ShowUnrate": ShowUnrate
    }

    st.sidebar.text('')
    st.sidebar.subheader(interface_dict['links_title'][interface_lang])

    github_url = "https://github.com/week8day/salary-rus"
    st.sidebar.write("Github: %s" % github_url)

    return data


if __name__ == "__main__":
    process_main_page()
