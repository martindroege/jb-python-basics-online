#!/usr/bin/env python
# coding: utf-8

# # Interaktive Visualisierung der Wutbürger-Tweets mit Bokeh, 19.12.21
# 
# * Grundlage ist das Datenset #wutbuerger.json gescrappt über
#     * Twitter-API Academic Research; endpoint search all
#     * Twarc2
#     * Grundlage dazu weitere Test-Notebooks
# 
#     
# * Optimierungen im Layout sind ggf. noch möglich / nötig
#     * Farben der Marker
#     * Ticks der Spines
#     * Hintergrundfarbe
#     * Farben und Styling der Hoverox
#     * u.a.
# 

# In[1]:


import pandas as pd
import numpy as np
import pytz

from bokeh.plotting import figure, output_file, output_notebook, show
from bokeh.models import ColumnDataSource, CDSView, Legend 
from bokeh.models import CustomJS, Slider, OpenURL, TapTool, CustomJSFilter
from bokeh.models import DatetimeTickFormatter
from bokeh.models.tools import HoverTool, BoxZoomTool, ResetTool, PanTool
from bokeh.layouts import column, row 
from bokeh.io import show 

output_notebook()


# In[2]:


# read data

df = pd.read_csv('../data/211219-wutbürger-preprocessed.csv', 
                 parse_dates=['date'])


# In[3]:


df.info()


# In[4]:


# data wrangling and create new columns

# hours_minutes stellt die x-Achse dar
df.loc[:, 'hours_minutes'] = ((df.loc[:, 'date'].dt.hour * 60) + df.loc[:, 'date'].dt.minute) / 60

# tweet_score zeigt die Größe der Marker an
df.loc[:, 'tweet_score'] = 5 + ((df.loc[:, 'nlikes']) + (df.loc[:, 'nretweets'] * 2) + (df.loc[:, 'nreplies'] * 3)) / 100

# convert time zone: funktioniert nicht wie erwartet >  Berlin is UTC + 1 (Summertime +2)
# alle Datumsangaben sind (bei der V1-Visu) 2 Stunden früher > 2 Stunden dazu addiert
df.loc[:, 'date'] = df.loc[:, 'date'].dt.tz_convert(pytz.timezone('Europe/Berlin'))
df.loc[:, 'date'] = df.loc[:, 'date'] + pd.Timedelta(hours=2)

df = df.drop(['nqoutes'], axis=1)


# In[5]:


# Die Funktion setzt in jeden Tweets an jeder 8. Indexstelle den html-Tag <br>
# Damit wird bei der Hoverbox ein Zeilenumbruch erzeugt, um den Text lesbar zu machen.

