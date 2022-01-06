#!/usr/bin/env python
# coding: utf-8

# # Datentypen
# 
# ## Zeichenketten / Strings

# In[1]:


print("Hallo Welt!")


# ## Konkatenieren

# In[2]:


print("Hallo " + "Welt!")

print("Digital History Tagung " + "2021")

print("foo" * 2 + "bar " * 3)


# ## Variablen

# In[3]:


event = "Digital History Tagung"
year = 2021


# ## f-Strings

# In[4]:


print(f"Die {event} findet {year} statt.")

print("Die {} findet {} statt.".format(event, year))


# ## Funktionen und Methoden bei Strings

# In[5]:


print(len(event))

print(len("Digital History Tagung"))

print(event.lower())

print("Digital History Tagung".upper())


# ## Listen / Lists

# In[6]:


list_1 = [1, 2, 3, 4]

list_2 = ["Banane", "Apfel", "Birne"]

list_3 = [17, "Obst", 23, "Ball"]

list_4 = [[1, 2, 3,], ["a", "b", "c"], ["Hallo", "Welt"]]


# ## Zuordnungen / Dictionaries

# In[7]:


dict_1 = {"Banane": 5, 
          "Apfel": 7, 
          "Birne": 9}

dict_2 = {"Vorname": "Monty", 
          "Nachname": "Python", 
          "Alter": 48}


# ## Mengen / Sets

# In[8]:


menge = {1, 2, 2, 3, 3, 3, 4, 4, 5, 5, 5}

print(menge)

type(menge)


# ## Tuple

# In[9]:


word_freq = ("Wort A", 42)

type(word_freq)


# ## Indexieren von Strings

# In[10]:


print("Digital History Tagung"[1])

print("Digital History Tagung"[0])

print("Digital History Tagung"[8])


# ## Slicing

# In[11]:


print("Digital History Tagung"[0:10])

print("Digital History Tagung"[3:6])


# ## Indexieren von Listen

# In[12]:


list_2 = ["Banane", "Apfel", "Birne"]

print(list_2[2])

print(list_2[0])


# ## Funktionen und Methoden bei Listen

# In[13]:


print(len(list_2))

list_2.append("Ananas")

list_2.pop(1)


# ## Zugriff auf Dictionaries

# In[14]:


dict_1 = {"Banane": 5, "Apfel": 7, "Birne": 9}

print(dict_1["Banane"])

print(dict_1.keys())

print(dict_1.values())

print(sum(dict_1.values()))


# ## Logische Ausdrücke

# In[15]:


print(5 > 3)

print(5 > 7)

print("Mauer" == "Haus")

print("Mauer" != "Haus")


# ## Logische Ausdrücke: and, or

# In[16]:


print(5 > 3 and "Mauer" != "Haus")

print(5 > 3 and "Mauer" == "Haus")

print(5 > 3 or "Mauer" == "Haus")

print(5 > 7 or "Mauer" == "Haus")


# ## User-Input Skript

# In[17]:


# Eingabe Name
name = input("Wie heißt du? >>>")

# Eingabe Alter
alter = input("Wie alt bist du? >>>")

# Eingabe Wohnort
ort = input("Wo wohnst du? >>>")

jahr = 2021 - int(alter)

# Ausgabe
print(f"""
\nHallo {name}, schön, dass du da bist!\n
Du bist {jahr} geboren.\n
{ort} ist der beste Ort auf dem Planeten.""")

