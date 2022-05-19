# import libraries
import os 
import pandas as pd
import numpy as np 
import argparse
import spacy 
from spacytextblob.spacytextblob import SpacyTextBlob
import matplotlib.pyplot as plt

# load and process the data
def load_process_data(file):
    # initiate spacy model
    nlp = spacy.load("en_core_web_sm")
    # add spacy pipe 
    nlp.add_pipe('spacytextblob')
    # define a filepath
    filepath = os.path.join("in", "tabular_examples", file)
    # get the data
    data = pd.read_csv(filepath)
    # split the data according to labels = fake or real 
    real_data = data[data["label"] == "REAL"]
    fake_data = data[data["label"] == "FAKE"]
    return nlp, real_data, fake_data

# get sentiment scores 
def find_sents(nlp, dataframe):
    # create an empty list
    sents = []
    # for every headline in the dataframe under "title"
    for headline in nlp.pipe(dataframe["title"]):
        # get the sentiments of the headline
        sent = headline._.blob.polarity
        # and append them to the list
        sents.append(sent)
    return sents 

# find the GPEs
def find_entities(nlp, dataframe):
    # define an empty list
    GPE = []
    # for every headline in the dataframe under "title"
    for headline in nlp.pipe(dataframe["title"]):
        # for every entity 
        for entity in headline.ents:
            # if the entity is GPE
            if entity.label_ == "GPE":
                # append to the list
                GPE.append(entity.text)
    return GPE

# let's create an output
def create_output(dataframe, sents, GPE):
    # create list out of lists and dataframe column
    out_list = list(zip(dataframe["Unnamed: 0"], sents, GPE, dataframe["title"]))
    # create dataframe and set index
    out_df = pd.DataFrame(out_list, columns = ["ID", "GPE", "Sentiment", "Title"]).set_index("ID")
    out_df = out_df.round(decimals = 3)
    # print to the terminal
    print(out_df)
    return out_df

# save the data frame
def save_csv(dataframe, name):
    # define a path
    path = os.path.join("out", name)
    # save
    dataframe.to_csv(path)
    return dataframe

# get the 20 most common mentioned GPEs in both datasets 
def top20(dataframe, name):
    # get the amount of times each GPEs is mentioned
    dataframe_counts = dataframe.value_counts("GPE")
    # get top 20
    top20_mentions = dataframe_counts.nlargest(20)
    # convert to list
    top20_mentions_list = top20_mentions.tolist()
    # create list of indices and top20 mentions
    top20_mentions_final = list(zip(top20_mentions.index, top20_mentions_list))
    
    # define the plot
    labels, y = zip(*top20_mentions_final)
    x = np.arange(len(labels))
    y_ticks = list(range(0,100,10))
    # plot into bar chart
    plt.xticks(x, labels, rotation=75)
    plt.yticks(y_ticks)    
    # add axes labels
    plt.xlabel("Geopolitical entities")
    plt.ylabel("Frequency")
    # add title
    plt.title("Top 20 geopolitical entities")
    # plot as bar chart
    plt.bar(x, y, color = "red", width = 0.8)
    # define outpath
    outpath = os.path.join("out")
    # save figure
    plt.savefig(os.path.join(outpath, name))
    
def parse_args():
    # initialize argparse
    ap = argparse.ArgumentParser()
    # add command line parameters 
    ap.add_argument("-f", "--file", required=True, help="The file to use")
    # pasrse arguments from the command line 
    args = vars(ap.parse_args())
    # return list og arguments
    return args

# let's get the code to run!
def main():
    args = parse_args()
    nlp, real_data, fake_data = load_process_data(args["file"])
    print("creating real news output")
    real_ents = find_entities(nlp, real_data)
    real_sents = find_sents(nlp, real_data)
    real_output = create_output(real_data, real_ents, real_sents)
    real_dataframe = save_csv(real_output, "real_news_sentiment_analysis.csv")
    top20(real_dataframe, "real_news_top20_gpe.jpg")
    print("creating fake news output")
    fake_ents = find_entities(nlp, fake_data)
    fake_sents = find_sents(nlp, fake_data)
    fake_output = create_output(fake_data, fake_ents, fake_sents)
    fake_dataframe = save_csv(fake_output, "fake_news_sentiment_analysis.csv")
    top20(fake_dataframe, "fake_news_top20_gpe.jpg")

if __name__ == "__main__":
    main()
    
    
