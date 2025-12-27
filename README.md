# Smart Scientific Calculator and Virtual Canvas Using Hand Gesture Recognition

## Overview
This project is a vision-based interactive system that combines a **smart scientific calculator**
and a **virtual drawing canvas**, both controlled using **hand gestures**.
The user does not need to touch a keyboard or mouse.
By moving fingers in front of a camera, calculations can be performed and drawings can be made.
The system uses computer vision to recognize hand gestures in real time.

---

## Objective
The objective of this project is to build a **touch-free interactive system** that:
- Performs scientific calculations using hand gestures
- Allows drawing and erasing on a virtual canvas
- Demonstrates modern human–computer interaction
- Reduces physical contact with devices

---

## How the System Works (Simple Explanation)
1. The webcam captures live video input.
2. MediaPipe detects hand landmarks and finger positions.
3. OpenCV processes finger movements in real time.
4. Gestures are mapped to calculator buttons or canvas actions.
5. The system performs calculations or drawing based on the gesture.
6. The output (calculator result or drawing) is displayed on the screen.

---

## Technologies Used
Python  
OpenCV  
MediaPipe  
NumPy  
CvZone  

---

## Features
- Touch-free scientific calculator
- Supports basic and scientific calculations
- Virtual drawing canvas
- Erase and clear functionality
- Real-time hand gesture recognition
- Easy-to-use and modular design

---

## Project Structure
Smart-Scientific-Calculator-Gesture-Control/
|
|-- main.py                  Main execution file
|-- virtual_calculator.py    Calculator operations logic
|-- canvas.py                Virtual canvas and erase functionality
|-- requirements.txt         Project dependencies
|-- README.md                Project documentation

---

## How to Run the Project

Step 1: Clone the repository  
git clone https://github.com/rajkumar-rgb/Smart-Scientific-Calculator-Gesture-Control.git  

Step 2: Go inside the project folder  
cd Smart-Scientific-Calculator-Gesture-Control  

Step 3: Install required libraries  
pip install -r requirements.txt  

Step 4: Run the project  
python main.py  

---

## Requirements
Python 3.9 or above  
Webcam is required  
Good lighting for better gesture detection  

---

## Applications
- Touchless calculator systems
- Virtual drawing and learning tools
- Human–computer interaction demos
- Educational and research applications

---

## License
This project is licensed under the MIT License.
Anyone can use, modify, and share this project.

---

## Author
Raj Kumar Paswan  
B.Tech CSE (AI & ML)

---

## Clone Prompt (For Anyone)
git clone https://github.com/rajkumar-rgb/Smart-Scientific-Calculator-Gesture-Control.git  
cd Smart-Scientific-Calculator-Gesture-Control  
pip install -r requirements.txt  
python main.py  
