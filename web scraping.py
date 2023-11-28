#!/usr/bin/env python
# coding: utf-8

# In[1]:


from googleapiclient.discovery import build
import pandas  as pd 
import seaborn as sns


# In[2]:


api_key = 'AIzaSyATXxDbbDOAYJ3MgbxjR1qifKhwGeWC02M'
channel_ids = ['UCxgAuX3XZROujMmGphN_scA',
             'UCIaH-gZIVC432YRjNVvnyCA',
             'UCWsDFcIhY2DBi3GB5uykGXA',  
             'UCvgfXK4nTYKudb0rFR6noLA',
             'UCcyq283he07B7_KUX07mmtA'
              ]

youtube = build('youtube','v3', developerKey=api_key)


# ## funcrtion to get channel statistics

# In[3]:


def get_channel_stats(youtube,channel_ids):
    all_data=[]
    request = youtube.channels().list(
                 part='snippet,contentDetails,statistics',
                 id = ','.join(channel_ids))
    response = request.execute()
    for i in range(len(response['items'])):
        data= dict(Channel_name = response['items'][i]['snippet']['title'],
                   Subscribers = response['items'][i]['statistics']['subscriberCount'],
                   Views =response['items'][i]['statistics']['viewCount'],
                   Total_videos =response['items'][i]['statistics']['videoCount'],
                  playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
        all_data.append(data)
    return all_data


# In[4]:


channel_statistics=get_channel_stats(youtube,channel_ids)


# In[5]:


ch_data=pd.DataFrame(channel_statistics)
ch_data


# In[6]:


ch_data['Subscribers'] = pd.to_numeric(ch_data['Subscribers'])
ch_data['Views'] = pd.to_numeric(ch_data['Views'])
ch_data['Total_videos'] = pd.to_numeric(ch_data['Total_videos'])
ch_data.dtypes


# In[7]:


sns.set(rc={'figure.figsize':(10,8)})
ax =sns.barplot(x='Channel_name',y='Subscribers',data = ch_data)


# In[8]:


ax =sns.barplot(x='Channel_name',y='Views',data = ch_data)


# In[9]:


ax =sns.barplot(x='Channel_name',y='Total_videos',data = ch_data)


# # Funtion to get video id
# 

# In[32]:


ch_data


# In[33]:


playlist_id = ch_data.loc[ch_data['Channel_name']=='IShowSpeed', 'playlist_id'].iloc[0]


# In[34]:


playlist_id


# In[35]:


def get_video_ids(youtube,playlist_id):
    request = youtube.playlistItems().list(
                part ='contentDetails',
                playlistId = playlist_id,
                maxResults = 50)
    response = request.execute()
    
    video_ids = []
    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])
    next_page_token = response.get('nextPageToken')
    more_pages = True 
        
    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(
                        part ='contentDetails',
                        playlistId = playlist_id,
                        maxResults = 50,
                        pageToken = next_page_token)
            response = request.execute()
            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])
            next_page_token = response.get('nextPageToken')
    return video_ids


# In[36]:


video_ids = get_video_ids(youtube,playlist_id)


# In[37]:


video_ids


# In[38]:


video_ids


# #Function details 

# In[43]:


def get_video_details(youtube, video_ids):
    all_video_stats = []
    for i in range(0, len(video_ids),50):
        request = youtube.videos().list(
                    part='snippet,statistics',
                    id=','.join(video_ids[i:i+50]))
        response = request.execute()
        for video in response['items']:
             
            video_stats = dict(Title = video['snippet']['title'],
                               Published_date = video['snippet']['publishedAt'],
                               Views = video['statistics']['viewCount'],
                               Likes = video['statistics']['likeCount'],
                               
                               Comments = video['statistics']['commentCount']
                                   )
            all_video_stats.append(video_stats)
        
            
       
        return all_video_stats
   


# In[44]:


video_details = get_video_details(youtube, video_ids)


# In[46]:


video_data = pd.DataFrame(video_details)


# In[47]:


video_data


# In[51]:


video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date
video_data['Views'] = pd.to_numeric(video_data['Views'] )
video_data['Likes'] = pd.to_numeric(video_data['Likes'] )
video_data['Views'] = pd.to_numeric(video_data['Views'] )
video_data


# In[57]:


top10_videos = video_data.sort_values(by = 'Views',ascending = False).head(10)
top10_videos


# In[58]:


ax1=sns.barplot(x='Views',y='Title',data=top10_videos)


# In[60]:


video_data


# In[64]:


video_data['Month'] =pd.to_datetime(video_data['Published_date']).dt.strftime('%b')


# In[65]:


video_data


# In[71]:


videos_per_month = video_data.groupby('Month', as_index=False).size()


# In[72]:


videos_per_month


# In[78]:


sort_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']  


# In[83]:


videos_per_month.index = pd.Categorical(videos_per_month['Month'], categories=sort_order, ordered=True)


# In[84]:


videos_per_month = videos_per_month.sort_index()


# In[85]:


ax2 = sns.barplot(x='Month',y = 'size',data=videos_per_month)


# In[86]:


video_data.to_csv('Video_Details(Ken Jee).csv')


# In[ ]:




