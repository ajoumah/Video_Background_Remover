"""Background_Remover

"""

!pip install moviepy opencv-python rembg onnxruntime

from moviepy.editor import VideoFileClip
import cv2
import numpy as np
from rembg import remove, new_session
import onnxruntime as ort # Explicitly import onnxruntime

#  Install necessary libraries first


def remove_background_from_video(input_path, output_path):
    """
    Removes the background from a video file and replaces it with a green screen.

    Args:
        input_path (str): The path to the input video file.
        output_path (str): The path to save the output video file
                           with the background removed and replaced by green.
    """
    try:
        clip = VideoFileClip(input_path)
        # Use the default u2net session for rembg
        session = new_session()

        def process_frame(get_frame, t):
            # Get the frame at time t
            frame = get_frame(t)
            # Convert the frame to bytes (required by rembg)
            frame_bytes = cv2.imencode('.png', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))[1].tobytes()

            # Remove background from the frame
            result_bytes = remove(frame_bytes, session=session)

            # Convert the result back to a NumPy array
            nparr = np.frombuffer(result_bytes, np.uint8)
            result_img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

            # Check if the result has an alpha channel
            if result_img.shape[2] == 4:
                # If it has an alpha channel, blend it with a green background
                # Green color in BGR format (OpenCV uses BGR by default)
                green_background = np.full_like(result_img[:, :, :3], [0, 255, 0], dtype=np.uint8)
                alpha_channel = result_img[:, :, 3] / 255.0
                # Blend the foreground with the green background based on the alpha channel
                blended_frame = (result_img[:, :, :3] * alpha_channel[:, :, np.newaxis] +
                                 green_background * (1 - alpha_channel[:, :, np.newaxis])).astype(np.uint8)
                return blended_frame
            else:
                 # If no alpha channel (likely an error or no foreground detected), return original or handle as needed
                 print(f"Warning: Frame at time {t} did not result in an image with an alpha channel. Returning original frame.")
                 return frame


        # Apply the process_frame function to each frame
        processed_clip = clip.fl(process_frame)

        # Write the processed video to the output path
        processed_clip.write_videofile(output_path, codec='libx264')

        print(f"Background removal completed with green screen. Output saved to: {output_path}")

    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage (replace 'input.mp4' and 'output_green_screen.mp4' with your file paths):
# remove_background_from_video('input.mp4', 'output_green_screen.mp4')

