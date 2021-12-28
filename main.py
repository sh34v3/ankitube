#!/usr/bin/env python 

#^^special shebang instructs linux to use the python binary being used by virtualenv


#import library for nice typing of complex data structures
from typing import Dict, List, Tuple
#import os library for making a directory
import os
#import glob for getting frame files
import glob
#import web scraping libraries
from pytube import YouTube
#import ffmpeg tool from moviepy for slicing clips from mp4
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
#import OpenCV for getting JPEGs for making GIFs
import cv2
#import Pillow to create GIFs from JPEGs
from PIL import Image

#where to save media
SAVE_PATH = os.getcwd()+"/media/"
SCRIPT_DIR = os.getcwd()

#extract a clip from a given video using moviepy
def clip_mp4(start_time: int, end_time: int, infile_video: str):
    outfile_clip = "clip.mp4"
    ffmpeg_extract_subclip(SAVE_PATH+infile_video, start_time, end_time, targetname=SAVE_PATH + outfile_clip)
    return outfile_clip

#convert a given video into a series of images
def convert_mp4_to_jpgs(infile_video: str):
    print("**Making frames from clip**")
    #get video
    video_capture = cv2.VideoCapture(SAVE_PATH+infile_video)
    #make image dir
    try:
        os.mkdir(SAVE_PATH+"temp_frame_dir")
    except FileExistsError:
        #remove and remake tempdir if it already exists
        os.system("rm -r {}temp_frame_dir".format(SAVE_PATH))
        os.mkdir(SAVE_PATH+"temp_frame_dir")
    #change directory to temp_frame_dir
    os.chdir(SAVE_PATH+"temp_frame_dir")
    #get continue flag and first frame
    still_reading, image = video_capture.read()
    #accumulator variable
    frame_count = 0
    while still_reading:
        #write image
        cv2.imwrite(str(frame_count)+".png", image)

        #read next image
        still_reading, image = video_capture.read()
        frame_count+= 1
    
    #change directory back
    os.chdir(SCRIPT_DIR)
    print("**Frames finished!**")

#sort a list of string based on numerical file prefix
def numSort(e):
    return eval(e[:-4])

def make_gif(outfile: str):
    print("**Cooking GIF soup**")
    #changedirs
    os.chdir(SAVE_PATH+"temp_frame_dir/")
    #get frames
    images = glob.glob("*.png")
    images.sort(key=numSort)
    #open frames as proper frames
    frames = [Image.open(image) for image in images] #cool list comprehension!
    frame_one = frames[0]
    frame_one.save(SAVE_PATH+outfile+".gif", format="GIF", append_images=frames, save_all=True,
                    duration=33, loop=0)
    print("**GIF ready**")

def main():

    #link of video to be downloaded
    link: str = "https://www.youtube.com/watch?v=YzRaWy7NG4M&ab_channel=Engineeringandarchitecture"
    video_name: str = "pile_driving"

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

    clip_start: int = eval(input("Enter clip start timestamp in seconds: "))
    clip_end: int = eval(input("Enter clip end timestamp in seconds: "))

    clip = clip_mp4(clip_start, clip_end, download_video.default_filename)
    convert_mp4_to_jpgs(clip)
    make_gif(input("What would you like to call your GIF: "))
main()