#!/usr/bin/env python
# coding: utf-8

# In[25]:


### loading data
# data_file = "/home/pdey3/blenderbot/_reformat/augesc/augesc.txt"
data_file = "/Users/priyanka/Downloads/augesc.txt"


# In[26]:


get_ipython().system(' ls -l ~/Downloads/augesc.txt')


# In[27]:


data = open(data_file, "r")
data = data.readlines()


# In[28]:


data = [d[:-1] for d in data]


# In[29]:


### need to convert this so that it resembles KEMI data structure
#'dialog': [
        #{'text': 'Hi', 
        # 'speaker': 'usr' 
        #}, 
        #{'text': 'Hi, I am here to support you in anyway that I can how is your day going?', 
        #'speaker': 'sys', 
        #} 


# In[30]:


import ast


# In[31]:


ast.literal_eval(data[0])


# In[32]:


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


# In[33]:


results[0]


# In[59]:


train_examples = results[:int(8*len(results)/10)]
val_examples = results[int(8*len(results)/10)+1:int(9*len(results)/10)]
test_examples = results[int(9*len(results)/10)+1:]
len(test_examples)


# In[52]:


len(train_examples) + len(val_examples) + len(test_examples)


# In[61]:


### write to files 
import json

train_file = open("/Users/priyanka/Downloads/augesc_train.txt", "w")
for t in train_examples: 
    train_file.write(json.dumps(t) + "\n")
val_file = open("/Users/priyanka/Downloads/augesc_val.txt", "w")
for t in val_examples: 
    val_file.write(json.dumps(t) + "\n")
test_file = open("/Users/priyanka/Downloads/augesc_test.txt", "w")
for t in test_examples: 
    test_file.write(json.dumps(t) + "\n")


# In[ ]:




