# -*- coding: utf-8 -*-
"""ChatBot.ipynb
#This bot will take data from mayoclinic and try to give information on Chronic Kidney Disease
"""

pip install nltk

pip install newspaper3k

#Libraries
from newspaper import Article
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
warnings.filterwarnings('ignore')

#Use opensource NLP PUNKT
nltk.download('punkt',quiet=True)

#Using mayoclinic data 
article = Article('https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521')
article.download()
article.parse()
article.nlp()
corpus = article.text

print(corpus)

#Tokenization
text = corpus
sentence_list = nltk.sent_tokenize(text) #Array of sentences

print(sentence_list)

#Create greet function
def greeting_response(text):
  text = text.lower()
  bot_greetings = ['howdy', 'hi', 'hey', 'hello', 'kidha', 'namaste']
  user_greetings = ['hi','hey','hello','greetings','sup','yo','test','']

  #is user inputs greeting, return random greeting
  for word in text.split():
    if word in user_greetings:
      return random.choice(bot_greetings)

def index_sort(list_var):
  length = len(list_var)
  list_index = list(range(0,length))

  x = list_var

  for i in range(length):
    for j in range(length):
      if x[list_index[i]] > x[list_index[j]]:
        #swap
        temp = list_index[i]
        list_index[i] = list_index[j]
        list_index[j] = temp

  return list_index

#creating bots response
def bot_responseTEST(user_input):
  user_input = user_input.lower()
  sentence_list.append(user_input)
  bot_response = '' #null initial value
  cm = CountVectorizer().fit_transform(sentence_list) #get count matrix from sentence list
  similarity_scores = cosine_similarity(cm[-1],cm) #get last sentence of cm, which is user input, and compare to all of cm, which is our parsed data
  similarity_scores_list = similarity_scores.flatten() #reduce the dimensionality of the similarity scores (reduce input variables)
  
  #find index of highest score
  index = index_sort(similarity_scores_list) #go from highest to lowest values of similarity scores and find highest value place at the lowest index

#testing bot_response
#user_input = 'i have stomach pains'
#sentence_list.append(user_input)
#bot_response = '' #null initial value
#cm = CountVectorizer().fit_transform(sentence_list) #get count matrix from sentence list
#similarity_scores = cosine_similarity(cm[-1],cm) #get last sentence of cm, which is user input, and compare to all of cm, which is our parsed data
#similarity_scores_list = similarity_scores.flatten() #reduce the dimensionality of the similarity scores (reduce input variables)
#sentence_list.remove(user_input)
#find index of highest score
#index = index_sort(similarity_scores_list) #go from highest to lowest values of similarity scores and find highest value place at the lowest index

def bot_response(user_input):
  user_input = user_input.lower()
  sentence_list.append(user_input)
  bot_response = '' #null initial value
  cm = CountVectorizer().fit_transform(sentence_list) #get count matrix from sentence list
  similarity_scores = cosine_similarity(cm[-1],cm) #get last sentence of cm, which is user input, and compare to all of cm, which is our parsed data
  similarity_scores_list = similarity_scores.flatten() #reduce the dimensionality of the similarity scores (reduce input variables)
  
  #find index of highest score
  index = index_sort(similarity_scores_list) #go from highest to lowest values of similarity scores and find highest value place at the lowest index

  #now we can get the highest valued similarity score
  index = index[1:] #contain only non highest elements
  response_flag = 0 #to check if there is a response to user

  j = 0
  for i in range(len(index)):
    if similarity_scores_list[index[i]] > 0: #if we find a match to our users input (anything over 0 on our similarity score list)
      bot_response = bot_response + ' ' + sentence_list[index[i]] #then assign bot response the corresponding highest similarity score sentence
      response_flag += 1 #update the flag to indicate there has been a sentence found
      j += 1 #lets us know how many possible matches we have (counting scores)
    if j > 2:
      break #if we get more than one corresponding sentence, lets break out of this loop since we already have the highest similarity score sentence selected.

  if response_flag == 0:
    bot_response += " Sorry, I couldn't find any information on that"
    
  sentence_list.remove(user_input) #remove the users input

  return bot_response

#Chat with bot
print('Hi, I am here to help you on your questions and concerns about Chronic Kidney Disease to the best of my ability. To exit, type \"bye\"')

exit_list = ['exit','see you later', 'bye', 'quit', 'break']
while(True):
  user_input = input()
  if user_input.lower() in exit_list:
    print('Hope I was able to help, bye!')
    break
  else:
    if greeting_response(user_input) != None:
      print(greeting_response(user_input))
    else:
      print(bot_response(user_input))

