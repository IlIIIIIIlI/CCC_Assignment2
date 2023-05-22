import streamlit as st
import requests
import pandas as pd
import numpy as np
from streamlit_tags import st_tags  # to add labels on the fly!
import re
import nltk
from wordcloud import WordCloud, STOPWORDS
# Download stopwords
from nltk.corpus import stopwords
from datasets import load_dataset
import matplotlib.pyplot as plt
import json
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
nltk.download('stopwords')
stop_words = set(stopwords.words("english"))
import plotly.graph_objects as go
import random

def Seven_Aspects():
    import spacy
    from spacytextblob.spacytextblob import SpacyTextBlob

    @st.cache_resource()
    def load_nlp_model():
        nlp = spacy.load('en_core_web_sm')
        nlp.add_pipe('spacytextblob')
        return nlp

    nlp = load_nlp_model()

    def sentiment(text):
        doc = nlp(text)
        if doc._.polarity < 0:
            return "Negative"
        elif doc._.polarity == 0:
            return "Neutral"
        else:
            return "Positive"

    def subjectivity(text):
        doc = nlp(text)
        if doc._.subjectivity > 0.5:
            return "Highly Opinionated sentence"
        elif doc._.subjectivity < 0.5:
            return "Less Opinionated sentence"
        else:
            return "Neutral sentence"

    def standardize(text):
        text = re.sub('[^a-zA-Z\d\s]', '', text)
        text = text.lower()
        return text

    # Load the data from JSON file
    with open("utils/data/combined_text.json", "r") as file:
        data = json.load(file)

    # # Load IP address
    # with open('config.json') as f:
    #     localhost = json.load(f)['IP']
    #
    # # Fetch data from server
    # r = requests.get(f'http://{localhost}:8000/page4data', timeout=200)
    # # parse json
    # data = r.json()


    # Count the number of records in each category
    category_counts = {category: len(records["text"].split()) for category, records in data.items()}
    # Access the data in the dictionary
    income_text = data["income"]["text"]
    health_text = data["health"]["text"]
    education_text = data["education"]["text"]
    social_relationship_text = data["social_relationship"]["text"]
    culture_and_leisure_text = data["culture_and_leisure"]["text"]
    sense_of_security_text = data["sense_of_security"]["text"]
    environmental_protection_text = data["environmental_protection"]["text"]
    filtered_text = ''

    def word_cloud(text, title):
        text = standardize(text)
        words = text.split()
        words = ' '.join([word for word in words if word not in stop_words])
        wc = WordCloud(background_color="black", max_words=200, contour_width=3,
                       stopwords=STOPWORDS, max_font_size=50)
        wc.generate(words)
        fig, ax = plt.subplots(figsize=(15, 15), dpi=500)
        ax.set_title(title, fontsize=20)
        ax.imshow(wc.recolor(colormap='magma', random_state=42), cmap=plt.cm.gray, interpolation="bilinear",
                  alpha=0.98)
        ax.axis('off')
        plt.subplots_adjust(top=0.95, bottom=0.05, right=0.95, left=0.05,
                            hspace=0.2, wspace=0.2)
        st.pyplot(fig)

    def get_df(input_text):
        list_words = input_text.split(' ')
        set_words_full = list(set(list_words))
        set_words = [i for i in set_words_full if i not in stop_words]
        count_words = [list_words.count(i) for i in set_words]
        df = pd.DataFrame(zip(set_words, count_words), columns=['words', 'count'])
        df.sort_values('count', ascending=False, inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    def generate_pie_chart(text,colr):
        text_c = re.sub('[^A-Za-z0-9°]+', ' ', text).lower()
        df_words = get_df(text_c)
        fig = px.pie(df_words[0:20], values='count', names='words',
                     color_discrete_sequence=list(sns.color_palette(palette=colr, n_colors=20).as_hex()))
        fig.update_traces(textposition='auto', textinfo='percent+label', hole=.6, hoverinfo="label+percent+name",
                          domain=dict(x=[0.1, 0.9], y=[0.1, 0.9]))
        fig.update_layout(width=600, height=500, margin=dict(t=0, l=0, r=0, b=0))
        return fig

    def tab_info(datas, l_word, h_word, ccolor, emo):
        st.subheader(f"Twitter regarding {h_word}")
        st.markdown(
            f"{h_word} has a positive impact on the happiness of Australian citizens, as it provides greater financial stability, access to better healthcare and education, and increased opportunities for leisure activities and social engagement."
        )

        def display_results(keyword, submit_button):
            search_results = [line for line in datas.split("\n") if keyword.lower() in line.lower()]
            if len(search_results) > 0:
                st.markdown(f"#### {emo}Aussie Twitter on {h_word}: Insights & Opinions: {keyword} (Max 20)")
                if len(search_results) > 20:
                    random_search_results = random.sample(search_results, 20)
                else:
                    random_search_results = search_results

                # Add the API output to the result DataFrame
                result_with_sentiment_and_subjectivity = [
                    {
                        "Text": res,
                        "Sentiment": sentiment(res),
                        "Subjectivity": subjectivity(res),
                    }
                    for i, res in enumerate(random_search_results)
                ]

                # Create the final DataFrame
                df = pd.DataFrame(result_with_sentiment_and_subjectivity)
                st.dataframe(df, width=1500, height=500)

                # Generate word cloud and pie chart for filtered sentences
                filtered_text = "\n".join(random_search_results)
                return filtered_text
            else:
                st.error(f"No lines found containing the keyword: {keyword}")

        if keyword and submit_button:
            filtered_text = display_results(keyword, submit_button)
        elif not submit_button:
            filtered_text = display_results(l_word, True)
        else:
            st.warning("Please click the 'Submit' button to see the results.")

        col1, col2 = st.columns((1, 1))
        with col1:
            st.subheader(f"Words Cloud: 💰🗣️ Exploring {h_word} through {keyword}")
            if len(filtered_text) > 0:
                word_cloud(filtered_text, f"{h_word} frequency")
            else:
                word_cloud(datas, f"{h_word} frequency")
        with col2:
            if len(filtered_text) > 0:
                pie_chart = generate_pie_chart(filtered_text, ccolor)
            else:
                pie_chart = generate_pie_chart(datas, ccolor)
            st.plotly_chart(pie_chart)


    st.title("🎈 Twitter Text Analysis in Seven Happiness Aspects in Australia")

    with st.sidebar:
        st.header("Records Statistics")
        # Convert the dictionary to a pandas DataFrame
        df = pd.DataFrame(list(category_counts.items()), columns=['Category', 'Count'])

        # Sort the DataFrame by the 'Count' column in descending order
        df = df.sort_values('Count', ascending=False)

        # Display the DataFrame as a bar chart in the sidebar
        st.bar_chart(df.set_index('Category'))
        st.markdown("---")

        keyword = st.text_input(f"Enter a keyword to search in the data", value="income")
        submit_button = st.button("Submit")

    ############ TABBED NAVIGATION ############
    # tabInfo displays info about the app.
    IncomeTab, EducationTab, HealthTab, SocialRelationshipTab, CultureLTab, SenseTab, EnvironmentTab = st.tabs(["Income", "Education", "Health", "Social Relationship", "Culture and Leisure", "Sense of security", "Environmental protection"])

    with IncomeTab:
        tab_info(income_text, 'income', 'Income', 'Reds_r', "💵")

    with HealthTab:
        tab_info(health_text, 'health', 'Health', 'Oranges', "🏥")

    with SocialRelationshipTab:
        tab_info(social_relationship_text, 'social', 'Social Relationship', 'YlOrBr', "👥")

    with CultureLTab:
        tab_info(culture_and_leisure_text, 'culture', 'Culture', 'YlGn', "🎭")

    with SenseTab:
        tab_info(sense_of_security_text, 'security', 'Sense of Security', 'PuBuGn', "🔒")

    with EnvironmentTab:
        tab_info(environmental_protection_text, 'environment', 'Environment', 'PuBu', "🌍")

    with EducationTab:
        tab_info(education_text, 'education', 'Education', 'PiYG', "🎓")
