#!/usr/bin/env python

from pytube import YouTube
import sys
import ffmpeg
import http.client
import argparse
def main():
    #command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('link', help="Enter the YouTube link to a video here.")
    parser.add_argument("-t", "--type", help="Select the type you want to download. Can be audio or video. Defaults to video.")
    parser.add_argument("-q", "--quality", help="Choose video quality. Can be 1080p, 720p, 480p, etc. If not specified, defaults to highest available.")
    args = parser.parse_args()

    dlVideo(args.link, args.type, args.quality)
    print("Done")




def dlVideo(link, dltype = "video", resolution = None):
    try:
        yt = YouTube(link)
    except Exception as e:
        print("Invalid video link: " + str(e))
        exit()
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
        print("Incorrect video type given.")
        exit()

def joinVideo(videoname, audioname):
    audio = ffmpeg.input(videoname)
    video = ffmpeg.input(audioname)
    ffmpeg.output(video, audio, "video.mp4", vcodec = "copy", acodec ="copy",).run()

if __name__ == "__main__":
    main()
