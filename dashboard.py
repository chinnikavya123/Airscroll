import cv2
import customtkinter as ctk
import pyautogui
import threading
import time
import math
from PIL import Image, ImageTk
from collections import deque
from hand_tracking import HandTracker
from content_launcher import open_website, select_pdf


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
pyautogui.FAILSAFE = True


class AirScrollDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AirScroll | Gesture Control")
        self.geometry("1250x850")
        self.minsize(1080, 720)

        self.is_running = False
        self.paused = False
        self.scroll_speed = 100
        self.camera_index = 0
        self.previous_y = None
        self.previous_pinch = False
        self.smooth_positions = deque(maxlen=4)
        self.gesture_history = deque(maxlen=4)
        self.scroll_accumulator = 0.0
        self.scroll_threshold = 7.0
        self.scroll_events = 0
        self.last_scroll_time = 0.0
        self.preview_labels = []
        self.hand_detail_labels = {}
        self.nav_buttons = {}
        self.current_page = "Overview"
        self.camera_thread = None

        self.protocol("WM_DELETE_WINDOW", self.close_app)
        self.create_interface()
        self.show_page("Overview")

    # ------------------------- MAIN INTERFACE -------------------------
    def create_interface(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=235, corner_radius=0, fg_color="#111827")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(
            self.sidebar, text="✋ AirScroll", font=("Segoe UI", 27, "bold"),
            text_color="#60A5FA"
        ).pack(pady=(32, 5))
        ctk.CTkLabel(
            self.sidebar, text="GESTURE CONTROL SYSTEM", font=("Segoe UI", 10),
            text_color="#94A3B8"
        ).pack(pady=(0, 30))

        for page, icon in [
            ("Overview", "▣"),
            ("Hand Tracking", "✋"),
            ("Scroll Controls", "↕"),
            ("Settings", "⚙")
        ]:
            button = ctk.CTkButton(
                self.sidebar,
                text=f"{icon}   {page}",
                height=44,
                corner_radius=9,
                anchor="w",
                font=("Segoe UI", 13),
                fg_color="transparent",
                hover_color="#263449",
                text_color="#CBD5E1",
                command=lambda p=page: self.show_page(p)
            )
            button.pack(fill="x", padx=14, pady=5)
            self.nav_buttons[page] = button

        ctk.CTkFrame(self.sidebar, fg_color="transparent").pack(expand=True, fill="both")

        privacy = ctk.CTkFrame(self.sidebar, fg_color="#1E293B", corner_radius=12)
        privacy.pack(fill="x", padx=14, pady=18)
        ctk.CTkLabel(
            privacy, text="PRIVACY FIRST", font=("Segoe UI", 11, "bold"),
            text_color="#60A5FA"
        ).pack(anchor="w", padx=12, pady=(12, 5))
        ctk.CTkLabel(
            privacy, text="Camera processing happens\nlocally on your device.",
            font=("Segoe UI", 11), text_color="#CBD5E1", justify="left"
        ).pack(anchor="w", padx=12, pady=(0, 12))

        self.main = ctk.CTkFrame(self, fg_color="#0B1120", corner_radius=0)
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(1, weight=1)

        self.header = ctk.CTkFrame(self.main, fg_color="transparent")
        self.header.grid(row=0, column=0, sticky="ew", padx=28, pady=(18, 12))
        self.header.grid_columnconfigure(0, weight=1)

        header_top = ctk.CTkFrame(self.header, fg_color="transparent")
        header_top.pack(fill="x")

        self.page_title = ctk.CTkLabel(
            header_top, text="Overview", font=("Segoe UI", 27, "bold"),
            text_color="#F8FAFC"
        )
        self.page_title.pack(side="left", anchor="w")

        # One shared camera control area stays visible on every page.
        global_controls = ctk.CTkFrame(
            header_top, fg_color="#111827", corner_radius=10
        )
        global_controls.pack(side="right", padx=(12, 0))

        self.global_status_label = ctk.CTkLabel(
            global_controls, text="● INACTIVE", font=("Segoe UI", 10, "bold"),
            text_color="#F87171"
        )
        self.global_status_label.pack(side="left", padx=(12, 8), pady=8)

        self.global_start_button = ctk.CTkButton(
            global_controls, text="▶ START", width=92, height=32,
            font=("Segoe UI", 11, "bold"),
            command=self.start_tracking
        )
        self.global_start_button.pack(side="left", padx=4, pady=6)

        self.global_stop_button = ctk.CTkButton(
            global_controls, text="■ STOP", width=82, height=32,
            font=("Segoe UI", 11, "bold"),
            fg_color="#991B1B", hover_color="#7F1D1D",
            command=self.stop_tracking, state="disabled"
        )
        self.global_stop_button.pack(side="left", padx=(4, 8), pady=6)

        self.page_subtitle = ctk.CTkLabel(
            self.header, text="Control your computer using natural hand gestures.",
            font=("Segoe UI", 13), text_color="#94A3B8"
        )
        self.page_subtitle.pack(anchor="w", pady=(4, 0))

        self.page_host = ctk.CTkScrollableFrame(
            self.main, fg_color="transparent", corner_radius=0
        )
        self.page_host.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 18))
        self.page_host.grid_columnconfigure(0, weight=1)

    def show_page(self, page):
        self.current_page = page
        for child in self.page_host.winfo_children():
            child.destroy()
        for name, button in self.nav_buttons.items():
            button.configure(
                fg_color="#1D4ED8" if name == page else "transparent",
                font=("Segoe UI", 13, "bold" if name == page else "normal")
            )

        descriptions = {
            "Overview": "Control your computer using natural hand gestures.",
            "Hand Tracking": "Monitor your camera and see which hand gesture AirScroll detects.",
            "Scroll Controls": "Adjust scrolling sensitivity and monitor scroll activity.",
            "Settings": "Configure the camera and learn how to use AirScroll."
        }
        self.page_title.configure(text=page)
        self.page_subtitle.configure(text=descriptions[page])

        if page == "Overview":
            self.build_overview_page()
        elif page == "Hand Tracking":
            self.build_hand_tracking_page()
        elif page == "Scroll Controls":
            self.build_scroll_controls_page()
        else:
            self.build_settings_page()

    # ------------------------- REUSABLE UI -------------------------
    def make_card(self, parent, title, row=None, column=0, colspan=1):
        card = ctk.CTkFrame(parent, fg_color="#111827", corner_radius=15)
        if row is not None:
            card.grid(row=row, column=column, columnspan=colspan, sticky="nsew", padx=8, pady=8)
        ctk.CTkLabel(
            card, text=title, font=("Segoe UI", 13, "bold"), text_color="#CBD5E1"
        ).pack(anchor="w", padx=16, pady=(15, 10))
        return card

    def register_preview(self, label):
        self.preview_labels.append(label)

    def create_camera_preview(self, parent, height=390):
        label = ctk.CTkLabel(
            parent,
            text="Camera is inactive\n\nClick START AIRSCROLL to begin tracking",
            font=("Segoe UI", 15), text_color="#94A3B8",
            fg_color="#020617", corner_radius=12, height=height
        )
        label.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        self.register_preview(label)
        return label

    def create_start_stop_buttons(self, parent):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=(8, 5))
        self.start_button = ctk.CTkButton(
            row, text="▶  START AIRSCROLL", height=43,
            fg_color="#2563EB", hover_color="#1D4ED8",
            font=("Segoe UI", 12, "bold"), command=self.start_tracking
        )
        self.start_button.pack(fill="x", pady=(0, 8))
        self.stop_button = ctk.CTkButton(
            row, text="■  STOP", height=40,
            fg_color="#991B1B", hover_color="#7F1D1D",
            command=self.stop_tracking, state="disabled"
        )
        self.stop_button.pack(fill="x")

    def create_speed_control(self, parent):
        ctk.CTkLabel(
            parent, text="SCROLL SPEED", font=("Segoe UI", 12, "bold"),
            text_color="#CBD5E1"
        ).pack(anchor="w", padx=18, pady=(18, 4))
        self.speed_value_label = ctk.CTkLabel(
            parent, text=f"{self.scroll_speed}%", font=("Segoe UI", 20, "bold"),
            text_color="#60A5FA"
        )
        self.speed_value_label.pack(anchor="w", padx=18)
        self.speed_slider = ctk.CTkSlider(
            parent, from_=10, to=200, number_of_steps=19,
            command=self.update_speed
        )
        self.speed_slider.set(self.scroll_speed)
        self.speed_slider.pack(fill="x", padx=18, pady=(8, 15))

    def create_status_labels(self, parent):
        self.status_label = ctk.CTkLabel(
            parent, text=self.system_status_text(), font=("Segoe UI", 12, "bold"),
            text_color="#4ADE80" if self.is_running else "#F87171"
        )
        self.status_label.pack(anchor="w", padx=18, pady=(10, 5))
        self.gesture_label = ctk.CTkLabel(
            parent, text="Gesture: None detected", font=("Segoe UI", 12),
            text_color="#CBD5E1"
        )
        self.gesture_label.pack(anchor="w", padx=18, pady=5)
        self.pause_label = ctk.CTkLabel(
            parent, text="Scrolling: Inactive", font=("Segoe UI", 12),
            text_color="#94A3B8"
        )
        self.pause_label.pack(anchor="w", padx=18, pady=5)
        self.scroll_count_label = ctk.CTkLabel(
            parent, text=f"Scroll actions: {self.scroll_events}",
            font=("Segoe UI", 11), text_color="#94A3B8"
        )
        self.scroll_count_label.pack(anchor="w", padx=18, pady=(5, 12))

    def system_status_text(self):
        return "●  SYSTEM ACTIVE" if self.is_running else "●  SYSTEM INACTIVE"

    # ------------------------- OVERVIEW PAGE -------------------------
    def build_overview_page(self):
        self.page_host.grid_columnconfigure(0, weight=3)
        self.page_host.grid_columnconfigure(1, weight=2)

        left = ctk.CTkFrame(self.page_host, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew")
        right = ctk.CTkFrame(self.page_host, fg_color="transparent")
        right.grid(row=0, column=1, sticky="nsew")

        camera_card = self.make_card(left, "LIVE CAMERA PREVIEW")
        camera_card.pack(fill="both", expand=True, padx=8, pady=8)
        self.create_camera_preview(camera_card, 360)

        controls = self.make_card(right, "CONTROL CENTER")
        controls.pack(fill="x", padx=8, pady=8)
        self.create_status_labels(controls)
        ctk.CTkLabel(
            controls,
            text="Use the camera controls in the top bar to start or stop AirScroll.\n"
                 "Adjust scrolling speed from the Scroll Controls section.",
            font=("Segoe UI", 11), text_color="#94A3B8",
            justify="left", wraplength=280
        ).pack(anchor="w", padx=18, pady=(8, 15))

        launcher = self.make_card(self.page_host, "CONTENT LAUNCHER")
        launcher.grid(row=1, column=0, columnspan=2, sticky="ew", padx=8, pady=8)
        launcher.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            launcher, text="Open a website in your browser or choose a PDF from your computer.",
            font=("Segoe UI", 11), text_color="#94A3B8"
        ).pack(anchor="w", padx=16, pady=(0, 10))
        url_row = ctk.CTkFrame(launcher, fg_color="transparent")
        url_row.pack(fill="x", padx=14)
        self.url_entry = ctk.CTkEntry(
            url_row, height=40, placeholder_text="Paste a website URL (e.g. https://www.google.com)"
        )
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        ctk.CTkButton(
            url_row, text="🌐  OPEN WEBSITE", width=160, height=40,
            command=self.launch_website
        ).pack(side="left")
        ctk.CTkButton(
            launcher, text="📄  SELECT PDF", width=160, height=38,
            fg_color="#7C3AED", hover_color="#6D28D9",
            command=self.launch_pdf
        ).pack(anchor="w", padx=14, pady=10)
        self.launcher_status = ctk.CTkLabel(
            launcher, text="Ready to open a website or PDF.",
            font=("Segoe UI", 11), text_color="#94A3B8", anchor="w"
        )
        self.launcher_status.pack(fill="x", padx=16, pady=(0, 12))

    # ------------------------- HAND TRACKING PAGE -------------------------
    def build_hand_tracking_page(self):
        self.page_host.grid_columnconfigure(0, weight=3)
        self.page_host.grid_columnconfigure(1, weight=2)

        camera_card = self.make_card(self.page_host, "LIVE HAND TRACKING")
        camera_card.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        self.create_camera_preview(camera_card, 480)

        info = self.make_card(self.page_host, "DETECTION DETAILS")
        info.grid(row=0, column=1, sticky="new", padx=8, pady=8)
        self.create_status_labels(info)

        metrics = ctk.CTkFrame(info, fg_color="#1E293B", corner_radius=11)
        metrics.pack(fill="x", padx=14, pady=(12, 8))

        ctk.CTkLabel(
            metrics, text="LIVE HAND INFORMATION",
            font=("Segoe UI", 11, "bold"), text_color="#60A5FA"
        ).pack(anchor="w", padx=12, pady=(12, 8))

        metric_rows = [
            ("hand", "Hand detected"),
            ("count", "Hands in frame"),
            ("side", "Detected hand"),
            ("confidence", "Classification confidence"),
            ("position", "Index fingertip (X, Y)"),
            ("pinch", "Thumb-index distance")
        ]

        self.hand_detail_labels = {}
        for key, title in metric_rows:
            row = ctk.CTkFrame(metrics, fg_color="transparent")
            row.pack(fill="x", padx=12, pady=4)
            ctk.CTkLabel(
                row, text=title, font=("Segoe UI", 11),
                text_color="#94A3B8"
            ).pack(side="left")
            value = ctk.CTkLabel(
                row, text="Waiting...", font=("Segoe UI", 11, "bold"),
                text_color="#E2E8F0"
            )
            value.pack(side="right")
            self.hand_detail_labels[key] = value

        guide = ctk.CTkFrame(info, fg_color="#1E293B", corner_radius=11)
        guide.pack(fill="x", padx=14, pady=(8, 14))
        ctk.CTkLabel(
            guide, text="SUPPORTED GESTURES",
            font=("Segoe UI", 11, "bold"), text_color="#60A5FA"
        ).pack(anchor="w", padx=12, pady=(12, 6))
        ctk.CTkLabel(
            guide,
            text="☝  Index finger only  —  Scroll\n"
                 "👌  Thumb + index pinch  —  Pause / Resume\n"
                 "✋  Other hand poses  —  No scrolling",
            font=("Segoe UI", 11), text_color="#CBD5E1",
            justify="left"
        ).pack(anchor="w", padx=12, pady=(0, 12))

    # ------------------------- SCROLL CONTROLS PAGE -------------------------
    def build_scroll_controls_page(self):
        self.page_host.grid_columnconfigure(0, weight=1)
        controls = self.make_card(self.page_host, "SCROLL CONFIGURATION")
        controls.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        self.create_speed_control(controls)
        ctk.CTkLabel(
            controls,
            text="Move your index finger upward to scroll up and downward to scroll down.\n"
                 "Higher speed increases both scrolling sensitivity and the number of scroll lines per movement.",
            font=("Segoe UI", 12), text_color="#94A3B8", justify="left"
        ).pack(anchor="w", padx=18, pady=(0, 15))

        activity = self.make_card(self.page_host, "SCROLL ACTIVITY")
        activity.grid(row=1, column=0, sticky="ew", padx=8, pady=8)
        self.scroll_activity_label = ctk.CTkLabel(
            activity, text=f"Scroll actions triggered: {self.scroll_events}",
            font=("Segoe UI", 17, "bold"), text_color="#60A5FA"
        )
        self.scroll_activity_label.pack(anchor="w", padx=18, pady=(5, 8))
        self.scroll_direction_label = ctk.CTkLabel(
            activity, text="Last direction: Not started", font=("Segoe UI", 12),
            text_color="#CBD5E1"
        )
        self.scroll_direction_label.pack(anchor="w", padx=18, pady=(0, 15))


    # ------------------------- SETTINGS PAGE -------------------------
    def build_settings_page(self):
        self.page_host.grid_columnconfigure(0, weight=1)
        camera = self.make_card(self.page_host, "CAMERA SETTINGS")
        camera.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        ctk.CTkLabel(
            camera, text="Camera device index", font=("Segoe UI", 12),
            text_color="#CBD5E1"
        ).pack(anchor="w", padx=18, pady=(5, 5))
        self.camera_index_entry = ctk.CTkEntry(camera, width=150, height=36)
        self.camera_index_entry.insert(0, str(self.camera_index))
        self.camera_index_entry.pack(anchor="w", padx=18, pady=(0, 8))
        ctk.CTkButton(
            camera, text="SAVE CAMERA INDEX", width=180,
            command=self.save_camera_index
        ).pack(anchor="w", padx=18, pady=(0, 15))

        guide = self.make_card(self.page_host, "HOW TO USE AIRSCROLL")
        guide.grid(row=1, column=0, sticky="ew", padx=8, pady=8)
        ctk.CTkLabel(
            guide,
            text="1. Start AirScroll and allow the camera to detect your hand.\n"
                 "2. Raise only your index finger; keep the other fingers folded.\n"
                 "3. Move your index finger up or down to scroll.\n"
                 "4. Pinch your thumb and index finger once to pause or resume.\n"
                 "5. Keep the mouse pointer over the webpage or PDF while scrolling.\n\n"
                 "Tip: Keep your hand visible, well-lit and facing the camera.",
            font=("Segoe UI", 12), text_color="#CBD5E1", justify="left"
        ).pack(anchor="w", padx=18, pady=(5, 16))

        reset = self.make_card(self.page_host, "RESET")
        reset.grid(row=2, column=0, sticky="ew", padx=8, pady=8)
        ctk.CTkButton(
            reset, text="RESET SCROLL COUNTER", width=200,
            fg_color="#475569", hover_color="#334155",
            command=self.reset_scroll_counter
        ).pack(anchor="w", padx=18, pady=(5, 15))

    # ------------------------- LAUNCHER -------------------------
    def show_launcher_status(self, message, success):
        if hasattr(self, "launcher_status") and self.launcher_status.winfo_exists():
            self.launcher_status.configure(
                text=message, text_color="#4ADE80" if success else "#F87171"
            )

    def launch_website(self):
        success, message = open_website(self.url_entry.get())
        self.show_launcher_status(message, success)

    def launch_pdf(self):
        success, message = select_pdf()
        self.show_launcher_status(message, success)

    # ------------------------- SETTINGS / SPEED -------------------------
    def update_speed(self, value):
        self.scroll_speed = int(float(value))
        if hasattr(self, "speed_value_label") and self.speed_value_label.winfo_exists():
            self.speed_value_label.configure(text=f"{self.scroll_speed}%")

    def save_camera_index(self):
        try:
            value = int(self.camera_index_entry.get().strip())
            if value < 0:
                raise ValueError
            if self.is_running:
                self.stop_tracking()
            self.camera_index = value
            self.show_message("Camera index saved. Restart tracking to use it.")
        except ValueError:
            self.show_message("Enter a valid camera index (0, 1, 2...).", error=True)

    def show_message(self, message, error=False):
        dialog = ctk.CTkToplevel(self)
        dialog.title("AirScroll")
        dialog.geometry("390x150")
        dialog.transient(self)
        dialog.grab_set()
        ctk.CTkLabel(
            dialog, text=message, wraplength=340, justify="center",
            font=("Segoe UI", 12), text_color="#F87171" if error else "#CBD5E1"
        ).pack(expand=True, padx=20, pady=15)
        ctk.CTkButton(dialog, text="OK", width=100, command=dialog.destroy).pack(pady=(0, 15))

    def reset_scroll_counter(self):
        self.scroll_events = 0
        self.refresh_status_widgets()

    # ------------------------- TRACKING -------------------------
    def start_tracking(self):
        if self.is_running:
            return
        self.is_running = True
        self.paused = False
        self.previous_y = None
        self.previous_pinch = False
        self.smooth_positions.clear()
        self.gesture_history.clear()
        self.scroll_accumulator = 0.0
        self.last_scroll_time = 0.0
        self.refresh_status_widgets()
        self.camera_thread = threading.Thread(target=self.camera_loop, daemon=True)
        self.camera_thread.start()

    def stop_tracking(self):
        self.is_running = False
        self.paused = False
        self.previous_y = None
        self.previous_pinch = False
        self.scroll_accumulator = 0.0
        self.smooth_positions.clear()
        self.gesture_history.clear()
        self.refresh_status_widgets()
        self.update_hand_details({
            "hand": "—",
            "count": "—",
            "side": "—",
            "confidence": "—",
            "position": "—",
            "pinch": "—"
        })
        for label in self.preview_labels:
            if label.winfo_exists():
                label.configure(
                    image=None,
                    text="Camera is inactive\n\nClick START AIRSCROLL to begin tracking"
                )
                label.image = None

    def is_index_finger_gesture(self, results):
        """Detect an upright index-only pose using MediaPipe finger landmarks."""
        if not results or not results.multi_hand_landmarks:
            return False
        points = results.multi_hand_landmarks[0].landmark

        # Index should be extended: tip above its PIP joint.
        index_extended = points[8].y < points[6].y - 0.025

        # Remaining fingers should be folded. The small margin tolerates jitter.
        middle_folded = points[12].y > points[10].y - 0.005
        ring_folded = points[16].y > points[14].y - 0.005
        pinky_folded = points[20].y > points[18].y - 0.005

        return index_extended and middle_folded and ring_folded and pinky_folded

    def camera_loop(self):
        cap = None
        tracker = None
        try:
            cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
            if not cap.isOpened():
                cap.release()
                cap = cv2.VideoCapture(self.camera_index)
            tracker = HandTracker()

            if not cap.isOpened():
                self.after(0, lambda: self.show_message("Could not open the selected camera. Check the camera index in Settings.", error=True))
                return

            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

            while self.is_running:
                ok, frame = cap.read()
                if not ok:
                    time.sleep(0.02)
                    continue

                frame = cv2.flip(frame, 1)
                frame, results = tracker.process_frame(frame)
                position = tracker.get_index_finger_position(results, frame.shape)
                pinch_distance = tracker.get_pinch_distance(results)
                raw_index = self.is_index_finger_gesture(results)

                hand_count = (
                    len(results.multi_hand_landmarks)
                    if results and results.multi_hand_landmarks else 0
                )
                hand_side = "—"
                hand_confidence = "—"
                if hand_count and results.multi_handedness:
                    classification = results.multi_handedness[0].classification[0]
                    hand_side = classification.label
                    hand_confidence = f"{classification.score * 100:.1f}%"

                fingertip_text = (
                    f"{position[0]}, {position[1]}" if position else "—"
                )
                pinch_text = (
                    f"{pinch_distance:.3f}" if pinch_distance is not None else "—"
                )
                hand_details = {
                    "hand": "Yes" if hand_count else "No",
                    "count": str(hand_count),
                    "side": hand_side,
                    "confidence": hand_confidence,
                    "position": fingertip_text,
                    "pinch": pinch_text
                }
                self.gesture_history.append(raw_index)
                index_gesture = len(self.gesture_history) >= 3 and sum(self.gesture_history) >= 3

                # Toggle once when pinch begins; wait for fingers to separate before re-arming.
                if pinch_distance is not None:
                    if not self.previous_pinch and pinch_distance < 0.045:
                        self.previous_pinch = True
                        self.paused = not self.paused
                        self.previous_y = None
                        self.scroll_accumulator = 0.0
                        self.smooth_positions.clear()
                    elif self.previous_pinch and pinch_distance > 0.065:
                        self.previous_pinch = False
                else:
                    self.previous_pinch = False

                direction_text = "Waiting for movement"
                if index_gesture and position and not self.paused:
                    y = position[1]
                    self.smooth_positions.append(y)
                    smooth_y = sum(self.smooth_positions) / len(self.smooth_positions)

                    if self.previous_y is not None:
                        delta = self.previous_y - smooth_y
                        if abs(delta) >= 0.6:
                            self.scroll_accumulator += delta

                        # Higher speed means both a lower movement threshold and
                        # more wheel steps for the same detected finger movement.
                        speed_ratio = (self.scroll_speed - 10) / 190.0
                        threshold = 7.0 - (speed_ratio * 5.8)  # 7 px at 10%, about 1.2 px at 200%
                        if abs(self.scroll_accumulator) >= threshold:
                            now = time.monotonic()
                            if now - self.last_scroll_time >= 0.02:
                                direction = 1 if self.scroll_accumulator > 0 else -1
                                movement_steps = max(
                                    1,
                                    min(6, int(abs(self.scroll_accumulator) / threshold))
                                )
                                speed_multiplier = 1 + int(self.scroll_speed / 10)
                                wheel_steps = movement_steps * speed_multiplier

                                pyautogui.scroll(direction * wheel_steps)
                                self.scroll_events += 1
                                self.last_scroll_time = now
                                direction_text = "Up" if direction > 0 else "Down"
                                self.scroll_accumulator -= direction * movement_steps * threshold
                    self.previous_y = smooth_y
                else:
                    self.previous_y = None
                    self.scroll_accumulator = 0.0
                    self.smooth_positions.clear()

                if self.previous_pinch:
                    gesture = "Pinch"
                elif index_gesture:
                    gesture = "Index finger"
                elif results and results.multi_hand_landmarks:
                    gesture = "Other gesture"
                else:
                    gesture = "No hand"

                status = "Paused" if self.paused else ("Active" if self.is_running else "Inactive")
                cv2.putText(frame, f"AirScroll: {status}", (12, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.65,
                            (0, 0, 255) if self.paused else (0, 255, 0), 2)
                cv2.putText(frame, f"Gesture: {gesture}", (12, 56), cv2.FONT_HERSHEY_SIMPLEX, 0.58,
                            (255, 255, 255), 2)
                cv2.putText(frame, f"Scroll events: {self.scroll_events}", (12, 84), cv2.FONT_HERSHEY_SIMPLEX,
                            0.55, (255, 255, 0), 2)

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(rgb)
                image.thumbnail((720, 500))
                photo = ImageTk.PhotoImage(image)
                self.after(
                    0,
                    lambda p=photo, g=gesture, s=status, d=direction_text, h=hand_details:
                        self.update_tracking_ui(p, g, s, d, h)
                )

        except pyautogui.FailSafeException:
            self.after(0, self.stop_tracking)
        except Exception as error:
            print("AirScroll tracking error:", error)
            try:
                self.after(0, lambda e=str(error): self.show_message(f"Tracking error: {e}", error=True))
            except Exception:
                pass
        finally:
            if cap is not None:
                cap.release()
            if tracker is not None:
                tracker.close()
            try:
                self.after(0, self.tracking_finished)
            except Exception:
                pass

    def update_hand_details(self, details):
        if not self.hand_detail_labels:
            return

        for key, value in details.items():
            widget = self.hand_detail_labels.get(key)
            if widget is not None and widget.winfo_exists():
                widget.configure(text=value)

    def update_tracking_ui(self, photo, gesture, status, direction, hand_details=None):
        if not self.winfo_exists():
            return
        for label in self.preview_labels:
            if label.winfo_exists():
                label.configure(image=photo, text="")
                label.image = photo
        self.refresh_status_widgets(gesture, status, direction)
        if hand_details is not None:
            self.update_hand_details(hand_details)

    def refresh_status_widgets(self, gesture=None, status=None, direction=None):
        if hasattr(self, "global_status_label") and self.global_status_label.winfo_exists():
            self.global_status_label.configure(
                text="● ACTIVE" if self.is_running else "● INACTIVE",
                text_color="#4ADE80" if self.is_running else "#F87171"
            )
        if hasattr(self, "global_start_button") and self.global_start_button.winfo_exists():
            self.global_start_button.configure(
                state="disabled" if self.is_running else "normal"
            )
        if hasattr(self, "global_stop_button") and self.global_stop_button.winfo_exists():
            self.global_stop_button.configure(
                state="normal" if self.is_running else "disabled"
            )

        for name in ("status_label",):
            widget = getattr(self, name, None)
            if widget is not None and widget.winfo_exists():
                widget.configure(
                    text=self.system_status_text(),
                    text_color="#4ADE80" if self.is_running else "#F87171"
                )
        if gesture is not None and hasattr(self, "gesture_label") and self.gesture_label.winfo_exists():
            self.gesture_label.configure(text=f"Gesture: {gesture}")
        if status is not None and hasattr(self, "pause_label") and self.pause_label.winfo_exists():
            self.pause_label.configure(
                text=f"Scrolling: {status}",
                text_color="#4ADE80" if status == "Active" else "#F87171"
            )
        if hasattr(self, "scroll_count_label") and self.scroll_count_label.winfo_exists():
            self.scroll_count_label.configure(text=f"Scroll actions: {self.scroll_events}")
        if hasattr(self, "scroll_activity_label") and self.scroll_activity_label.winfo_exists():
            self.scroll_activity_label.configure(text=f"Scroll actions triggered: {self.scroll_events}")
        if direction and hasattr(self, "scroll_direction_label") and self.scroll_direction_label.winfo_exists():
            self.scroll_direction_label.configure(text=f"Last direction: {direction}")

    def tracking_finished(self):
        if self.is_running:
            self.is_running = False
        self.refresh_status_widgets()

    def close_app(self):
        self.is_running = False
        self.destroy()


if __name__ == "__main__":
    app = AirScrollDashboard()
    app.mainloop()
