import streamlit as st
import pickle
import pandas as pd
#https://pypi.org/project/yfinance/
import yfinance as yf
import predictions
import matplotlib.pyplot as plt

st.set_page_config(
    page_icon='📖',
    initial_sidebar_state='expanded'
)

st.title('The Blockchain Guru: Its Crypto, Not Cryptic')

page = st.sidebar.selectbox(
    'Page',
    ('Home','What even is a cryptocurrency?','Model Performance')
)

@st.cache
def load_data():
    df = pd.read_csv('data/austen_poe.csv')
    return df
if page == 'Home':
    st.subheader('Welcome to the Blockchain Guru, where we demystefy the cryptocurrency market because as we always say, it crypto, not cryptic')
    st.subheader('Who/What is the Blockchain Guru?')
    st.write('We are a platform that is trying to do the impossible! Cryptocurrency is a relatively new phenominon that has taken people by storm. Some people love and others hate it. The Blockchain Guru seeeks to make cryptocurrencies more approachable so that they don\'t let fear deter them from a potential opportunity for profit.' )
    st.subheader('Can you really predict the future?')
    st.write('No prediction will ever be perfect because of the chaos that is life. Our models try to make very educated guesses so that you can take the best action based on current information. We suggest users not to rely on our models and to do more research before making any trading decisions.')
    st.subheader('What even is a cryptocurrency?')
    st.write('We have a page dedicated to explaining that! Click on the drop down menu on the left and look for "What even is a cryptocurrency?" ')
        
    
if page == 'What even is a cryptocurrency?':
    st.subheader('What even is a cryptocurrency?')
    st.write('Cryptocurrency is a decentralized digital currency that is built with blockchain technology. This is a lot of words so let us break that sentence down. Digital currency  is just money in a digital format. Decentralized means that it isn’t controlled by a single entity like a government. Cryptocurrencies are controlled by a communal ledger that keeps track of transactions in a blockchain. A blockchain is a type of database that’s distributed across many computers around the world. Transactions are recorded in “blocks” and as more transaction data is generated, more blocks are created and these blocks  are then linked together on a “chain”. Each transaction is checked using validation techniques to prevent fraud. So to rephrase the first sentence,  cryptocurrency is a form of digital money maintained by a communal ledger which is built on  a network of databases that collect validated transaction data. Think of cryptocurrency as a monetary system with a record keeping structure so coordinated, there is no need to trade physical money.')
    
if page == 'Model Performance':
    st.subheader('Lets take a look to see how well our models have been performing recently.')
    st.write('Generating Predictions (this might take a minute)')
    fig,ax= predictions.predict()
    st.pyplot(fig)

elif page == 'EDA':
    pass