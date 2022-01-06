#!/usr/bin/env python
# coding: utf-8

# # Titel ist hier zu finden!

# In[1]:


from bokeh.plotting import figure, show, output_notebook
from bokeh.sampledata.iris import flowers
from bokeh.transform import factor_cmap, factor_mark
output_notebook()


# In[2]:


p = figure()
p.circle(flowers["sepal_width"], flowers["sepal_length"], fill_color=flowers["species"], size=flowers["sepal_length"])
show(p)


# In[ ]:




