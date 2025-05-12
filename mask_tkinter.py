import os
import cv2
from tkinter import (
    filedialog,
    colorchooser,
    messagebox,
    END,
    Label,
    Button,
    Entry,
    Tk,
)
from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip
from PIL import Image, ImageTk


def mask_position(vw, vh, mw, mh, position):
    if position[0] == "left":
        x = 0
    elif position[0] == "center":
        x = (vw - mw) / 2
    elif position[0] == "right":
        x = vw - mw
    else:
        x = float(position[0])

    if position[1] == "top":
        y = 0
    elif position[1] == "center":
        y = (vh - mh) / 2
    elif position[1] == "bottom":
        y = vh - mh
    else:
        y = float(position[1])

    return max(0, x), max(0, y)


def add_mask(video_input, mask_width, mask_height, color, position):
    if isinstance(video_input, str):
        # If the input is a file path, create a VideoFileClip
        video = VideoFileClip(video_input)
        preview_prop_x_y.config(text="")
    else:
        # Otherwise, assume it's a VideoFileClip object
        video = video_input
        preview_prop_x_y.config(text=f"({video.w}, {video.h})")

    position = mask_position(video.w, video.h, mask_width, mask_height, position)

    mask = ColorClip(size=(mask_width, mask_height), color=color)
    mask = mask.set_position(position).set_duration(video.duration)

    final_video = CompositeVideoClip([video, mask.set_opacity(1)])
    return final_video


def process_videos(
    input_paths, output_folder, mask_width, mask_height, color, position
):
    for input_path in input_paths:
        # output_path = os.path.join(output_folder, os.path.basename(input_path))
        original_name = os.path.splitext(os.path.basename(input_path))[0]  # Get the original filename without extension
        masked_name = f"m_{original_name}.mp4"  # Create the new filename
        output_path = os.path.join(output_folder, masked_name)  # Construct the new path
        try:
            final_video = add_mask(input_path, mask_width, mask_height, color, position)
            final_video.write_videofile(output_path, codec="libx264")
            # messagebox.showinfo("Success", f"Processed: {os.path.basename(input_path)}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


def upload_video():
    filenames = filedialog.askopenfilenames(filetypes=[("MP4 files", "*.mp4")])
    entry_video_path.delete(0, END)
    entry_video_path.insert(0, ", ".join(filenames))
    preview_video()


def preview_video():
    label_preview.img_tk = None  # Clear the previous reference
    if entry_video_path.get():
        first_video = entry_video_path.get().split(", ")[0]
        mask_width = int(entry_width.get())
        mask_height = int(entry_height.get())
        color_hex = entry_color.get()
        color_rgb = tuple(int(color_hex[i : i + 2], 16) for i in (1, 3, 5))
        position = (entry_x.get(), entry_y.get())

        short_video = VideoFileClip(first_video).subclip(0, 0.01)
        final_video = add_mask(
            short_video, mask_width, mask_height, color_rgb, position
        )
        preview_first_frame(final_video)
    else:
        messagebox.showwarning("No Video", "Please upload video first.")


def preview_first_frame(final_video):
    # Use a temporary file to store the preview video
    temp_file = "temp_preview.mp4"
    final_video.write_videofile(temp_file, codec="libx264", fps=24)

    cap = cv2.VideoCapture(temp_file)
    ret, frame = cap.read()  # Read the first frame
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Maintain aspect ratio and fit in a container size
        container_width, container_height = 400, 300
        h, w, _ = frame.shape

        # Calculate the aspect ratio
        aspect_ratio = w / h

        if aspect_ratio > (container_width / container_height):
            new_width = container_width
            new_height = int(container_width / aspect_ratio)
        else:
            new_height = container_height
            new_width = int(container_height * aspect_ratio)

        img = Image.fromarray(frame)
        img = img.resize(
            (new_width, new_height), Image.LANCZOS
        )  # Use LANCZOS for resizing
        img_tk = ImageTk.PhotoImage(image=img)

        # Update the label with the new frame
        label_preview.img_tk = img_tk  # Keep a reference
        label_preview.config(image=img_tk)
        label_preview.update_idletasks()

    cap.release()
    os.remove(temp_file)  # Clean up the temporary file


