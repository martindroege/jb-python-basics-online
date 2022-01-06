#!/usr/bin/env python
# coding: utf-8

# # Funktionen Textprocessing
# 
# ## Text-Datei runterladen

# In[1]:


import requests

gg_raw_url = "https://raw.githubusercontent.com/levinalex/deutsche_verfassungen/master/grundgesetz/grundgesetz.txt"
response = requests.get(gg_raw_url)
grundgesetz = response.text

grundgesetz[:1000]


# ## Text-Datei speichern

# In[2]:


with open('grundgesetz.txt', 'w', encoding='utf-8') as f:
    f.write(grundgesetz)


# ## Kleinschreibung vereinheitlichen

# In[3]:


grundgesetz = grundgesetz.lower()
print(grundgesetz[:250])


# ## Zeichensetzung entfernen

# In[4]:


import string

def remove_punctuation(text):
    punctuation = string.punctuation
    for marker in punctuation:
        text = text.replace(marker, "")
    return text

grundgesetz = remove_punctuation(grundgesetz)
print(grundgesetz[:250])


# ## Liste erstellen

# In[5]:


grundgesetz_words = grundgesetz.split()


# In[6]:


print("Anzahl aller Worte des Textes: ")
print(len(grundgesetz_words))
print("=======")
print(grundgesetz_words[:25])


# ## Zählen eines bestimmten Worts

# In[7]:


def count_item_in_text(item_to_count, list_to_search):
    number_of_hits = 0
    for item in list_to_search:
        if item == item_to_count:
            number_of_hits += 1
    return number_of_hits


# In[8]:


print(count_item_in_text("bund", grundgesetz_words))


# ## Alle Wörter zählen mit Hilfe eines Dictionarys

# In[9]:


def counter_dict(list_to_search):
    counts = {}
    for word in list_to_search:
        if word in counts:
            counts[word] = counts[word] + 1  
        else:
            counts[word] = 1
    return counts


# In[10]:


counter_dict(grundgesetz_words)


# ## Worthäufigkeiten sortieren

# In[11]:


def freq_sort(list_to_search):
    counts = counter_dict(list_to_search)
    counts = [(counts[key], key) for key in counts]
    counts.sort()
    counts.reverse()
    return counts


# In[12]:


freq_sort(grundgesetz_words)[:25]


# ## Entfernen von Stoppwörtern

# In[13]:


def remove_stopwords(list_to_search):
    stopword_url = "http://members.unine.ch/jacques.savoy/clef/germanST.txt"
    response = requests.get(stopword_url)
    stopwords = response.text
    stopwords = stopwords.split()
    return [w for w in list_to_search if w not in stopwords]


# In[14]:


remove_stopwords(grundgesetz_words)[:25]


# ## Entfernen von Zahlen mit regulärem Ausdruck

# In[15]:


import re

RE_INT = re.compile(r'\d+')

def remove_digit(text):
    return re.sub(RE_INT, '', text)


# ## Funktionsaufrufe

# In[16]:


grundgesetz = grundgesetz.lower()
grundgesetz = remove_punctuation(grundgesetz)
grundgesetz = remove_digit(grundgesetz)
grundgesetz_words = grundgesetz.split()
grundgesetz_words = remove_stopwords(grundgesetz_words)
freq_sort(grundgesetz_words)[:25]

