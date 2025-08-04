from ascii_video_lib import ascii_video

vid = ascii_video()

input_path = 'video.mp4'
video_path = 'video/'

txtf = video_path+'video.txt'
mp3f = video_path+'audio.mp3'

vid.ascii_convert(input_path, video_path, 100, 'txt')

fps = float(open(video_path+'fps.txt', 'r').read())

vid.read_video(txtf, mp3f, fps=fps)