def select_color():
    color_code = colorchooser.askcolor(title="Choose color")
    if color_code[1]:
        entry_color.delete(0, END)
        entry_color.insert(0, color_code[1])
        preview_video()


def start_processing():
    video_paths = entry_video_path.get().split(", ")
    output_folder = filedialog.askdirectory(title="Select Output Directory")
    mask_width = int(entry_width.get())
    mask_height = int(entry_height.get())
    color_hex = entry_color.get()
    position = (entry_x.get(), entry_y.get())

    color_rgb = tuple(int(color_hex[i : i + 2], 16) for i in (1, 3, 5))
    process_videos(
        video_paths, output_folder, mask_width, mask_height, color_rgb, position
    )


def set_entry(value, entry):
    entry.delete(0, END)  # Clear the entry
    entry.insert(0, value)  # Set the new value
    if value.startswith("#"):
        preview_video()


# Create the GUI window
root = Tk()
root.title("Video Masking Tool")

# Video path entry
Label(root, text="Video Files:").grid(row=0, column=0)
entry_video_path = Entry(root)
entry_video_path.grid(row=0, column=1)
Button(root, text="Upload MP4", command=upload_video).grid(
    row=0, column=2, columnspan=2
)

# Mask dimensions with default values
Label(root, text="Mask Width (x):").grid(row=1, column=0)
entry_width = Entry(root)
entry_width.insert(0, "100")  # Default value for width
entry_width.grid(row=1, column=1)

Label(root, text="Mask Height (y):").grid(row=2, column=0)
entry_height = Entry(root)
entry_height.insert(0, "100")  # Default value for height
entry_height.grid(row=2, column=1)

# Mask color with default value
Label(root, text="Mask Color:").grid(row=3, column=0)
entry_color = Entry(root)
entry_color.insert(0, "#FFFFFF")  # Default value for color (white)
entry_color.grid(row=3, column=1)
Button(root, text="Select Color", command=select_color).grid(
    row=3, column=2, columnspan=2
)
Button(root, text="Black", command=lambda: set_entry("#000000", entry_color)).grid(
    row=3, column=4
)

# Mask position input
Label(root, text="Mask X Position:").grid(row=4, column=0)
entry_x = Entry(root)
entry_x.insert(0, "0")  # Default value for X position
entry_x.grid(row=4, column=1)
Button(root, text="left", command=lambda: set_entry("left", entry_x)).grid(
    row=4, column=2
)
Button(root, text="center", command=lambda: set_entry("center", entry_x)).grid(
    row=4, column=3
)
Button(root, text="right", command=lambda: set_entry("right", entry_x)).grid(
    row=4, column=4
)


Label(root, text="Mask Y Position:").grid(row=5, column=0)
entry_y = Entry(root)
entry_y.insert(0, "0")  # Default value for Y position
entry_y.grid(row=5, column=1)
Button(root, text="top", command=lambda: set_entry("top", entry_y)).grid(
    row=5, column=2
)
Button(root, text="center", command=lambda: set_entry("center", entry_y)).grid(
    row=5, column=3
)
Button(root, text="bottom", command=lambda: set_entry("bottom", entry_y)).grid(
    row=5, column=4
)

# Preview button
Button(root, text="Preview", command=preview_video).grid(row=6, columnspan=5)

# Frame for video preview
label_preview = Label(root)
label_preview.grid(row=7, columnspan=5)

Label(root, text="Video's (x, y):").grid(row=8, column=0)
preview_prop_x_y = Label(root, text="")
preview_prop_x_y.grid(row=8, column=1)


# Process button
Button(root, text="Download", command=start_processing).grid(row=9, columnspan=5)

root.mainloop()
