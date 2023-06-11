# virtualenvironment creation
# python -m venv youtube_env 
# to activate ctrl+shift+p

API_KEY='AIzaSyC0tvq0iyU4i84OVwNkDhQ3tuVo-MBoGQs'
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_channel_id(channel_name):
        response = youtube.search().list(
            part='id',
            q=channel_name,
            type='channel'
        ).execute()
        channel = response['items'][0]
        channel_id = channel['id']['channelId']
        return channel_id


def get_channel_details(channel_id):
    response = youtube.channels().list(
        part='snippet,statistics,contentDetails',
        id=channel_id
    ).execute()
    
    channel_details = response['items'][0]
    channel_title = channel_details['snippet']['title']
    subscriber_count = channel_details['statistics']['subscriberCount']
    view_count = channel_details['statistics']['viewCount']
    description = channel_details['snippet']['description']
    
    channel_details = {
        'Channel_Name': channel_title,
        'Channel_Id': channel_id,
        'Subscription_Count': subscriber_count,
        'Channel_Views': view_count,
        #'Channel_Description': description,

    }
    return channel_details

def get_channel_playlists(channel_id):
        response = youtube.playlists().list(
            part='snippet',
            channelId=channel_id,
            maxResults=10  # Adjust the maximum number of playlists to retrieve
        ).execute()

        playlists = response['items']
        channel_playlists={}
        for playlist in playlists:
            playlist_id = playlist['id']
            playlist_title = playlist['snippet']['title']
            channel_playlists[playlist_title]=playlist_id
        return channel_playlists

def get_playlist_videos(playlist_id):
    response = youtube.playlistItems().list(
        part='snippet',
        playlistId=playlist_id,
        maxResults=50
    ).execute()

    videos = response['items']
    playlist_videos = {}

    for video in videos:
        video_id = video['snippet']['resourceId']['videoId']
        video_title = video['snippet']['title']

        video_info = youtube.videos().list(
            part='snippet,statistics,contentDetails',
            id=video_id
        ).execute()

        video_data = video_info['items'][0]
        video_details = {
            'Video_Id': video_id,
            'Video_Name': video_title,
            #'Video_Description': video_data['snippet']['description'],
            'Tags': video_data['snippet'].get('tags', []),
            'PublishedAt': video_data['snippet']['publishedAt'],
            'View_Count': video_data['statistics']['viewCount'],
            'Like_Count': video_data['statistics']['likeCount'],
            # 'Dislike_Count': video_data['statistics']['dislikeCount'],
            'Favorite_Count': video_data['statistics']['favoriteCount'],
            'Comment_Count': video_data['statistics']['commentCount'],
            'Duration': video_data['contentDetails']['duration'],
            'Thumbnail': video_data['snippet']['thumbnails']['default']['url'],
            #'Caption_Status': video_data['snippet']['caption'],
            'Comments': {}
        }

        comment_response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=5  # Adjust the maximum number of comments to retrieve
        ).execute()

        comments = comment_response['items']
        for comment in comments:
            comment_id = comment['id']
            comment_text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
            comment_author = comment['snippet']['topLevelComment']['snippet']['authorDisplayName']
            comment_published_at = comment['snippet']['topLevelComment']['snippet']['publishedAt']

            comment_details = {
                'Comment_Id': comment_id,
                'Comment_Text': comment_text,
                'Comment_Author': comment_author,
                'Comment_PublishedAt': comment_published_at
            }

            video_details['Comments'][comment_id] = comment_details

        playlist_videos[video_title] = video_details

    return playlist_videos

#-----------------------------MAIN------------------------------------------#

select_box='channel_name' # or channel_id
channel_identity='Microsoft Develope123'
if select_box=='channel_name':
        channel_id=get_channel_id(channel_identity)
elif select_box=='channel_id':
        channel_id=channel_identity

channel_details=get_channel_details(channel_id)  
channel_playlists=get_channel_playlists(channel_id)
print(channel_details)
print(channel_playlists)

# channel_title = channel_details['snippet']['title']
# subscriber_count = channel_details['statistics']['subscriberCount']
# view_count = channel_details['statistics']['viewCount']
# description = channel_details['snippet']['description']
# video_count = channel_details['statistics']['videoCount']

# # Print the extracted information
# print("Channel Title:", channel_title)
# print("Subscriber Count:", subscriber_count)
# print("View Count:", view_count)
# #print("Description:", description)
# print("Video Count:", video_count)
# print(json.dumps(channel_details, indent=4))
# for key, value in channel_playlists.items():
#       print(json.dumps(get_playlist_videos(value), indent=4))
#       break


