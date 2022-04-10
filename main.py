#!/usr/bin/env python

from pytube import YouTube
import sys
import ffmpeg
import http.client

def main(link, dltype, resolution = None):
    dlVideo(link, dltype, resolution)
    print("Done")




def dlVideo(link, dltype, resolution = None):
    yt = YouTube(link)
    if dltype == "video":
        attempt = 0
        maxretries = 5
        while attempt < maxretries:
            try:
                if resolution == None:
                    stream = yt.streams.filter(only_video = True, file_extension="mp4")
                elif type(resolution) == str:
                    stream = yt.streams.filter(only_video = True, file_extension="mp4", res=resolution)
                    if len(stream) == 0:
                        print("No suitable video found. Maybe the video quality value is wrong or the video doesn't have that resolution?")
                        exit()
                stream[0].download(filename="videopart.mp4")
                break
            except http.client.IncompleteRead:
                print("Error occured, retrying...")
                attempt = attempt + 1
        if attempt == 5:
            print("Error has occured. Max retries reached. Exiting...")
            exit()
        attempt = 0
        while attempt < maxretries:
            try:
                stream = yt.streams.get_audio_only()
                stream.download(filename="audiopart.mp4")
                break
            except http.client.IncompleteRead:
                print("Error occured, retrying...")
                attempt = attempt + 1
        if attempt == 5:
            print("Error has occured. Max retries reached. Exiting...")
            exit()
        attempt = 0
        joinVideo("videopart.mp4", "audiopart.mp4")
    elif dltype == "audio":
        attempt = 0
        maxretries = 5
        while attempt < maxretries:
            try:
                stream = yt.streams.get_audio_only()
                stream.download(filename="audio.mp4")
                break
            except http.client.IncompleteRead:
                print("Error occured, retrying...")
                attempt = attempt + 1
        if attempt == 5:
            print("Error has occured. Max retries reached. Exiting...")
            exit()
        attempt = 0
    else:
        print("Incorrect video type. Correct usage: python main.py link audio/video quality(Optional, 1080p,720p,480p,360p)")

def joinVideo(videoname, audioname):
    audio = ffmpeg.input(videoname)
    video = ffmpeg.input(audioname)
    ffmpeg.output(video, audio, "video.mp4", vcodec = "copy", acodec ="copy",).run()

if __name__ == "__main__":
    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        ("Incorrect amount of arguments given. Correct usage: python main.py YoutubeLink type(audio or video) quality(Optional, 1080p,720p,480p,360p)")
