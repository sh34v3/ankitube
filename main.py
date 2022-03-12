#!/usr/bin/env python 

#^^special shebang instructs linux to use the python binary being used by virtualenv


#import tkinter
from tkinter import *

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

#import library for nice typing of complex data structures
from typing import Dict, List, Tuple
#import os library for making a directory
import os
#import subprocess for callimg ffmpeg
import subprocess

#import web scraping libraries
from pytube import YouTube

#import ffmpeg tool from moviepy for slicing clips from mp4
import moviepy.video.io.ffmpeg_tools as FFMpeg
import moviepy.editor as mp

#import ffmpeg
import ffmpeg

youtube="https://www.youtube.com/watch?v=PuKKL3tOXfo&t=90s&ab_channel=UniversalPictures"

#where to save media
SAVE_PATH = os.getcwd()+"/media/"
SCRIPT_DIR = os.getcwd()

#extract a clip from a given video using moviepy
def clip_mp4(start_time: int, end_time: int, infile_video: str, name: str):
    os.chdir(SAVE_PATH) # change working directory to media temp directory

    infile = str(SAVE_PATH+infile_video)
    infile = str('\"'+infile+'\"')
    outfile_clip = SAVE_PATH + name + ".webm"
    
    #subprocess.call(str('ffmpeg -i '+infile_video+' -c:v libvpx-vp9 -b:v 2M -pass 1 -an -f null /dev/null && \ '))
    subprocess.call([
        'ffmpeg',                   # call ffmpeg
        '-i', infile_video,         # this is the video to be converted
        '-threads', '4',            # use 4 threads for the video conversion
        '-c:v', 'libvpx-vp9',       # c[odec]:v[ideo] - we use libvpx cause we want webm
        '-c:a', 'libvorbis',        # c[odec]:a[udio] - this is the one everyone else was using
        '-b:v',  '400k',            # reccomended video bitrate
        '-b:a', '192k',             # reccomended audio bitrate
        '-vf', 'trim='+str(start_time)+':'+str(end_time), # trim the video to desired points during rencoding
        '-deadline', 'realtime',    # setting for quality vs. speed (best, good, realtime (fastest)); boundry for quality vs. time set the following settings
        '-qmin', '0',               # quality minimum boundry. (lower means better)
        '-qmax', '50',              # quality maximum boundry (higher means worse)
        'y',                        # overwrite the file if it's in the directory
        'outfile.webm'              # file to be written out
    ])
   

    # stream = ffmpeg.input(SAVE_PATH+infile_video)
    # inv = stream.video
    # inv = inv.trim(start=start_time, end=end_time)
    # ina = stream.audio
    # ina = ina.atrim(start=start_time, end=end_time)
    # out = ffmpeg.output(inv, ina, outfile_clip)
    # out.run()

    #stream = ffmpeg.input(outfile_clip)
    #stream = ffmpeg.output(stream, outfile_clip, {'c:v' : 'libvpx-vp9','b:v':'2M','pass':'1','c:a':'libopus','y':''})
    #ffmpeg.run(stream)'


def main():

    #link of video to be downloaded
    link: str = input("Please enter video link: ")
    video_name: str = "temp"

    try:
        print("**getting youtube video object**")
        #getting youtube video object
        yt = YouTube(link)
    except:
        print("Connection Error")
    
    #get mp4 StreamQuery
    mp4files = yt.streams.filter(file_extension='mp4')

    #get highest resolution Stream available in mp4files
    download_video = mp4files.get_highest_resolution()

  
    # downloading video
    download_video.download(output_path=SAVE_PATH)
 
    print("**download complete**")


    #I with the program would handle my typos
    clip_start: int = input("Enter clip start timestamp like so: min sec: ")
    clip_start = eval(clip_start[0])*60 + eval(clip_start[2:])
    clip_end: int = input("Enter clip end timestamp like so: min sec: ")
    clip_end = eval(clip_end[0])*60 + eval(clip_end[2:])
    clip = clip_mp4(clip_start, clip_end, download_video.default_filename, "clip")
