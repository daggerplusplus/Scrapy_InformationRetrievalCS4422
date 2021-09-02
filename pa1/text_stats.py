import sys
import json
import nltk
from collections import Counter
from nltk import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
import matplotlib.pyplot as plt


#pass file name by argument to this script
file = sys.argv[1]  
with open(file,"r") as read_file:
  data = json.load(read_file)

body_data = []
for item in data:
  body_data.append(item['body'])
body_data = [[string.lower() for string in sublist] for sublist in body_data]

#Vocabulary
flattened = []
Vocab = []
#add words to list
for sublist in body_data:
  for val in sublist:
    flattened.append(val)
#add words not in list
for item in flattened:
  if not item in Vocab:
    Vocab.append(item)
tokens=[word_tokenize(data) for data in flattened]    #tokenize body text
num_tokens = len(tokens)
counts = [[len(word) for word in sublist] for sublist in tokens]
flatcount = []
for sublist in counts:  #flattened counts
  for val in sublist:
    flatcount.append(val)
avgtokensperpage = (sum([len(i) for i in tokens])/ num_tokens)
doc_len = sum(flatcount)/ avgtokensperpage


email_data = []
for item in data:
  email_data.append(item['emails'])
email_perc = email_data                     #copy of email_data with empty elements for % calcs
email_data = list(filter(None,email_data))  #remove empty elements from list
email_counter = Counter(tuple(item) if type(item) is list else item for item in email_data)
freq = email_counter.most_common(10)              #count frequency of items in series
empty_emails = email_perc.count([])         #count pages without emails
perc = ((empty_emails) / (len(email_perc))) * 100 #calc % of pages crawled with at least one email

#Vocabulary
flattened = []
Vocab = []
#add words to list
for sublist in tokens:
  for val in sublist:
    flattened.append(val)
#add words not in list
for item in flattened:
  if not item in Vocab:
    Vocab.append(item)





print('doc_len: {:.2f}'.format(doc_len))
print('emails:\n')
print(*freq,sep='\n')
print('\n')
print('perc: {:.2f}'.format(perc))
print('\n\n')


top30_withstops = Counter(flattened).most_common(30)
ranking = {pair[0]: rank
  for rank,pair in enumerate(top30_withstops)}
print('Top 30 most common words BEFORE removing stopwords:')
rank = 1
print('Rank\tTerm\tFreq')
print('---------------------')
for item in top30_withstops:
  print(rank,item)
  rank += 1
print('\n')

filteredA = []
filteredB = []
stop_words = set(stopwords.words('english'))
punctuations = '!()-[]{};:\'"\\,<>./?@#$%^&*_~’'
for w in flattened:
  if w not in stop_words:
    filteredA.append(w)

for char in filteredA:
  if char not in punctuations:
    filteredB.append(char)
top30_filtered = Counter(filteredB).most_common(30)
print('Top 30 most common words AFTER removing stopwords:')
rank = 1
print('Rank\tTerm\tFreq')
print('---------------------')
for item in top30_filtered:
  print(rank,item)
  rank += 1
print('\n')


fd = nltk.FreqDist(flattened)
fd.plot(30,cumulative=False)

a = dict(Counter(flattened).most_common(30))
y = a.values()
x = list(range(1,31))
df = pd.DataFrame({'x':x,'y':y})
plt.loglog(x,y)
plt.show()
#plt.savefig("loglog.png")   #save output to main folder