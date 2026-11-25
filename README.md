# 🖐️ AirScroll – Gesture-Based Touch-Free Scrolling Application

**Control your scrolling with simple hand gestures. Browse smarter. Interact without touching your mouse. 🚀**

---

## 📌 Table of Contents

1. 🌟 About the Project
2. ✨ Features
3. 🖐️ Gesture Controls
4. 🛠️ Tech Stack
5. 📊 Application Modules
6. 🏗️ Project Architecture
7. ⚙️ Getting Started
8. 📖 How to Use
9. 📂 Project Structure
10. 🔍 Troubleshooting
11. 🎯 Future Enhancements
12. 👩‍💻 Project Links & Owner

---

## 🌟 About the Project

**AirScroll** is a Python-based desktop application that enables touch-free scrolling using hand gestures and computer vision.

Imagine browsing websites or reading PDF documents without repeatedly touching your mouse or keyboard. AirScroll makes this possible by using your webcam to detect and track hand movements in real time.

With simple gestures, users can scroll up and down using their index finger and pause or resume scrolling using a pinch gesture.

The application combines **OpenCV, MediaPipe, and PyAutoGUI** to transform natural hand movements into scrolling actions, providing a convenient and interactive browsing experience.

### 💡 Project Objective

The main objective of AirScroll is to make digital interaction more convenient and accessible by introducing a simple gesture-based scrolling system.

---

## ✨ Features

- 🖐️ **Gesture-Based Scrolling:** Scroll up and down using index-finger movements.
- 🤏 **Pinch Detection:** Pause or resume scrolling using a thumb-and-index-finger pinch gesture.
- ⚡ **Adjustable Scroll Speed:** Customize scrolling speed according to your preference.
- 🌐 **Website Launcher:** Enter a website URL and open it directly in your default browser.
- 📄 **PDF Launcher:** Select and open PDF documents in your default PDF reader.
- 👁️ **Live Hand Tracking:** Visualize hand landmarks and monitor real-time tracking information.
- 📊 **Interactive Dashboard:** Navigate through dedicated sections for overview, hand tracking, scroll controls, and settings.
- 🎥 **Camera Controls:** Start and stop webcam tracking whenever required.
- 📈 **Scroll Activity Monitoring:** Monitor scrolling activity and direction.

---

## 🖐️ Gesture Controls

AirScroll recognizes simple hand movements and converts them into scrolling actions.

| Gesture | Action |
|---|---|
| ☝️ Raise index finger | Activate gesture-based scrolling |
| ⬆️ Move index finger upward | Scroll up |
| ⬇️ Move index finger downward | Scroll down |
| 🤏 Pinch thumb and index finger | Pause or resume scrolling |

**Tip:** Adjust the scrolling speed from the Scroll Controls section for a comfortable experience.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| OpenCV | Webcam processing and image handling |
| MediaPipe | Hand detection and landmark tracking |
| NumPy | Numerical operations |
| PyAutoGUI | Mouse and scrolling automation |
| CustomTkinter | Modern desktop user interface |
| Pillow | Image processing and display |

---

## 📊 Application Modules

AirScroll provides an organized dashboard with four main sections.

### 1. 🏠 Overview
- Launch websites using their URLs.
- Browse and open PDF documents.
- Access the main camera controls.
- View the application's current status.

### 2. ✋ Hand Tracking
- View the live webcam preview.
- Track detected hand landmarks.
- Monitor hand detection information.
- View fingertip coordinates and pinch distance.
- Understand the supported gestures.

### 3. ⚡ Scroll Controls
- Adjust scrolling speed using the speed slider.
- Monitor scrolling activity.
- View the current scrolling direction.

### 4. ⚙️ Settings
- Configure the camera index.
- Access usage instructions.
- Reset the scroll activity counter.

---

## 🏗️ Project Architecture

AirScroll follows a computer vision-based workflow to convert hand movements into scrolling actions.

