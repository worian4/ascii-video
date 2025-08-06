from PIL import Image, ImageDraw, ImageFont
import cv2
from sys import stdout
import time
import numpy as np
from bs4 import BeautifulSoup
import re
import shutil
import os
from moviepy import VideoFileClip
import threading
import subprocess
from pydub import AudioSegment



ASCII_CHARS = '@#W$%&B8MHKRQDNXAUO0gpdb69ZvYwEqahP4GmT35SzLnVyFtuJkex1Cf7r2o+ijslc=*[]{/}?^()/!|<>"~-_;:,.` '[::-1]
animation = '|/-\\'

colors = [
    [(255, 0, 0), (0, 255, 0), (0, 0, 255), (100, 100, 100)],
    [(200, 200, 0), (0, 200, 200), (200, 0, 200), (50, 50, 50)]
]

class ascii_video:

    def loading(self, start, point, list_len):
        return str(format(point/list_len*100,'f'))[:10]+'% '+animation[int(((start-time.time())/0.2)%4)]
    
    def play_audio(self, path):

        subprocess.run(
        ["ffplay", "-nodisp", "-autoexit", path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
        )
    
    def display_ascii_video_smooth(self, frames, fps):

        start_time = time.time()
        frame_duration = 1 / fps

        for i, frame in enumerate(frames):
            current_time = time.time()
            expected_time = start_time + i * frame_duration
            time_to_wait = expected_time - current_time
            if time_to_wait > 0:
                time.sleep(time_to_wait)

            stdout.write("\x1b[H")
            stdout.write(frame)
            stdout.flush()

    def save_ascii_to_txt(self, ascii_image, output_path="ascii_bw.txt"):

        f = open(output_path, 'a', encoding="utf-8")
        for line in ascii_image:
            f.write(line + '\n')
        f.write('qwerty')


    def ascii_to_bw_image(self, ascii_image, font_path, font_size=10, text_color="black", bg_color="white"):

        img_width = len(ascii_image[0]) * font_size // 2
        img_height = len(ascii_image) * font_size

        img = Image.new('RGB', (img_width, img_height), color=bg_color)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font_path, font_size)

        for y, line in enumerate(ascii_image):
            for x, char in enumerate(line):
                draw.text((x * font_size // 2, y * font_size), char, fill=text_color, font=font)

        return np.array(img)
    
    def frame_to_ascii_bw(self, image, new_width=120):

        height, width, _ = image.shape
        aspect_ratio = height / width
        new_height = int(aspect_ratio * new_width * 0.55)

        resized = cv2.resize(image, (new_width, new_height))
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        normalized = (gray / 255) * (len(ASCII_CHARS) - 1)

        ascii_image = []
        for y in range(new_height):
            line = ''
            for x in range(new_width):
                char = ASCII_CHARS[int(normalized[y, x])]
                line += char
            ascii_image.append(line)
        return ascii_image

    def save_colored_ascii_to_txt(self, ascii_image, color_map, output_path="ascii_color.txt"):

        f = open(output_path, 'a', encoding="utf-8")
        for line_chars, line_colors in zip(ascii_image, color_map):
            for ch, (r, g, b) in zip(line_chars, line_colors):
                ansi_color = f"\x1b[38;2;{r};{g};{b}m{ch}"
                f.write(ansi_color)
            f.write("\x1b[0m\n")
        f.write('qwerty')
        
    def frame_to_ascii_color(self, image, new_width=120):

        height, width, _ = image.shape
        aspect_ratio = height / width
        new_height = int(aspect_ratio * new_width * 0.55)

        resized = cv2.resize(image, (new_width, new_height))
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        normalized = (gray / 255) * (len(ASCII_CHARS) - 1)

        ascii_image = []
        color_map = []

        for y in range(new_height):
            line = ''
            colors = []
            for x in range(new_width):
                char = ASCII_CHARS[int(normalized[y, x])]
                line += char
                b, g, r = resized[y, x]
                colors.append((r, g, b))
            ascii_image.append(line)
            color_map.append(colors)
        return ascii_image, color_map

    def ascii_to_color_image(self, ascii_image, colors, font_path, font_size=10):

        img_width = len(ascii_image[0]) * font_size // 2
        img_height = len(ascii_image) * font_size

        img = Image.new('RGB', (img_width, img_height))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font_path, font_size)

        for y, (line, row_colors) in enumerate(zip(ascii_image, colors)):
            for x, (char, color) in enumerate(zip(line, row_colors)):
                draw.text((x * font_size // 2, y * font_size), char, fill=color, font=font)

        return np.array(img)

    def ascii_convert(self, input_path, output, new_width, format, rgb):

        _ = os.system('cls')

        try: shutil.rmtree(output)
        except: pass
        os.makedirs(output, exist_ok=True)

        video = VideoFileClip(input_path)
        if video.audio is not None:
            video.audio.write_audiofile(output+'audio.mp3')
        else:
            silent = AudioSegment.silent(duration=1000)
            silent.export(output+'audio.mp3', format="mp3")

        output_path = 'output.mp4'
        font_path = r"C:\Windows\Fonts\consola.ttf" #you can change this to dejavu-fonts if using linux or mac
        font_size = 10
        
        if format in ['txt']:
            try: os.remove(output+'video.txt')
            except: pass
            file = open(output+'video.txt', 'w', encoding='utf-8')

        cap = cv2.VideoCapture(input_path)
        fps = cap.get(cv2.CAP_PROP_FPS)

        ret, first_frame = cap.read()
        if not ret: raise RuntimeError('Couldn\'t find the video')

        height, width = first_frame.shape[:2]
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        if format == 'mp4': out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        counter = 0
        start = time.time()

        while cap.isOpened():

            stdout.write('\rbuilding video: '+self.loading(start, counter, frame_count))
            stdout.flush()

            ret, frame = cap.read()
            if not ret:
                break

            if rgb: ascii_img, colors = self.frame_to_ascii_color(frame, new_width=new_width)
            else: ascii_img = self.frame_to_ascii_bw(frame, new_width=new_width)

            if format == 'mp4':
                if rgb: ascii_frame = self.ascii_to_color_image(ascii_img, colors, font_path, font_size)
                else: ascii_frame = self.ascii_to_bw_image(ascii_img, font_path, font_size)
                ascii_frame = cv2.resize(ascii_frame, (width, height))

                out.write(cv2.cvtColor(ascii_frame, cv2.COLOR_RGB2BGR))
            if format == 'txt':
                if rgb: self.save_colored_ascii_to_txt(ascii_img, colors, output_path=output+'video.txt')
                else: self.save_ascii_to_txt(ascii_img, output_path=output+'video.txt')

            counter += 1

        cap.release()
        if format == 'mp4': out.release()
        
        stdout.write('\rDone!'+' '*30)

        f_fps = open(output+'fps.txt', 'w')
        f_fps.write(str(fps))

    def read_video(self, path):
        
        _ = os.system('cls')

        frames = open(path+'/video.txt', 'r', encoding='utf-8').read().split('qwerty')

        audio_thread = threading.Thread(target=self.play_audio, args=path+'/audio.mp3',)
        audio_thread.start()

        fps = float(open(path+'fps.txt', 'r').read())

        self.display_ascii_video_smooth(frames, fps)
        audio_thread.join()

        _ = os.system('cls')

    def __init__(self):
        self.frames = []




