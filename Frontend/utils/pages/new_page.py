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

def new_page():
    import spacy
    from spacytextblob.spacytextblob import SpacyTextBlob

    @st.cache(allow_output_mutation=True)
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

    # def create_color_map(palette, num_colors, start):
    #     cmap = plt.get_cmap(palette)
    #     color_dict = {}
    #     for i in range(start, start + num_colors):
    #         color_dict[i] = cmap(i)
    #     return color_dict

    def standardize(text):
        text = re.sub('[^a-zA-Z\d\s]', '', text)
        text = text.lower()
        return text

    # Load the data from JSON file
    with open("utils/data/combined_text.json", "r") as file:
        data = json.load(file)

    # Access the data in the dictionary
    income_text = data["income"]["text"]
    health_text = data["health"]["text"]
    education_text = data["education"]["text"]
    social_relationship_text = data["social_relationship"]["text"]
    culture_and_leisure_text = data["culture_and_leisure"]["text"]
    sense_of_security_text = data["sense_of_security"]["text"]
    environmental_protection_text = data["environmental_protection"]["text"]

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

    def generate_pie_chart(text):
        text_c = re.sub('[^A-Za-z0-9°]+', ' ', text).lower()
        df_words = get_df(text_c)
        print(df_words)

        fig = px.pie(df_words[0:30], values='count', names='words',
                     color_discrete_sequence=list(sns.color_palette(palette='Reds_r', n_colors=30).as_hex()))
        fig.update_traces(textposition='auto', textinfo='percent+label', hole=.6, hoverinfo="label+percent+name",
                          domain=dict(x=[0.1, 0.9], y=[0.1, 0.9]))
        fig.update_layout(width=600, height=500, margin=dict(t=0, l=0, r=0, b=0))
        return fig

    # def generate_sunburst_chart(text, contents):
    #     pr_text = []
    #     for i in contents:
    #         idx1 = contents.index(i)
    #         if (idx1 >= 0) and (idx1 <= len(contents) - 2):
    #             text_s1 = text.split('\n\n\n== ' + i)[0]
    #             text_s2 = text_s1.split('\n\n\n== ' + contents[idx1 + 1])[0]
    #             pr_text.append(text_s2)
    #         else:
    #             pass
    #
    #     cn_clean_text = [re.sub('[^A-Za-z0-9°]+', ' ', t).lower() for t in pr_text]
    #     df_cn_words = [list(get_df(i)['words'][0:10]) for i in cn_clean_text]
    #     df_cn_count = [list(get_df(i)['count'][0:10]) for i in cn_clean_text]
    #     df_cn_content = [[i.lower()] * len(j) for i, j in zip(contents, df_cn_words)]
    #
    #     df_cont = pd.DataFrame(zip(sum(df_cn_content, []), sum(df_cn_words, []), sum(df_cn_count, [])),
    #                            columns=['contents', 'words', 'count'])
    #
    #     df_sum = df_cont.groupby(['contents']).sum().reset_index()
    #
    #     pre_words = [i.split(' ')[0] for i in sum(df_cn_content, [])]
    #     sb_words = [j + '_' + i + ' ' + str(k) for i, j, k in
    #                 zip(sum(df_cn_words, []), pre_words, sum(df_cn_count, []))] + list(df_sum['contents'])
    #     sb_count = sum(df_cn_count, []) + list(df_sum['count'])
    #     sb_contents = sum(df_cn_content, []) + ['Climate change'] * len(list(df_sum['contents']))
    #
    #     list_cn_count = sum(df_cn_count, [])
    #     nc = max(list_cn_count) - min(list_cn_count) + 1
    #     color_w = create_color_map('Reds', nc, min(list_cn_count))
    #
    #     list_sum_count = list(df_sum['count'])
    #     nw = max(list_sum_count) - min(list_sum_count) + 1
    #     color_c = create_color_map('Reds', nw, min(list_sum_count))
    #
    #     sb_color = [color_w.get(i) for i in sum(df_cn_count, [])] + [color_c.get(i) for i in list(df_sum['count'])]
    #
    #     fig = go.Figure(go.Sunburst(labels=sb_words,
    #                                 parents=sb_contents,
    #                                 values=sb_count,
    #                                 marker=dict(colors=sb_color)
    #                                 ))
    #     fig.update_layout(width=600, height=500, margin=dict(t=0, l=0, r=0, b=0))  # smaller size
    #     return fig

    st.title("🎈 Twitter Text Analysis in Seven Happiness Aspects in Australia")
    # We need to set up session state via st.session_state so that app interactions don't reset the app.
    if not "valid_inputs_received" in st.session_state:
        st.session_state["valid_inputs_received"] = False

    ############ SIDEBAR CONTENT ############
    st.sidebar.write("")
    API_KEY = st.sidebar.text_input(
        "Enter your HuggingFace API key",
        help="Once you created you HuggingFace account, you can get your free API token in your settings page: https://huggingface.co/settings/tokens",
        type="password",
    )

    # Adding the HuggingFace API inference URL.
    API_URL = "https://api-inference.huggingface.co/models/valhalla/distilbart-mnli-12-3"

    # Now, let's create a Python dictionary to store the API headers.
    headers = {"Authorization": f"Bearer {API_KEY}"}

    st.sidebar.markdown("---")

    st.sidebar.write(
    """
    App created by [Charly Wargnier](https://twitter.com/DataChaz) using [Streamlit](https://streamlit.io/)🎈 and [HuggingFace](https://huggingface.co/inference-api)'s [Distilbart-mnli-12-3](https://huggingface.co/valhalla/distilbart-mnli-12-3) model.
    """
    )

    ############ TABBED NAVIGATION ############

    # First, we're going to create a tabbed navigation for the app via st.tabs()
    # tabInfo displays info about the app.
    # tabMain displays the main app.
    IncomeTab, EducationTab, HealthTab, SocialRelationshipTab, CultureLTab, SenseTab, EnvironmentTab = st.tabs(["Income", "Education", "Health", "Social Relationship", "Culture and Leisure", "Sense of security", "Environmental protection"])

    with IncomeTab:
        st.subheader("What is Streamlit?")
        st.markdown(
            "[Streamlit](https://streamlit.io) is a Python library that allows the creation of interactive, data-driven web applications in Python."
        )
        # Adding the search feature
        st.markdown("#### Search Keywords")

        with st.sidebar:
            keyword = st.text_input("Enter a keyword to search in the text", value="income")
            submit_button = st.button("Submit")

        # Search using the default keyword ('income') or the user input keyword
        if keyword:
            # Assuming that income_text is a list of sentences
            search_results = [line for line in income_text.split("\n") if keyword.lower() in line.lower()]
            if len(search_results) > 0:
                st.markdown(f"#### 20 random lines containing the keyword: {keyword}")
                if len(search_results) > 20:
                    random_search_results = random.sample(search_results, 20)
                else:
                    random_search_results = search_results

                result_with_sentiment_and_subjectivity = [
                    {"Text": res, "Sentiment": sentiment(res), "Subjectivity": subjectivity(res)} for res in
                    random_search_results]

                df = pd.DataFrame(result_with_sentiment_and_subjectivity)
                st.dataframe(df, width=1200)
            else:
                st.error(f"No lines found containing the keyword: {keyword}")

        Income_1, Income_2 = st.columns((1, 1))
        with Income_1:
            word_cloud(income_text, "Word Cloud for Income")
        with Income_2:
            pie_chart = generate_pie_chart(income_text)
            st.plotly_chart(pie_chart)


    with HealthTab:
        st.subheader("What is Streamlit?")
        st.write(income_text)
        st.markdown(
            "[Streamlit](https://streamlit.io) is a Python library that allows the creation of interactive, data-driven web applications in Python."
        )

    with SocialRelationshipTab:
        st.subheader("What is Streamlit?")
        st.write(income_text)
        st.markdown(
            "[Streamlit](https://streamlit.io) is a Python library that allows the creation of interactive, data-driven web applications in Python."
        )

    with CultureLTab:
        st.subheader("What is Streamlit?")
        st.write(income_text)
        st.markdown(
            "[Streamlit](https://streamlit.io) is a Python library that allows the creation of interactive, data-driven web applications in Python."
        )
    with SenseTab:
        st.subheader("What is Streamlit?")
        st.write(income_text)
        st.markdown(
            "[Streamlit](https://streamlit.io) is a Python library that allows the creation of interactive, data-driven web applications in Python."
        )
    with EnvironmentTab:
        st.subheader("What is Streamlit?")
        st.write(income_text)
        st.markdown(
            "[Streamlit](https://streamlit.io) is a Python library that allows the creation of interactive, data-driven web applications in Python."
        )
    with EducationTab:

        st.write("")
        st.markdown(
            """
    
        Classify keyphrases on the fly with this mighty app. No training needed!
    
        """
        )

        st.write("")

        # Now, we create a form via `st.form` to collect the user inputs.

        # All widget values will be sent to Streamlit in batch.
        # It makes the app faster!

        with st.form(key="my_form"):

            ############ ST TAGS ############

            # We initialize the st_tags component with default "labels"

            # Here, we want to classify the text into one of the following user intents:
            # Transactional
            # Informational
            # Navigational

            labels_from_st_tags = st_tags(
                value=["Transactional", "Informational", "Navigational"],
                maxtags=3,
                suggestions=["Transactional", "Informational", "Navigational"],
                label="",
            )

            # The block of code below is to display some text samples to classify.
            # This can of course be replaced with your own text samples.

            # MAX_KEY_PHRASES is a variable that controls the number of phrases that can be pasted:
            # The default in this app is 50 phrases. This can be changed to any number you like.

            MAX_KEY_PHRASES = 50

            new_line = "\n"

            pre_defined_keyphrases = [
                "I want to buy something",
                "We have a question about a product",
                "I want a refund through the Google Play store",
                "Can I have a discount, please",
                "Can I have the link to the product page?",
            ]

            # Python list comprehension to create a string from the list of keyphrases.
            keyphrases_string = f"{new_line.join(map(str, pre_defined_keyphrases))}"

            # The block of code below displays a text area
            # So users can paste their phrases to classify

            text = st.text_area(
                # Instructions
                "Enter keyphrases to classify",
                # 'sample' variable that contains our keyphrases.
                keyphrases_string,
                # The height
                height=200,
                # The tooltip displayed when the user hovers over the text area.
                help="At least two keyphrases for the classifier to work, one per line, "
                + str(MAX_KEY_PHRASES)
                + " keyphrases max in 'unlocked mode'. You can tweak 'MAX_KEY_PHRASES' in the code to change this",
                key="1",
            )

            # The block of code below:

            # 1. Converts the data st.text_area into a Python list.
            # 2. It also removes duplicates and empty lines.
            # 3. Raises an error if the user has entered more lines than in MAX_KEY_PHRASES.

            text = text.split("\n")  # Converts the pasted text to a Python list
            linesList = []  # Creates an empty list
            for x in text:
                linesList.append(x)  # Adds each line to the list
            linesList = list(dict.fromkeys(linesList))  # Removes dupes
            linesList = list(filter(None, linesList))  # Removes empty lines

            if len(linesList) > MAX_KEY_PHRASES:
                st.info(
                    f"❄️ Note that only the first "
                    + str(MAX_KEY_PHRASES)
                    + " keyphrases will be reviewed to preserve performance. Fork the repo and tweak 'MAX_KEY_PHRASES' in the code to increase that limit."
                )

                linesList = linesList[:MAX_KEY_PHRASES]

            submit_button = st.form_submit_button(label="Submit")

        ############ CONDITIONAL STATEMENTS ############

        # Now, let us add conditional statements to check if users have entered valid inputs.
        # E.g. If the user has pressed the 'submit button without text, without labels, and with only one label etc.
        # The app will display a warning message.

        if not submit_button and not st.session_state.valid_inputs_received:
            st.stop()

        elif submit_button and not text:
            st.warning("❄️ There is no keyphrases to classify")
            st.session_state.valid_inputs_received = False
            st.stop()

        elif submit_button and not labels_from_st_tags:
            st.warning("❄️ You have not added any labels, please add some! ")
            st.session_state.valid_inputs_received = False
            st.stop()

        elif submit_button and len(labels_from_st_tags) == 1:
            st.warning("❄️ Please make sure to add at least two labels for classification")
            st.session_state.valid_inputs_received = False
            st.stop()

        elif submit_button or st.session_state.valid_inputs_received:

            if submit_button:

                # The block of code below if for our session state.
                # This is used to store the user's inputs so that they can be used later in the app.

                st.session_state.valid_inputs_received = True

            ############ MAKING THE API CALL ############

            # First, we create a Python function to construct the API call.

            def query(payload):
                response = requests.post(API_URL, headers=headers, json=payload)
                return response.json()

            # The function will send an HTTP POST request to the API endpoint.
            # This function has one argument: the payload
            # The payload is the data we want to send to HugggingFace when we make an API request

            # We create a list to store the outputs of the API call

            list_for_api_output = []

            # We create a 'for loop' that iterates through each keyphrase
            # An API call will be made every time, for each keyphrase

            # The payload is composed of:
            #   1. the keyphrase
            #   2. the labels
            #   3. the 'wait_for_model' parameter set to "True", to avoid timeouts!

            for row in linesList:
                api_json_output = query(
                    {
                        "inputs": row,
                        "parameters": {"candidate_labels": labels_from_st_tags},
                        "options": {"wait_for_model": True},
                    }
                )

                # Let's have a look at the output of the API call
                # st.write(api_json_output)

                # All the results are appended to the empty list we created earlier
                list_for_api_output.append(api_json_output)

                # then we'll convert the list to a dataframe
                df = pd.DataFrame.from_dict(list_for_api_output)

            st.success("✅ Done!")

            st.caption("")
            st.markdown("### Check the results!")
            st.caption("")

            # st.write(df)

            ############ DATA WRANGLING ON THE RESULTS ############
            # Various data wrangling to get the data in the right format!

            # List comprehension to convert the score from decimals to percentages
            f = [[f"{x:.2%}" for x in row] for row in df["scores"]]

            # Join the classification scores to the dataframe
            df["classification scores"] = f

            # Rename the column 'sequence' to 'keyphrase'
            df.rename(columns={"sequence": "keyphrase"}, inplace=True)

            # The API returns a list of all labels sorted by score. We only want the top label.

            # For that, we need to select the first element in the 'labels' and 'classification scores' lists
            df["label"] = df["labels"].str[0]
            df["accuracy"] = df["classification scores"].str[0]

            # Drop the columns we don't need
            df.drop(["scores", "labels", "classification scores"], inplace=True, axis=1)

            # st.write(df)

            # We need to change the index. Index starts at 0, so we make it start at 1
            df.index = np.arange(1, len(df) + 1)

            # Display the dataframe
            st.write(df)

            cs, c1 = st.columns([2, 2])




            # The code below is for the download button
            # Cache the conversion to prevent computation on every rerun

            with cs:

                # Cache the conversion to prevent computation on every rerun
                @st.cache_data
                def convert_df(df):
                    return df.to_csv().encode("utf-8")

                csv = convert_df(df)

                st.caption("")

                st.download_button(
                    label="Download results",
                    data=csv,
                    file_name="classification_results.csv",
                    mime="text/csv",
                )