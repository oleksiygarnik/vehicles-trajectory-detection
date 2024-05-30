# Vehicles Trajectory Detection

This repository provides a comprehensive solution for detecting and tracking vehicle trajectories in video footage. The system utilizes advanced computer vision techniques including YOLO for object detection, Kalman Filter for prediction, and the Hungarian Algorithm for tracking. Additionally, it includes a Flask web application for uploading and processing videos, with results visualized and stored for further analysis.

## Features

- **YOLO Object Detection**: Utilizes the YOLO (You Only Look Once) algorithm for detecting vehicles in each frame of the video.
- **Kalman Filter**: Predicts the future position of detected vehicles, improving the accuracy of tracking.
- **Hungarian Algorithm**: Assigns detected objects to existing tracks, ensuring consistent tracking across frames.
- **Flask Web Application**: Provides a user-friendly interface for uploading videos and viewing results.
- **Event-Driven Architecture**: Uses events to manage video processing tasks and communicate results.
