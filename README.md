# 🎥 Video Background Remover with Green Screen Replacement

A powerful Python tool to automatically remove the background from videos and replace it with a green screen — ideal for video editing, virtual production, or training data preparation.

---

## ✨ Features

- ✅ Automatically removes background from video frames  
- ✅ Replaces background with green screen (chroma keying)  
- ✅ Works frame-by-frame using the [Rembg](https://github.com/danielgatis/rembg) model (U-2-Net)  
- ✅ Supports MP4 and other popular formats via `moviepy`  
- ✅ Ideal for:  
  - Video post-production  
  - Machine learning dataset generation  
  - Virtual background replacement  
  - Online streaming overlays  

---

## 🛠️ Installation

Install the required dependencies:

```bash
pip install rembg moviepy opencv-python numpy
Usage
python

from background_remover import remove_background_from_video

remove_background_from_video('input_video.mp4', 'output_green_screen.mp4')
This will:

Load your input video

Remove the background from each frame

Replace the background with a solid green color

Save the processed video to the output path

🧠 How It Works
Reads the video frame-by-frame using moviepy.

Applies the rembg model (U-2-Net) to segment the foreground.

Blends the foreground with a green screen using OpenCV.

Exports the new video with the replaced background.
