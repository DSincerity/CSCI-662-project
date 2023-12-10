#!/usr/bin/env python
# coding: utf-8

# In[30]:


### loading data
data_file = "/home/pdey3/blenderbot/_reformat/augesc/augesc.txt"


# In[31]:


data = open(data_file, "r")
data = data.readlines()


# In[32]:


data = [d[:-1] for d in data]


# In[33]:


### need to convert this so that it resembles KEMI data structure
#'dialog': [
        #{'text': 'Hi', 
        # 'speaker': 'usr' 
        #}, 
        #{'text': 'Hi, I am here to support you in anyway that I can how is your day going?', 
        #'speaker': 'sys', 
        #} 


# In[34]:


import ast


# In[35]:


ast.literal_eval(data[0])


# In[36]:


results = [] 
for d in data: 
    d = ast.literal_eval(d)
    reformed = [] 
    for utterance in d: 
        user = utterance[0]
        text = utterance[1]
        reformed.append({
            'text': text,
            'speaker': user
        })
    dict_ = {'dialog': reformed}
    results.append(dict_)


# In[37]:


results[0]


# In[23]:


pt_1 = int(0.1 * len(results))
len(results)


# In[27]:


train_examples = results[:int(8*pt_1)]
val_examples = results[int(8*pt_1)+1:]
len(val_examples)


# In[42]:


### write to files 
import json

train_file = open("augesc_train_small.txt", "w")
for t in train_examples[:10000]: 
    train_file.write(json.dumps(t) + "\n")
val_file = open("augesc_val_small.txt", "w")
for t in val_examples[:2000]: 
    val_file.write(json.dumps(t) + "\n")


# In[43]:


get_ipython().system('ls -lh *txt')


# In[44]:


### combining the dataset with esconv
get_ipython().system(' cat /home/pdey3/blenderbot/_reformat/esconv/sbert/train.txt augesc_train_small.txt > combined_train_small.txt')
get_ipython().system(' cat /home/pdey3/blenderbot/_reformat/esconv/sbert/valid.txt augesc_val_small.txt > combined_val_small.txt')


# In[41]:


get_ipython().system('ls -lh /home/pdey3/blenderbot/_reformat/esconv/sbert/train.txt')


# In[ ]:




