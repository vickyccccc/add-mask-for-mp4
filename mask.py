import os
from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip


def mask_logo(video_path, output_path):
    # Load the video
    video = VideoFileClip(video_path)

    # Define the dimensions of the logo area (adjust as needed)
    logo_width = 100  # Width of the logo to mask
    logo_height = 100  # Height of the logo to mask
    position = (video.w - logo_width, 0)  # Top right corner

    # Create a colored clip to mask the logo (black color, for example)
    mask = ColorClip(size=(logo_width, logo_height), color=(255, 255, 255))
    mask = mask.set_position(position).set_duration(video.duration)

    # # Create a composite video clip with the mask
    # final_video = CompositeVideoClip([video, mask])
    final_video = CompositeVideoClip([video, mask.set_opacity(1)])

    # # Write the result to a file
    final_video.write_videofile(output_path, codec="libx264")


def process_videos(input_folder, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Process each MP4 file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".mp4"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            mask_logo(input_path, output_path)


input_folder = "./in"
output_folder = "./out"
process_videos(input_folder, output_folder)
