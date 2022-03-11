import streamlit as st 
import pandas as pd
from fetch_data import fetch_comment_data
from fetch_data import url_to_id
from sentiment_analysis import sentiment 
import plotly.express as px


#st.set_page_config(layout="wide")

st.title('youtube comment analyzer')
st.subheader('Only english comments are analyzable')
st.markdown("""
This app retrieves youtube comments and analyzes in various ways.
""")

expander_bar = st.expander("About")
expander_bar.markdown("""
* **Python libraries:**  pandas, streamlit, numpy, plotly, nltk
""")

def get_thumbnail(url):
    id = url_to_id(url)
    img = 'https://img.youtube.com/vi/{}/0.jpg'.format(id)
    return img 

def create_plot(data):
    data = data['sentiment category'].value_counts()
    labels = list(data.index)
    values = list(data)
    fig = px.pie(labels, values=values, 
    names= labels, color = labels, 
    color_discrete_map = {
        'Positive': '#1f77b4',
        'Negative': '#d62728',
        'Neutral': '#7f7f7f'
    })
    return fig


def make_dataframe(data, options = []):
    if len(options) == 0 or options[0] == 'ALL':
        st.header('Youtube comment data')
        st.dataframe(data[['comments','sentiment score']].style.bar(subset=['sentiment score'], color=['#d65f5f','#5fba7d']))
        return data
    else:
        data = data[data['sentiment category'].isin(options)]
        st.header('Youtube comment data')
        st.dataframe(data[['comments','sentiment score']].style.bar(subset=['sentiment score'], color=['#d65f5f','#5fba7d']))
        return data

@st.cache(allow_output_mutation=True)
def get_data(video_url):
    data = fetch_comment_data(video_url)
    data = sentiment(data)
    return data


# sidebar ----------------------------
sidebar = st.sidebar

# header 
sidebar.header('Input Options')
video_url=sidebar.text_input('youtube url')
# multiselect
options = sidebar.multiselect('What sentiment category do you want to see?',
    ['ALL','Positive', 'Negative', 'Neutral'])


col1, col2 = st.columns(2)



if sidebar.button('search'):
    # thumbnail
    st.header('Thumbnail')
    st.image(get_thumbnail(video_url))
    
    # dataframe
    data = get_data(video_url)
    data = make_dataframe(data,options=options)
    

    # pie plot
    fig = create_plot(data)
    st.header('Pie plot')
    st.plotly_chart(fig, use_container_width = True)

    # multiselect
    
    

    









