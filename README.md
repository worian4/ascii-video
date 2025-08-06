# ascii-video
Creates and displays in the terminal an ASCII video

To use it, upload a video to it, convert it into ASCII and read it by commands in ```ascii-video``` library as shown in main.py.

Functions:
```ascii_video.convert(input_path, output, format, new_width, rgb)``` - to convert a normal video to an ascii video. ```input_path``` and ```output_path``` stand for directions where for the program to get the video and direction or folder to place the ascii video (if folder doesn't exist it'll be created and files whithin will be deleted if exists). ```format``` (```'txt'``` by default) means how you want to save it and how you want it to be played later. If you choose ```'txt'```, it means that the program creates a folder with ```.mp3``` file for sound and ```.txt``` file for video, which can be displayed later in terminal by ```ascii_video.read```. If you choose ```'mp4'```, it means that the program will create an ```.mp4``` file with the ascii video in it. ```new_width``` (100 by default) means the width of the output video in symbols (heigth is created proportionally). Finally, ```rgb``` means weather you want to add color or not.

```ascii_video.read_video(video, audio, fps)``` - used to display the video in termainal if you've choosed ```'txt'``` while converting the video. ```