```text
             Webcam Input
                  |
                  ▼
          Hand Detection
             MediaPipe
                  |
                  ▼
          Landmark Tracking
               OpenCV
                  |
                  ▼
          Gesture Recognition
                  |
             ┌────┴────┐
             ▼         ▼
       Finger Movement  Pinch Detection
             |         |
             ▼         ▼
        Scroll Up/    Pause / Resume
         Scroll Down
             |
             ▼
          PyAutoGUI
             |
             ▼
       Touch-Free Scrolling
```

---

## ⚙️ Getting Started

Follow these instructions to set up and run AirScroll on your local machine.

### Prerequisites

- Windows 10 or Windows 11
- Python 3.12 recommended
- A working webcam
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/chinnikavya123/Airscroll.git
```

### 2. Navigate to the Project Directory

```bash
cd Airscroll
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Run the Application

```bash
python dashboard.py
```

That's it! AirScroll should now launch on your desktop.

---

## 📖 How to Use

1. Launch AirScroll.
2. Navigate to the Overview section.
3. Enter a website URL or select a PDF document.
4. Open the selected content.
5. Position your mouse pointer over the webpage or PDF.
6. Click **Start Camera** to begin hand tracking.
7. Show your hand in front of the webcam.
8. Use your index finger to scroll up and down.
9. Use the pinch gesture to pause or resume scrolling.
10. Adjust the scrolling speed whenever needed.
11. Click **Stop Camera** when finished.

**Important:** Websites and PDF documents open in external applications, not inside AirScroll. The application sends scrolling actions to the window beneath your mouse pointer. Keep your pointer over the webpage or PDF while using gestures.

---

## 📂 Project Structure

```text
AirScroll/
│
├── dashboard.py          # Main desktop application
├── hand_tracking.py      # Hand detection and landmark tracking
├── content_launcher.py   # Website and PDF launcher
│
├── webcam_test.py        # Webcam testing utility
├── scroll_test.py        # Scrolling testing utility
├── pinch_test.py         # Pinch detection testing utility
│
├── requirements.txt      # Project dependencies
├── .gitignore
└── README.md
```

---

## 🔍 Troubleshooting

<details>
<summary><strong>📷 Camera is not detected</strong></summary>

- Check whether your webcam is connected and working.
- Close other applications that may be using the webcam.
- Restart AirScroll and try again.

</details>

<details>
<summary><strong>🖐️ Hand gestures are not detected correctly</strong></summary>

- Keep your hand within the webcam's field of view.
- Ensure sufficient lighting.
- Avoid covering your fingers.
- Position your hand clearly in front of the camera.

</details>

<details>
<summary><strong>⬇️ Scrolling is not working</strong></summary>

- Make sure your mouse pointer is positioned over the webpage or PDF.
- Check whether the webcam is running.
- Ensure your hand is being detected.
- Adjust the scrolling speed if necessary.

</details>

<details>
<summary><strong>📦 Dependencies are missing</strong></summary>

Activate your virtual environment and execute:

```bash
python -m pip install -r requirements.txt
```

</details>

---

## 🎯 Future Enhancements

Some improvements planned for future versions:

- 🌐 Chrome browser extension for easier browser integration.
- ✋ Additional customizable hand gestures.
- ♿ More accessibility-focused controls.
- 🎯 Further improvements to gesture recognition accuracy.
- ⚡ Enhanced scrolling responsiveness and interaction.

---

## 👩‍💻 Project Links & Owner

**🌐 Project:** AirScroll – Gesture-Based Touch-Free Scrolling Application

**📂 GitHub Repository:** [AirScroll](https://github.com/chinnikavya123/Airscroll)

**👩‍💻 GitHub Profile:** [@chinnikavya123](https://github.com/chinnikavya123)

---

<p align="center">
  ⭐ If you find AirScroll interesting, consider giving this repository a star!
</p>

<p align="center">
  <strong>🖐️ Move. Gesture. Scroll. Experience touch-free interaction with AirScroll!</strong>
</p>

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/chinnikavya123"><strong>Chinni Kavya Sri</strong></a>
  <br />
  👩‍💻 Owner & Developer of AirScroll
</p>
