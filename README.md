# 🖐️ AirScroll

<h1 align="center">AirScroll</h1>

<p align="center">
  <strong>Your hands. Your gestures. Your scrolling experience.</strong>
</p>

<p align="center">
  A touch-free scrolling desktop application powered by Computer Vision.
  <br />
  Control websites and PDF documents using nothing but your hand gestures!
</p>

<p align="center">
  <a href="https://github.com/chinnikavya123/Airscroll">GitHub Repository</a>
</p>

---

## 🚀 What is AirScroll?

Imagine scrolling through a website or reading a PDF without touching your mouse or keyboard.

That's exactly what **AirScroll** makes possible!

AirScroll is a Python-based desktop application that uses your webcam and computer vision to recognize hand gestures and convert them into scrolling actions.

Simply move your index finger to scroll, and use a pinch gesture to pause or resume. It provides a convenient, touch-free way to interact with digital content.

## ✨ Key Features

| Feature | Description |
|---|---|
| 🖐️ Gesture-Based Scrolling | Scroll up and down using index-finger movements |
| 🤏 Pinch Detection | Pause or resume scrolling using a pinch gesture |
| ⚡ Adjustable Speed | Customize scrolling speed to match your preference |
| 🌐 Website Launcher | Enter a URL and open websites directly |
| 📄 PDF Launcher | Browse and open PDF documents |
| 👁️ Live Hand Tracking | View real-time hand landmarks and tracking information |
| 📊 Interactive Dashboard | Explore an organized interface with dedicated sections |
| 🎥 Camera Controls | Start and stop camera tracking whenever needed |

## 🖐️ How Gesture Controls Work

AirScroll translates simple hand movements into scrolling actions.

| Hand Gesture | Action |
|---|---|
| ☝️ Index finger | Activate gesture-based scrolling |
| ⬆️ Move finger upward | Scroll up |
| ⬇️ Move finger downward | Scroll down |
| 🤏 Pinch thumb and index finger | Pause or resume scrolling |

**Tip:** Adjust the scroll speed from the Scroll Controls section to find the movement that feels most comfortable.

## 🖥️ Application Dashboard

AirScroll includes four main sections:

- **Overview:** Launch websites and PDF documents and access the main controls.
- **Hand Tracking:** View the camera preview, detected landmarks, hand information, and gesture metrics.
- **Scroll Controls:** Adjust scrolling speed and monitor scrolling activity.
- **Settings:** Access camera settings, usage instructions, and reset the scroll counter.

## ⚙️ How It Works

AirScroll combines computer vision and desktop automation to make gesture-based scrolling possible.

```text
       Webcam Input
            │
            ▼
    Hand Detection
       (MediaPipe)
            │
            ▼
   Landmark Tracking
       (OpenCV)
            │
            ▼
   Gesture Recognition
            │
       ┌────┴────┐
       ▼         ▼
   Finger      Pinch
  Movement    Detection
       │         │
       ▼         ▼
  Scroll Up/   Pause /
   Scroll     Resume
    Down
       │
       ▼
  PyAutoGUI
       │
       ▼
  Touch-Free
    Scrolling
```

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

## 📥 Installation and Setup

### Prerequisites

- Windows 10 or Windows 11
- Python 3.12 recommended
- A working webcam
- Git

### 1. Clone the repository

```bash
git clone https://github.com/chinnikavya123/Airscroll.git
cd Airscroll
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Launch AirScroll

```bash
python dashboard.py
```

That's it! Your AirScroll desktop application should now launch.

## 📖 Getting Started

Follow these steps to use AirScroll:

1. Launch the application.
2. Open the Overview section.
3. Enter a website URL or select a PDF document.
4. Open the content in your default browser or PDF reader.
5. Position your mouse pointer over the content you want to scroll.
6. Click **Start Camera**.
7. Show your hand to the webcam and use the supported gestures.
8. Adjust scrolling speed whenever needed.
9. Use the pinch gesture to pause or resume scrolling.
10. Click **Stop Camera** when you're finished.

> **Important:** Websites and PDFs open in external applications, not inside AirScroll. The application sends scrolling actions to the window beneath your mouse pointer. Keep your pointer over the webpage or PDF while using hand gestures.

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
├── requirements.txt      # Python dependencies
├── .gitignore
└── README.md
```

## 🔍 Troubleshooting

<details>
<summary><strong>Camera is not detected</strong></summary>

- Check whether your webcam is connected.
- Close other applications that may be using the camera.
- Restart AirScroll and try again.

</details>

<details>
<summary><strong>Scrolling is not working</strong></summary>

- Make sure your mouse pointer is over the webpage or PDF.
- Check whether your hand is detected correctly.
- Ensure the camera is running.
- Adjust the scrolling speed.

</details>

<details>
<summary><strong>Dependencies are missing</strong></summary>

Activate your virtual environment and run:

```bash
python -m pip install -r requirements.txt
```

</details>

## 🔮 Future Enhancements

Here are some ideas planned for future development:

- 🌐 Chrome browser extension.
- ✋ More customizable hand gestures.
- ♿ Additional accessibility-focused controls.
- 🎯 Further improvements to gesture recognition.
- ⚡ Enhanced scrolling responsiveness.

## 👩‍💻 Author

<p align="center">
  <strong>Chinni Kavya Sri</strong>
  <br />
  <a href="https://github.com/chinnikavya123">GitHub Profile</a>
</p>

---

<p align="center">
  Made with ❤️ using Python and Computer Vision.
  <br />
  ⭐ If you like AirScroll, consider giving this repository a star!
</p>
