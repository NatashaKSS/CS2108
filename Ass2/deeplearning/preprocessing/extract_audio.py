__author__ = "xiangwang1223@gmail.com"

# The simple implementation of obtaining the audio clip of a original video.
import os
import moviepy.editor as mp

def getAudioClip(video_reading_path, audio_storing_path):
    clip = mp.VideoFileClip(video_reading_path)
    clip.audio.write_audiofile(audio_storing_path)

if __name__ == '__main__':
    list_of_video_names = os.listdir("../data/video")
    print(list_of_video_names)

    for video_name in list_of_video_names:
        # 1. Set the access path to the original file.
        video_reading_path = "../data/video/" + video_name
        print(video_reading_path)

        # 2. Set the path to store the extracted audio clip.
        audio_storing_path = "../data/audio/" + video_name[:-4] + ".wav"
        print(audio_storing_path)

        # 3. Fetch and store the corresponding audio clip.
        getAudioClip(video_reading_path=video_reading_path, \
                     audio_storing_path=audio_storing_path)
