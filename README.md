## 1. Assignment 2 - Sentiment and NER
Link to repository: https://github.com/MetteHejberg/Lang_assignment2

For this assignment, you will write a small Python program to perform NER and sentiment analysis using the techniques you saw in class. You have the choice of one of two different tasks:

2. Using the corpus of Fake vs Real news, write some code which does the following
- Split the data into two datasets - one of Fake news and one of Real news
- For every headline
   - Get the sentiment scores
   - Find all mentions of geopolitical entites
   - Save a CSV which shows the text ID, the sentiment scores, and column showing all GPEs in that text
- Find the 20 most common geopolitical entities mentioned across each dataset - plot the results as a bar charts
  
## 2. Methods
This assigment uses ```SpaCy TextBlob``` to perform sentiment analysis on real and fake news titles. Sentiment analysis is analyses computationally the underlying negative or positive feelings in a text. In this assignment, I use a dictionary approach with ```SpaCy TextBlob``` which assigns three different types of sentiment scores. One is polarity, positive vs. negative, ranging from -1 (very negative) to 1 (very positive). The second is subjectivity, objective vs. subjective, ranging from 0 (very objective) to 1 (very subjective). The last one is intensity, which looks at how the word modifies the following word. It ranges from x0.5 to x2. These scores are then summed up and averaged to give an overall sentiment score of the text.

This script explores the sentiments towards mentions of GPEs, which are geopolitical entities such as countries. The data is firstly split into real and fake headlines. The script then uses ```spacy``` to tokenize the text, get the GPEs mentions and sentiments of the entire headline. Then it creates a dataframe with ```pandas``` with the text IDs, GPEs, sentiments, and headlines which is then saved to ```out```

The script furthermore finds the 20 most common GPE mentions for both the real and fake data and plots them as bar charts with ```package```. 

Get the data from here:

## 3. Usage ```real_or_fake.py```
To run the code you should:
- Pull this repository with this folder structure
- Place the data in ```in```
- Install the packages mentioned in ```requirements.txt```
- Set your current working directory to the level above ```src```
- Write in the command line: ```python src/real_or_fake.py```
   - You can see the outputs of the code in ```out```

## 4. Discussion of Results
Since the dataset is so large, it is difficult to get an idea of how the sentiment scores are distributed across the real and fake headlines. However, there are issues with the dictionary approach that prevail regardless of whether the headline is real or fake. Usually, dictionaries are at least partly created with human annotators, which always introduces biases. Furthermore, computational linguistics in general and sentiment analysis specifically face the issue that the data is often taken out of context and therefore heavily reduced. This means that sarcasm and irony is very difficult to capture, which brings the generalizability of the method and results into question. Furthermore, the way the text is tokenized results in "USA" and "US" being two different GPEs. This is also visible in the figures where the US is referred to as "US", "America", "U.S.". This is of course not ideal, and would be something you could seek to improve in the code. 
