import requests
from gtts import gTTS
import os
import pyttsx3
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx, AudioFileClip, afx, CompositeAudioClip ,concatenate_audioclips, TextClip, CompositeVideoClip
from moviepy.editor import *
from nltk import tokenize
import nltk
import random
from pathlib import Path

app_id = ''
secret = ''
auth = requests.auth.HTTPBasicAuth(app_id, secret)
reddit_username = ''
reddit_password = ''
data = {
'grant_type': 'password',
'username': reddit_username,
'password': reddit_password
}
headers = {'User-Agent': 'MyAPI/0.0.1'}
res = requests.post('https://www.reddit.com/api/v1/access_token',
auth=auth, data=data, headers=headers)
#print(res.json())
TOKEN = res.json()['access_token']

headers['Authorization'] = f'bearer {TOKEN}'
#print(headers)

requests.get('https://oauth.reddit.com/api/v1/me', headers=headers).json()
#print(requests.get('https://oauth.reddit.com/api/v1/me',headers=headers).json())

res = requests.get('https://oauth.reddit.com/r/confession/hot', headers=headers).json() #'https://oauth.reddit.com/r/confession/hot'

#print(res)

comments = requests.get('https://oauth.reddit.com/r/AskReddit/comments/yl8b5f/what_show_has_no_likable_characters.json', headers=headers).json()

text_len = 0
font_size = 50
comment_index = 1
number_of_comments = 6
i = 0
ii = 0
sentences = []
sentences_audio = []

for title in comments[0]['data']['children']:
    converter = pyttsx3.init()
    converter.setProperty('rate', 150)
    converter.setProperty('volume', 0.8)

    videoIndex = random.randint(0, 12)
    videoIndex_str = str(videoIndex)

    backGroundVid = VideoFileClip(os.path.dirname(__file__) + "\\Minecraft\\" + videoIndex_str + ".mp4")
    finalVideo = backGroundVid

    title = title['data']['title']
    converter.save_to_file(title, "title_TTS.mp3")
    converter.runAndWait()

    title_TTS = AudioFileClip("title_TTS.mp3")
    title_txt_clip = TextClip(title, fontsize=font_size, color="white", stroke_color="black", stroke_width=1,method="caption")
    title_txt_clip = title_txt_clip.set_position(("Center", "Top")).set_duration(title_TTS.duration)
    sentences.insert(0, title_txt_clip)
    sentences_audio.insert(0, title_TTS)

    for comment in comments[comment_index]['data']['children']:
        comment = comment['data']['body']
        #comment = "Comment : " + comment
        comment_len = len(comment)

        if comment_len > 150:
            continue

        str_i = str(comment_index)
        fileName = "comment_TTS_" + str_i + ".mp3"
        converter.save_to_file(comment, fileName)
        converter.runAndWait()
        sentence_TTS = AudioFileClip(fileName)

        comment_txt_clip = TextClip(comment, fontsize=font_size, color="white", stroke_color="black", stroke_width=1, method="caption")
        comment_txt_clip = comment_txt_clip.set_position(("Center", "Top")).set_duration(sentence_TTS.duration)

        sentences.insert(comment_index, comment_txt_clip)
        sentences_audio.insert(comment_index, sentence_TTS)

        if comment_index == number_of_comments:
            break

        comment_index += 1

    final_txt_clip = concatenate_videoclips(sentences)
    final_txt_clip = final_txt_clip.set_position('center')

    final_audio_clip = concatenate_audioclips(sentences_audio)

    finalVideo = CompositeVideoClip([finalVideo, final_txt_clip])

    finalVideo.audio = CompositeAudioClip([final_audio_clip])

    print(finalVideo.duration)

    for sent in sentences:
        text_len += sent.duration

    finalVideo = finalVideo.subclip(0, text_len)

    finalVideo.write_videofile("FinalVideo.mp4")

    break







