# Al-Go

Al-Go is a thesis project by ECE students Balla, Saavedra, and Tejano focused on intelligent traffic monitoring. The system detects and tracks pedestrians, people with disabilities (PWDs), and vehicles using AI models deployed on Raspberry Pi devices.

[Computer Vision-Based Real-Time Pedestrian Density Monitoring for Traffic Signal Control Manuscript.pdf](https://github.com/user-attachments/files/20382916/Computer.Vision-Based.Real-Time.Pedestrian.Density.Monitoring.for.Traffic.Signal.Control.Manuscript.pdf)

## Project Structure

- **Pedestrian.py**  
  Detects and tracks pedestrians and PWDs using a trained model and tracking logic. Differentiates between pedestrians and passerby.

- **Vehicle.py**  
  Performs zone-based vehicle counting with defined areas to monitor traffic flow.

- **Program.py**  
  Manages Raspberry Pi cameras, captures frames, processes them through detection models, and sends detection data via serial communication.

## Features

- Real-time pedestrian and vehicle detection  
- Differentiation of PWDs using specialized models  
- Zone-based vehicle counting  
- Multi-threaded camera handling  
- Serial communication for data output

## Requirements

- Python 3.x  
- Degirum AI SDK  
- OpenCV  
- Picamera2  
- libcamera  
- Raspberry Pi with cameras attached

## Usage

1. Connect Raspberry Pi cameras and serial devices.  
2. Install required dependencies.  
3. Run `Program.py` to start detection and data transmission.

## Authors

- Balla  
- Saavedra  
- Tejano

