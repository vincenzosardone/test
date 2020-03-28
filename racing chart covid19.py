#!/usr/bin/env python
# coding: utf-8

# ### Importo le librerie

# In[1]:


import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from IPython.display import HTML


# ### Importo il file dei dati da github e guardo le prime righe
# 

# In[2]:


url = 'https://raw.githubusercontent.com/vincenzosardone/test/master/covid_data.csv'
df = pd.read_csv(url)
df.head(5)


# ### Ri-arrangio i dati in modo tale che per ogni data scelta si abbiamo le nazioni ordinate in modo decrescente per il numero totale di casi

# In[3]:


current_day = '27-03-20'
dff = df[df['date'].eq(current_day)].sort_values(by='cases', ascending=False).head(10)
dff


# ### Primo plot
# 
# --------------------------
# Top 10

# In[4]:


fig, ax = plt.subplots(figsize=(15, 8))
ax.barh(dff['state'], dff['cases'])


# ### Le nazioni sono raggruppate per macro-regioni, assegno ad ognuna di esse un colore

# In[5]:


colors = dict(zip(
    ["Americas","Europe","Asia","Africa","Oceania"],
    ["#adb0ff", "#e48381", "#90d595", "#f7bb5f", "#aafbff"]
))
group_region = df.set_index('state')['region'].to_dict()


# ### Rifaccio il plot includendo colori, alcuni orpelli puramente visivi e riordino le barre dal valore maggiore al minore

# In[6]:


fig, ax = plt.subplots(figsize=(15, 8))
dff = dff[::-1]
ax.barh(dff['state'], dff['cases'], color=[colors[group_region[x]] for x in dff['state']])
for i, (cases, state) in enumerate(zip(dff['cases'], dff['state'])):
    ax.text(cases, i,     state,            ha='right')
    ax.text(cases, i-.25, group_region[state],  ha='right')
    ax.text(cases, i,     cases, ha='left')
ax.text(1, 0.4, current_day, transform=ax.transAxes, size=46, ha='right')


# ### Ri-rifaccio il plot con ancor piu' inutili orpelli stilistici

# In[7]:


fig, ax = plt.subplots(figsize=(15, 8))

def draw_barchart(current_day):
    dff = df[df['date'].eq(current_day)].sort_values(by='cases', ascending=True).tail(10)
    ax.clear()
    ax.barh(dff['state'], dff['cases'], color=[colors[group_region[x]] for x in dff['state']])
    dx = dff['cases'].max() / 200
    for i, (cases, state) in enumerate(zip(dff['cases'], dff['state'])):
        ax.text(cases-dx, i,     state,           size=14, weight=600, ha='right', va='bottom')
        ax.text(cases-dx, i-.25, group_region[state], size=10, color='#444444', ha='right', va='baseline')
        ax.text(cases+dx, i,     f'{cases:,.0f}',  size=14, ha='left',  va='center')
    ax.text(1, 0.4, current_day, transform=ax.transAxes, color='#777777', size=46, ha='right', weight=800)
    ax.text(0, 1.06, 'By country', transform=ax.transAxes, size=18, color='#777777')
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#777777', labelsize=12)
    ax.set_yticks([])
    ax.margins(0, 0.01)
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    ax.text(0, 1.15, 'Total cases of COVID-19 from 22-Jan to the 27-Mar',
            transform=ax.transAxes, size=24, weight=600, ha='left', va='top')
    ax.text(1, 0, 'by @Vincenzo Sardone', transform=ax.transAxes, size=15, weight=500, color='#777777', ha='right',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))
    plt.box(False)
    
draw_barchart('27-03-20')


# ### Trasformo la colonna del data frame "date" in un lista di valori univoci, in questo modo posso usarla per definire i vari frame da mostrare nella animazione del plot

# In[8]:


date_df = pd.read_csv(url,usecols=['date'])
date_df.head(10)


# In[9]:


date_df['date'].unique()


# In[10]:


date_list = pd.unique(date_df['date']).tolist()


# In[11]:


date_list


# ### Rendo il grafico animato

# In[15]:


animator = animation.FuncAnimation(fig, draw_barchart, frames=date_list, interval=600)
HTML(animator.to_jshtml())


# In[ ]:




