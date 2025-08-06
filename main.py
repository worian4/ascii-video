from core.ascii_video_lib import ascii_video

vid = ascii_video()

input_path = 'videos/11.mp4'
video_path = 'video'

vid.ascii_convert(input_path, video_path, 'txt', new_width=500, rgb=1)

vid.read_video(video_path)
