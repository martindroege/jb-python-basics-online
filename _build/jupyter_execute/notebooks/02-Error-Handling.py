#!/usr/bin/env python
# coding: utf-8

# # error handling und Kontrollstrukturen

# ## Fehlerbehandlung / error handling

# In[1]:


print("Hallo Welt!"


# In[ ]:


for x in range(10)


# In[ ]:


for x in range(10):
print(x)


# ## help() Function

# In[ ]:


help(len)


# ## Kontrollstrukturen
# 
# ## For-Schleife

# In[ ]:


for x in range(10):
   print(x)


# ## While-Schleife

# In[ ]:


x = 10
while x > 0:
    print(x)
    x -= 1


# ## If-Anweisung

# In[ ]:


for x in range(1, 11):
    if x % 2 == 0:
        print(f"{x} ist eine gerade Zahl.")
    else:
        print(f"{x} ist eine ungerade Zahl.")


# ## Dateien lesen 1

# In[ ]:


f = open("DATEI.txt", "r", encoding="utf-8")
text = f.read()
f.close()


# ## Dateien lesen 2

# In[ ]:


with open("DATEI.txt", "r", encoding="utf-8") as f:
    text = f.read()


# ## I/O Parameter
# 
# * "r" = read / lesen
# * "w" = write / schreiben
# * "a" = append / anhängen

# ## Kommentar

# In[ ]:


# Dies ist ein Kommentar