def insert_br(text):
    '''
    function inserts <br> every 8th word
    to create custom tooltip with html
    '''  
    
    text = text.split(' ')
    for i in range(len(text) // 8):
    
        text.insert((i+1) * 8, '<br>')
    
    return ' '.join(text)


# In[6]:


# creat new column

df.loc[:, 'tweet_br'] = df.loc[:, 'tweet'].apply(lambda x: insert_br(x))


# In[7]:


# create diskurse

# Hier werden die Diskurse erstellt mittels Tuples von 3 Elementen erstellt:
# Index 0: Label des Diskurses
# Index 1: Farbe des Diskurses
# Index 2: Liste von Schlüsselworten, die zu dem Diskurs gehören

s21_diskurs = ('S21', 'red',  ['s21', 'stuttgart', 'stuttgart21', 'stuttgarter', 'brandschutz'])

afd_diskurs = ('AfD / Pegida', 'green', ['afd', 'pegida', 'noafd', 'nopegida', 'nazis', 'nazi', 'nonazis', 'lügenpresse', 'fckafd'])

corona_diskurs = ('Corona', 'orange', ['coronaleugner', 'covidioten', 'covidiot', 'corona', 'covid19', 'coronavirus', 'coronademo', 'infektion', 'maske', 'maskenverweigerer'                   'cov19unvereinbar', 'lockdown', 'impfgegner', 'maskenpflicht', 'drosten', 'pandemie', 'virus', 'coronakrise'])

mutbürger_diskurs = ('Mutbürger', 'darkturquoise', ['mutbürger'])

hutbürger_diskurs = ('Hutbürger', 'greenyellow', ['hutbürger'])

querdenker_diskurs = ('Querdenker', 'hotpink', ['querdenker', 'querdenken', 'verschwörungstheoretiker']) # verschwörungstheoretiker ist vllt. eigener Diskurs

diskurs_liste = [s21_diskurs, afd_diskurs, corona_diskurs, mutbürger_diskurs, hutbürger_diskurs, querdenker_diskurs, ('keine Zuordnung', '#1da1f2') ]


# color_list = ['red', 'green', 'orange', '#1da1f2']
# https://docs.bokeh.org/en/latest/docs/reference/colors.html


# In[8]:


# Die Funktion erstellt eine Spalte für den jeweiligen Diskurs
# Die Liste der Hashtags wird in der List-Comprehension geprüft, ob darin Schlüsselwörter des entsprechenden Diskurses enhalten ist
# Wenn das so ist, wird in der Spalte für den Diskurs das Label des Diskurses eingetragen, falls nicht wird np.nan eingetragen
# Vorteil von jeweils einer eigenen Spalte pro Diskurs: Überschneidungen von Diskurses können visuell erfasst werden

def diskurs_maker(hashtaglist, diskurstuple):
    '''
    checks if hashtaglist contains hastag that ist in list of Diskurs.
    '''

    if any(item in hashtaglist for item in diskurstuple[2]):
        return diskurstuple[0]
       
    else:
        return np.nan


# In[9]:


# Die for-Schleife erstellt die Spalten mit den Diskursen

for diskurs in diskurs_liste[:-1]:
    df.loc[:, diskurs[0]] = df.loc[:, 'hashtags'].apply(lambda x: diskurs_maker(x, diskurs))


# In[10]:


# Die Lambda-Funkton prüft, ob es so viele NaNs in einer Reihe wie Diskurse gibt, 
# also prüft, ob ein Tweet zu keinem der Diskurse gepasst hat: 
# dann wird keine Zuordnung gesagt
# Die Zahl der Diskurse wird aus mit len(Diskursliste - 1) errechnet
# Das letzte Element der Diskurslist ist das Tuple für die Farbzuordnung der nicht zugeordneten Tweets

df.loc[:, 'keine Zuordnung'] = df.isna().sum(axis=1).apply(lambda x: 'keine Zuordnung' if x == len(diskurs_liste) - 1 else np.nan )


# In[11]:


# Die for-Schleife erstellt auf Basis der Datenspalte die sources für die Bokeh-Figure
# Dazu wird für jede Diskursspalte mit einer Boolschen Maske geprüft, ob das Diskurs-Label in der Spalte enthalten ist
# Dann wird mit ColumnDataSource der gefilterte Dataframe in source umgewandelt und der source_list angefügt.

source_list = []

for diskurs in diskurs_liste:
    
    source = df.loc[df.loc[:, diskurs[0]] == diskurs[0], :]    
    source_list.append(ColumnDataSource(source))


# In[12]:


# create sliders

# In dieser Zellen werden die Slider für Retweets, Likes, Replies und Textlänger erstellt
# Wichtig ist, das der javascript Code für jeden Slider, jede source für die Diskurse mit
# sourceX.change.emit() aktiviert, sonst passiert bei den Slidern nichts.
# Ebenso muss bei den Args alle Sources übergeben werden.
# Die init_values sind die min bzw. max Werte der jeweiligen Datenspalte; 
# diese werden für die 'Begrenzung' des Slider-Raumes genutzt und für den Start-Value des Sliders genutzt

# >>> javascript code ist nötig, damit die erstellte html-Datei auch als Standalone funktioniert!

# javascript code
js_code = """
   source0.change.emit();
   source1.change.emit();
   source2.change.emit();
   source3.change.emit();
   source4.change.emit();
   source5.change.emit();
   source6.change.emit();
"""

# source dict
source_dict = dict(source0=source_list[0], 
                     source1=source_list[1], 
                     source2=source_list[2],
                     source3=source_list[3],
                     source4=source_list[4],
                     source5=source_list[5],
                     source6=source_list[6])

# Refactor > create for-loop

# Slider für Anzeige der Retweets
init_value_rt = (df.loc[:, 'nretweets'].min(), df.loc[:,'nretweets'].max())

rt_slider = Slider(start=init_value_rt[0], value=0, end=100, step=1, title='Anzahl der Retweets (zw. 0 und 100 einstellbar)')
rt_slider.js_on_change('value', CustomJS(args=source_dict, code=js_code))

# Slider für Anzeige der Likes
init_value_li = (df.loc[:, 'nlikes'].min(), df.loc[:,'nlikes'].max())

li_slider = Slider(start=init_value_li[0], value=0, end=100, step=1, title='Anzahl der Likes (zw. 0 und 100 einstellbar)')
li_slider.js_on_change('value', CustomJS(args=source_dict, code=js_code))

# Slider für Anzeige der Replies
init_value_li = (df.loc[:, 'nreplies'].min(), df.loc[:,'nreplies'].max())

re_slider = Slider(start=init_value_li[0], value=0, end=100, step=1, title='Anzahl der Antworten (zw. 0 und 100 einstellbar)')
re_slider.js_on_change('value', CustomJS(args=source_dict, code=js_code))

# Slider für Anzeige der Tweetlänge
init_value_tl = (df.loc[:, 'char_per_url_free_tweet'].min(), df.loc[:,'char_per_url_free_tweet'].max())

tl_slider = Slider(start=init_value_tl[0], value=0, end=init_value_tl[1], step=1, title='Länge der Tweets')
tl_slider.js_on_change('value', CustomJS(args=source_dict, code=js_code))

# TODO: Try RangeSlider for Tweetlänge


# In[13]:


# create figure, custom_filters and views

# Zunächst wird die figure mit den Maßen, Größenanpassung und Toolbar instantiiert.

p = figure(height=875, 
           width=875,
           sizing_mode="stretch_both", # vergrößert die figure auf die Breite des Browsers
           toolbar_location="above", 
           tools= ['pan', 'wheel_zoom', 'box_zoom', 'save', 'reset', 'tap'])

view_list = []
custom_filter_list = []

# für jede source wird ein Customfilter angelegt
# im javascript code werden alle Slider-Einstellungen verarbeitet
# nur die Indices, die zu den Slider-Einstellungen passen, werden zurückgegeben
# der Customfilter wird der custom_filter_list beigefügt

for source in source_list:

    custom_filter = CustomJSFilter(args=dict(rt_slider=rt_slider, li_slider=li_slider, re_slider=re_slider, tl_slider=tl_slider), code='''
        var indices = [];
        for (var i = 0; i < source.get_length(); i++){
            if (source.data['nretweets'][i] >= rt_slider.value && source.data['nlikes'][i] >= li_slider.value && source.data['nreplies'][i] >= re_slider.value && source.data['char_per_url_free_tweet'][i] >= tl_slider.value){
                indices.push(true);
            } else {
                indices.push(false);}}
        return indices; 
        ''')

    custom_filter_list.append(custom_filter)

# für jeden Source wird eine View erstellt
# bei den filters wird die gesamte custom_filter_list übergeben

for source in source_list:
    view = CDSView(source=source, filters=custom_filter_list)  
    view_list.append(view)
    
# aus den Listen werden die Grafiken erstellt und in eine figure gepackt

for source, diskurs, view in zip(source_list, diskurs_liste, view_list):

    p.circle(x='hours_minutes', y='date', color=diskurs[1], fill_alpha=0.5, size='tweet_score', legend_label=diskurs[0], source=source, view=view) 


# In[14]:


# Taptool: Durch einen click auf den Marker wird der Link zum Tweet aus der link-Spalte abgerufen:
# In einem neuen Browser Fenster öffnet sich der Tweet

taptool = p.select(type=TapTool)
taptool.callback = OpenURL(url='@link')


# In[15]:


# add hover 

hover = HoverTool(tooltips=[('Datum', '@date{%F %H:%M}'), 
                            ('Tweet', '<span style="font-size: 17px; font-weight: bold; width=42">@tweet_br{safe}</span>'),
                            ('von', '@username'),
                            ('Retweets', '@nretweets'),
                            ('Likes', '@nlikes'),
                            ('Replies', '@nreplies'),
                            ('Tweet-Score', '@tweet_score'),
                            ], 
                  formatters={'@date': 'datetime'})

p.add_tools(hover)


# In[16]:


# Layout styling der figure
# interactive legend outside the plot and other layout featurs

p.y_range.flipped = True
p.yaxis.formatter=DatetimeTickFormatter()

p.legend.location = 'top_left'
p.legend.click_policy='hide'
p.legend.title = 'Diskurse\n (click to hide)'
p.legend.title_text_font_style = 'normal'

p.title.text = 'Wutbürger Tweets'
p.xaxis.axis_label = 'Uhrzeit'
p.yaxis.axis_label = 'Datum'

p.add_layout(p.legend[0], 'left')

# change just some things about the x-grid
p.xgrid.grid_line_color = None

# change just some things about the y-grid
p.ygrid.band_fill_alpha = 0.1
p.ygrid.band_fill_color = "grey"


# In[17]:


# output to standalone HTML file
# output_file('211219-Wutbüger_interaktiv.html')


# In[18]:


# Anordnung des Layouts von Slidern und figure
layout = row(column(rt_slider, li_slider, re_slider, tl_slider), p)

show(layout)


# In[ ]:





# In[ ]:




