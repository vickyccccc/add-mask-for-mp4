# Video Masking Tool
![License](https://img.shields.io/badge/license-MIT-brightgreen)
![Python Version](https://img.shields.io/badge/python-3.x-blue)
![Version](https://img.shields.io/badge/version-v1.0.0-orange)
![Version](https://img.shields.io/badge/MoviePy-1.0.3-yellow)

## Overview
The Video Masking Tool is a graphical user interface (GUI) application that allows users to overlay a colored mask on videos. Users can customize the mask's dimensions, color, and position, and the application supports MP4 video files.

## Features
- **Upload Video**: Select one or multiple MP4 video files for processing.
- **Mask Customization**:
  - Set width and height of the mask.
  - Choose a color for the mask using a color picker or predefined options (e.g., black).
  - Define the mask's position (left, center, right for X; top, center, bottom for Y).
- **Preview Functionality**: Preview the mask on a short clip of the selected video.
- **Processing**: Generate the final video with the mask applied and save it to a specified directory.

## Requirements
- Python 3.x
- Required libraries:
  - **opencv-python**: 4.11.0.86
  - **moviepy**: 1.0.3
  - **Pillow**: 10.4.0
  - **Tkinter**: (standard with Python)

You can install the required libraries using pip:

```bash
pip install opencv-python moviepy==1.0.3 Pillow
```

## How to Use
1. **Upload Video**:
   - Click on the "Upload MP4" button to select video files.
   
2. **Set Mask Properties**:
   - Enter the desired width and height for the mask.
   - Choose a color for the mask. Click "Select Color" to use a color picker or choose the black button for a black mask.
   - Specify the X and Y positions of the mask.

3. **Preview**:
   - Click the "Preview" button to see how the mask will look on the video.

4. **Download Processed Video**:
   - Click the "Download" button to process the videos and save them to your chosen output directory.

## Notes
- The application will display error messages during processing.
- The `Video's (x, y):` label is updated to show the dimensions of the video when it is loaded.
- Ensure that the selected color is in hexadecimal format (e.g., `#FFFFFF` for white).

## Example
1. Upload an MP4 video.
2. Set the mask width to 100 and height to 100.
3. Select a color (e.g., #FF5733).
4. Position the mask at the center of the video.
5. Click "Preview" to view the result.
6. Click "Download" to save the final video with the mask applied.

## License
This project is licensed under the MIT License. Feel free to modify and distribute it as needed.

## Acknowledgments
- **MoviePy** for video processing capabilities.
- **Tkinter** for building the GUI.
- **OpenCV** for handling video frames.
