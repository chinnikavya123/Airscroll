
import cv2
import customtkinter as ctk
import pyautogui
import threading
import math
from PIL import Image, ImageTk
from collections import deque
from hand_tracking import HandTracker


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

pyautogui.FAILSAFE = True


class AirScrollDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AirScroll | Gesture Control")
        self.geometry("1150x720")
        self.minsize(1000, 650)

        self.is_running = False
        self.paused = False
        self.scroll_speed = 35

        self.cap = None
        self.tracker = None
        self.previous_y = None
        self.previous_pinch = False
        self.smooth_positions = deque(maxlen=5)

        self.create_interface()

        self.protocol("WM_DELETE_WINDOW", self.close_app)

    def create_interface(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_area()

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self,
            width=230,
            corner_radius=0,
            fg_color="#111827"
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        logo = ctk.CTkLabel(
            self.sidebar,
            text="✋ AirScroll",
            font=("Segoe UI", 27, "bold"),
            text_color="#60A5FA"
        )
        logo.pack(pady=(35, 8))

        subtitle = ctk.CTkLabel(
            self.sidebar,
            text="GESTURE CONTROL SYSTEM",
            font=("Segoe UI", 10),
            text_color="#94A3B8"
        )
        subtitle.pack(pady=(0, 35))

        self.create_sidebar_item("▣  Overview", True)
        self.create_sidebar_item("✋  Hand Tracking", False)
        self.create_sidebar_item("↕  Scroll Controls", False)
        self.create_sidebar_item("⚙  Settings", False)

        spacer = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )
        spacer.pack(expand=True)

        info = ctk.CTkFrame(
            self.sidebar,
            fg_color="#1E293B",
            corner_radius=12
        )
        info.pack(fill="x", padx=15, pady=20)

        ctk.CTkLabel(
            info,
            text="PRIVACY FIRST",
            font=("Segoe UI", 11, "bold"),
            text_color="#60A5FA"
        ).pack(anchor="w", padx=12, pady=(12, 5))

        ctk.CTkLabel(
            info,
            text="Camera processing happens\nlocally on your device.",
            font=("Segoe UI", 11),
            text_color="#CBD5E1",
            justify="left"
        ).pack(anchor="w", padx=12, pady=(0, 12))

    def create_sidebar_item(self, text, active):
        item = ctk.CTkLabel(
            self.sidebar,
            text=text,
            height=42,
            corner_radius=8,
            anchor="w",
            padx=18,
            font=("Segoe UI", 13, "bold" if active else "normal"),
            fg_color="#1D4ED8" if active else "transparent",
            text_color="white" if active else "#CBD5E1"
        )
        item.pack(fill="x", padx=15, pady=5)

    def create_main_area(self):
        self.main = ctk.CTkFrame(
            self,
            fg_color="#0B1120",
            corner_radius=0
        )
        self.main.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)

        self.main.grid_columnconfigure(0, weight=3)
        self.main.grid_columnconfigure(1, weight=2)
        self.main.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )
        header.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=30,
            pady=(25, 15)
        )

        ctk.CTkLabel(
            header,
            text="Overview",
            font=("Segoe UI", 28, "bold"),
            text_color="#F8FAFC"
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Control your computer using natural hand gestures.",
            font=("Segoe UI", 13),
            text_color="#94A3B8"
        ).pack(anchor="w", pady=(5, 0))

        self.create_preview()
        self.create_controls()

    def create_preview(self):
        self.preview_card = ctk.CTkFrame(
            self.main,
            fg_color="#111827",
            corner_radius=16
        )
        self.preview_card.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(30, 12),
            pady=10
        )

        self.preview_card.grid_rowconfigure(1, weight=1)
        self.preview_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.preview_card,
            text="LIVE CAMERA PREVIEW",
            font=("Segoe UI", 13, "bold"),
            text_color="#CBD5E1"
        ).grid(row=0, column=0, sticky="w", padx=18, pady=15)

        self.camera_label = ctk.CTkLabel(
            self.preview_card,
            text="Camera is currently inactive\n\nClick START to begin tracking",
            font=("Segoe UI", 15),
            text_color="#94A3B8",
            fg_color="#020617",
            corner_radius=12
        )
        self.camera_label.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=15,
            pady=(0, 15)
        )

    def create_controls(self):
        self.control_card = ctk.CTkFrame(
            self.main,
            fg_color="#111827",
            corner_radius=16
        )
        self.control_card.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(12, 30),
            pady=10
        )

        ctk.CTkLabel(
            self.control_card,
            text="CONTROL CENTER",
            font=("Segoe UI", 14, "bold"),
            text_color="#CBD5E1"
        ).pack(anchor="w", padx=20, pady=(20, 15))

        self.status_label = ctk.CTkLabel(
            self.control_card,
            text="●  SYSTEM INACTIVE",
            font=("Segoe UI", 13, "bold"),
            text_color="#F87171"
        )
        self.status_label.pack(anchor="w", padx=20, pady=5)

        self.start_button = ctk.CTkButton(
            self.control_card,
            text="▶  START AIRSCROLL",
            height=45,
            corner_radius=10,
            font=("Segoe UI", 13, "bold"),
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.start_tracking
        )
        self.start_button.pack(fill="x", padx=20, pady=(20, 10))

        self.stop_button = ctk.CTkButton(
            self.control_card,
            text="■  STOP",
            height=42,
            corner_radius=10,
            fg_color="#991B1B",
            hover_color="#7F1D1D",
            command=self.stop_tracking,
            state="disabled"
        )
        self.stop_button.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(
            self.control_card,
            text="SCROLL SPEED",
            font=("Segoe UI", 12, "bold"),
            text_color="#CBD5E1"
        ).pack(anchor="w", padx=20, pady=(30, 5))

        self.speed_value = ctk.CTkLabel(
            self.control_card,
            text="35",
            font=("Segoe UI", 20, "bold"),
            text_color="#60A5FA"
        )
        self.speed_value.pack(anchor="w", padx=20)

        self.speed_slider = ctk.CTkSlider(
            self.control_card,
            from_=5,
            to=100,
            number_of_steps=19,
            command=self.update_speed
        )
        self.speed_slider.set(35)
        self.speed_slider.pack(fill="x", padx=20, pady=(10, 20))

        self.gesture_label = ctk.CTkLabel(
            self.control_card,
            text="Gesture: None detected",
            font=("Segoe UI", 12),
            text_color="#94A3B8"
        )
        self.gesture_label.pack(anchor="w", padx=20, pady=8)

        self.pause_label = ctk.CTkLabel(
            self.control_card,
            text="Scrolling: Inactive",
            font=("Segoe UI", 12),
            text_color="#94A3B8"
        )
        self.pause_label.pack(anchor="w", padx=20, pady=5)

        tips = ctk.CTkFrame(
            self.control_card,
            fg_color="#1E293B",
            corner_radius=12
        )
        tips.pack(fill="x", padx=15, pady=(25, 15))

        ctk.CTkLabel(
            tips,
            text="QUICK GUIDE",
            font=("Segoe UI", 12, "bold"),
            text_color="#60A5FA"
        ).pack(anchor="w", padx=12, pady=(12, 5))

        ctk.CTkLabel(
            tips,
            text="↑  Move finger up: Scroll up\n↓  Move finger down: Scroll down\n👌  Pinch: Pause / Resume",
            font=("Segoe UI", 11),
            text_color="#CBD5E1",
            justify="left"
        ).pack(anchor="w", padx=12, pady=(0, 12))

    def update_speed(self, value):
        self.scroll_speed = int(value)
        self.speed_value.configure(text=str(self.scroll_speed))

    def start_tracking(self):
        if self.is_running:
            return

        self.is_running = True
        self.paused = False
        self.previous_y = None
        self.previous_pinch = False
        self.smooth_positions.clear()

        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.status_label.configure(
            text="●  SYSTEM ACTIVE",
            text_color="#4ADE80"
        )

        threading.Thread(
            target=self.camera_loop,
            daemon=True
        ).start()

    def stop_tracking(self):
        self.is_running = False
        self.paused = False
        self.previous_y = None

        self.status_label.configure(
            text="●  SYSTEM INACTIVE",
            text_color="#F87171"
        )

        self.gesture_label.configure(
            text="Gesture: None detected"
        )

        self.pause_label.configure(
            text="Scrolling: Inactive"
        )

        self.camera_label.configure(
            image=None,
            text="Camera is currently inactive\n\nClick START to begin tracking"
        )

        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")

    def camera_loop(self):
        cap = None
        tracker = None

        try:
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            tracker = HandTracker()

            if not cap.isOpened():
                self.after(0, lambda: self.status_label.configure(
                    text="●  CAMERA ERROR",
                    text_color="#F87171"
                ))
                return

            while self.is_running:
                success, frame = cap.read()

                if not success:
                    break

                frame = cv2.flip(frame, 1)
                frame, results = tracker.process_frame(frame)

                position = tracker.get_index_finger_position(
                    results, frame.shape
                )

                pinch_distance = tracker.get_pinch_distance(results)

                if pinch_distance is not None:
                    current_pinch = pinch_distance < 0.05

                    if current_pinch and not self.previous_pinch:
                        self.paused = not self.paused
                        self.previous_y = None
                        self.smooth_positions.clear()

                    self.previous_pinch = current_pinch
                else:
                    self.previous_pinch = False

                if position and not self.paused:
                    x, y = position
                    self.smooth_positions.append(y)

                    current_y = sum(self.smooth_positions) / len(
                        self.smooth_positions
                    )

                    if self.previous_y is not None:
                        movement = self.previous_y - current_y

                        if abs(movement) > 8:
                            if movement > 0:
                                pyautogui.scroll(self.scroll_speed)
                            else:
                                pyautogui.scroll(-self.scroll_speed)

                    self.previous_y = current_y
                else:
                    self.previous_y = None
                    self.smooth_positions.clear()

                gesture = "Pinch" if (
                    pinch_distance is not None and pinch_distance < 0.05
                ) else ("Index finger" if position else "No hand")

                status = "Paused" if self.paused else "Active"

                cv2.putText(
                    frame,
                    f"AirScroll: {status}",
                    (15, 35),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0) if not self.paused else (0, 0, 255),
                    2
                )

                frame_rgb = cv2.cvtColor(
                    frame, cv2.COLOR_BGR2RGB
                )

                image = Image.fromarray(frame_rgb)
                image.thumbnail((620, 430))

                photo = ImageTk.PhotoImage(image)

                self.after(
                    0,
                    lambda p=photo, g=gesture, s=status: self.update_preview(
                        p, g, s
                    )
                )

        except pyautogui.FailSafeException:
            self.after(0, self.stop_tracking)

        except Exception as error:
            print("AirScroll error:", error)
            self.after(0, self.stop_tracking)

        finally:
            if cap is not None:
                cap.release()

            if tracker is not None:
                tracker.close()

            self.after(0, self.tracking_finished)

    def update_preview(self, photo, gesture, status):
        if not self.winfo_exists():
            return

        self.camera_label.configure(image=photo, text="")
        self.camera_label.image = photo

        self.gesture_label.configure(
            text=f"Gesture: {gesture}"
        )

        self.pause_label.configure(
            text=f"Scrolling: {status}",
            text_color="#4ADE80" if status == "Active" else "#F87171"
        )

    def tracking_finished(self):
        if not self.is_running:
            return

        self.is_running = False
        self.status_label.configure(
            text="●  SYSTEM INACTIVE",
            text_color="#F87171"
        )
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")

    def close_app(self):
        self.is_running = False
        self.destroy()


if __name__ == "__main__":
    app = AirScrollDashboard()
    app.mainloop()
