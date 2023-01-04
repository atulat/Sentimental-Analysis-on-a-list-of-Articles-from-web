# Sentimental Analysis on a list of Articles from the webpage
The Motive of the Project is to extract textual data articles from the given URL and perform text analysis.

For each of the articles, given in the input.xlsx file, We extract only the article title and the article text, not the website header, footer, or anything other than the article text.
For this, we have used the BeautifulSoup Package for Web Scraping.

For each of the extracted texts from the article, we perform textual analysis and compute variables and save the output in the Output.xlsx

The Stop Words Lists (found in the folder StopWords) are used to clean the text so that Sentiment Analysis can be performed by excluding the words found in Stop Words List.

The Master Dictionary is used for creating a dictionary of Positive and Negative words. We add only those words in the dictionary if they are not found in the Stop Words Lists.

We convert the text into a list of tokens using the nltk tokenize module and use these tokens to calculate Positive Score, Negative Score, Polarity Score, Subjectivity Score.

Positive Score: This score is calculated by assigning the value of +1 for each word if found in the Positive Dictionary and then adding up all the values

Negative Score: This score is calculated by assigning the value of -1 for each word if found in the Negative Dictionary and then adding up all the values. We multiply the score with -1 so that the score is a positive number.

Polarity Score: This is the score that determines if a given text is positive or negative in nature. It is calculated by using the formula:
Polarity Score = (Positive Score – Negative Score)/ ((Positive Score + Negative Score) + 0.000001)
Range is from -1 to +1

Subjectivity Score: This is the score that determines if a given text is objective or subjective. It is calculated by using the formula: 
Subjectivity Score = (Positive Score + Negative Score)/ ((Total Words after cleaning) + 0.000001)
Range is from 0 to +1

Analysis of Readability is calculated using the Gunning Fox index

Average Sentence Length = the number of words / the number of sentences

Percentage of Complex words = the number of complex words / the number of words 

Fog Index = 0.4 * (Average Sentence Length + Percentage of Complex words)

Average Number of Words Per Sentence = the total number of words / the total number of sentences

Complex words: words that contain more than two syllables.

We count the number of Syllables in each word of the text by counting the vowels present in each word. We also handle some exceptions like words ending with "es","ed" by not counting them as a syllable.

To calculate Personal Pronouns mentioned in the text, we use regex to find the counts of the words - “I,” “we,” “my,” “ours,” and “us”. Special care is taken so that the country name US is not included in the list.

Average Word Length = Sum of the total number of characters in each word / Total number of words
