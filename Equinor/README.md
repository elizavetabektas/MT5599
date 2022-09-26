# KAI News and Commodity Prices

This repository is used for 2022 Summer Intern Project News and Commodity Prices. 

## Description

This application supports traders at Equinor by improving the timeliness and quality of natural gas trading decisions. 

Running of the application automates the scraping and analysis of news tweets related to the natural gas market on Twitter via Natural Language Processing (NLP). The output is a frontend visualisation of today's trending topics, historic trend of the topics and the change of occurrence of keywords under each topic tag for today compared to yesterday.

The programme contains a master Shell script, Python scripts for collecting tweets, topic modelling and visualisation to generate a streamlit dashboard, plus files containing the input configuration options.

## Getting Started

### Requirements

Python modules required are stored in the file: <code> requirements.txt </code>

### Running the programme

Run the master Shell script in the root folder: 

<code> sh master.sh </code>

The Shell script will install the required python modules and execute the Python files. A dashboard is created when the programme finishes running.

### Dashboard visualisation

Go to address <code>localhost:8501</code> 

A dash board is generated contains 4 graphs. The graphs are interactive with drop down list, showing daily trends relating to inferred topics and named entities. Entities can be chosen from a drop down list of organisations, geopolitical entities, people and nationalities.  Historic TTF daily closing price data is also plotted in a chart.

### Configurations

The programme allows change of several inputs, which can be done altering the files below: 

<code>input_twitter_handles.txt</code> for tweets from selected Twitter handles.

<code>blacklist.txt</code> for list of keywords to block in the topic modelling.

<code>keywords_lemmatised.txt</code>

## How it Works

- For each run, tweets posted through selected handles are scraped and formatted (length filtering, adding keyword tags and removing blacklisted tweets).
- The tweets are then fed into NLP models: spaCy's NER model and a custom clustering algorithm using transformer embeddings, UMAP manifold projection for dimensionality reduction, HDBSCAN density-based clustering and C-TFIDF for keyword extraction.
- A streamlit dashboard app is then created for illustration.



