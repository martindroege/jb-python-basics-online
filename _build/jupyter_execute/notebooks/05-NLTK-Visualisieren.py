#!/usr/bin/env python
# coding: utf-8

# # NLTK und Worthäufigkeiten visualisieren
# 
# ## collections

# In[1]:


from collections import Counter

freq = Counter(grundgesetz_words)


# In[ ]:


type(freq)


# In[ ]:


freq.most_common(25)


# ## NLTK

# In[ ]:


import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')

with open('grundgesetz.txt', 'r', encoding='utf-8') as infile:
    text_raw = infile.read()

text = text_raw.lower()
text = word_tokenize(text)
text = nltk.Text(text) 


# ## concordance

# In[ ]:


text.concordance("bund", width=110)


# ## similar

# In[ ]:


text.similar("freiheit")


# ## dispersion plot

# In[ ]:


text.dispersion_plot(["artikel", "gesetz", "freiheit", 'bundespräsident', 'bundeskanzler'])


# In[ ]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# In[ ]:


df = pd.DataFrame(freq.items(), columns=['word', 'count'])
df = df.sort_values(by='count', ascending=False)
df_top_25 = df.head(25)


# In[ ]:


fig, ax = plt.subplots(figsize=(12,8))

sns.barplot(x='word', y='count', data=df_top_25, ax=ax)
ax.set_xticklabels(labels=df_top_25.loc[:, 'word'], rotation=45, ha='right');

