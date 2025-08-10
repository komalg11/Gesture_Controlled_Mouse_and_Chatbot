# Hand Gesture Mouse Control

This project lets you control your mouse using hand gestures via a webcam.  
It uses **OpenCV**, **cvzone**, and **HandDetector** to track your fingers and map them to mouse actions.

## Features
- **Move Cursor** – Point with index finger to move the mouse.
- **Left Click** – Index + middle finger close together (thumb up).
- **Right Click** – Index + middle finger close together (thumb + pinky up).
- **Scroll Up / Down** – Index + middle finger close together, thumb down (scroll down) or pinky up (scroll up).
- **Double Click** – Thumb up only.

## Requirements
- Python 3.8+
- Webcam

## Installation
```bash
git clone https://github.com/komalg11/Gesture_Controlled_Mouse_and_Chatbot.git
cd Gesture_Controlled_Mouse_and_Chatbot

# Create and activate a virtual environment
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install opencv-python cvzone numpy mouse

