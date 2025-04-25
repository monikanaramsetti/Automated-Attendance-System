import cv2 
import numpy as np
import pandas as pd
from datetime import datetime
import os
import face_recognition
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class AttendanceSystem:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.multiple_faces_alert_shown = False
        self.optimal_distance = 60  # optimal distance in cm
        self.distance_tolerance = 15  # tolerance range in cm
        
        # Initialize student list with attendance status, email addresses, and alert flag
        self.students = {
            "USER_NAME": {"present": False, "time": None, "email": "USERMAIL@gmail.com", "alert_shown": False},
            "USER_NAME": {"present": False, "time": None, "email": "USERMAIL@gmail.com", "alert_shown": False},
            "USER_NAME": {"present": False, "time": None, "email": "USERMAIL@gmail.com", "alert_shown": False},
            "USER_NAME": {"present": False, "time": None, "email": "USERMAIL@gmail.com", "alert_shown": False},
            
        }
        
        # Image paths for face recognition
        self.face_data = {
            "USER_NAME": "IMAGE_PATH",
            "USER_NAME": "IMAGE_PATH",
            "USER_NAME": "IMAGE_PATH",
            "USER_NAME": "IMAGE_PATH",
           
        }
        
        self.attendance_file = "attendance.xlsx"
        self.load_known_faces()
        self.initialize_excel_file()

    def calculate_distance(self, face_height_pixels):
        known_face_height_cm = 20  # average face height in cm
        known_distance_cm = 60     # calibration distance in cm
        focal_length = (face_height_pixels * known_distance_cm) / known_face_height_cm
        distance = (known_face_height_cm * focal_length) / face_height_pixels
        return int(distance)

    def load_known_faces(self):
        print("Loading known faces...")
        for name, path in self.face_data.items():
            if os.path.exists(path):
                image = face_recognition.load_image_file(path)
                encoding = face_recognition.face_encodings(image)
                if encoding:
                    self.known_face_encodings.append(encoding[0])
                    self.known_face_names.append(name)
                    print(f"Loaded face data for {name}")
            else:
                print(f"Warning: Image not found for {name} at {path}")

    def initialize_excel_file(self):
        date_today = datetime.now().strftime("%Y-%m-%d")
        
        df_data = {
            "S.No": range(1, len(self.students) + 1),
            "Name": list(self.students.keys()),
            "Date": [date_today] * len(self.students),
            "Status": ["Absent"] * len(self.students),
            "Time": [""] * len(self.students)
        }
        
        if not os.path.exists(self.attendance_file):
            df = pd.DataFrame(df_data)
            df.to_excel(self.attendance_file, index=False, na_rep='')
            print("Created new attendance sheet")
        else:
            df = pd.read_excel(self.attendance_file, keep_default_na=False)
            today_records = df[df["Date"] == date_today]
            
            if today_records.empty:
                last_sno = df["S.No"].max() if not df.empty else 0
                new_records = pd.DataFrame({
                    "S.No": range(last_sno + 1, last_sno + len(self.students) + 1),
                    "Name": list(self.students.keys()),
                    "Date": [date_today] * len(self.students),
                    "Status": ["Absent"] * len(self.students),
                    "Time": [""] * len(self.students)
                })
                df = pd.concat([df, new_records], ignore_index=True)
                df.to_excel(self.attendance_file, index=False, na_rep='')
                print("Added new attendance records for today")

    def mark_attendance(self, name):
        if name not in self.students:
            print(f"Error: {name} not found in student list")
            return
            
        current_time = datetime.now().strftime("%H:%M:%S")
        date_today = datetime.now().strftime("%Y-%m-%d")
        
        if self.students[name]["present"] and not self.students[name]["alert_shown"]:
            print(f"Attendance already marked for {name}")
            self.students[name]["alert_shown"] = True
            return
        elif self.students[name]["present"]:
            return
            
        self.students[name]["present"] = True
        self.students[name]["time"] = current_time
        
        try:
            df = pd.read_excel(self.attendance_file, keep_default_na=False)
            mask = (df["Date"] == date_today) & (df["Name"] == name)
            df.loc[mask, "Status"] = "Present"
            df.loc[mask, "Time"] = current_time
            df.to_excel(self.attendance_file, index=False, na_rep='')
            print(f"Marked {name} as present at {current_time}")
        except Exception as e:
            print(f"Error updating attendance file: {e}")

    def display_attendance_status(self):
        date_today = datetime.now().strftime("%Y-%m-%d")
        
        print("\n=== Current Attendance Status ===")
        print(f"Date: {date_today}")
        print("\nStudent List:")
        print("-" * 60)
        print(f"{'S.No':<5} {'Name':<15} {'Status':<10} {'Time':<10}")
        print("-" * 60)
        
        present_count = 0
        for idx, (name, data) in enumerate(self.students.items(), 1):
            status = "Present" if data["present"] else "Absent"
            time = data["time"] if data["time"] else "-"
            print(f"{idx:<5} {name:<15} {status:<10} {time:<10}")
            if data["present"]:
                present_count += 1
        
        print("-" * 60)
        print(f"Total Students: {len(self.students)}")
        print(f"Present: {present_count}")
        print(f"Absent: {len(self.students) - present_count}")

    def send_absent_alert(self):
        print("\n=== Sending Absent Alerts ===")
        
        sender_email = "USERMAIL@gmail.com"
        sender_password = "USER PASSKEY"
        
        for name, data in self.students.items():
            if not data["present"]:
                receiver_email = data["email"]
                subject = f"Attendance Alert: {name} Absent"
                body = f"Dear {name},\n\nYou were marked absent today ({datetime.now().strftime('%Y-%m-%d')}). Please contact the instructor if this is an error.\n\nBest regards,\nAttendance System"
                
                message = MIMEMultipart()
                message["From"] = sender_email
                message["To"] = receiver_email
                message["Subject"] = subject
                
                message.attach(MIMEText(body, "plain"))

                try:
                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, receiver_email, message.as_string())
                    server.quit()
                    print(f"Email sent successfully to {name}")
                except Exception as e:
                    print(f"Error sending email to {name}: {e}")

    def start_recognition(self):
        print("Starting face recognition attendance system...")
        video_capture = cv2.VideoCapture(0)
        
        if not video_capture.isOpened():
            print("Error: Could not open camera")
            return
        
        print("\nControls:")
        print("Press 'd' to display current attendance status")
        print("Press 'q' to quit")
        
        while True:
            ret, frame = video_capture.read()
            if not ret:
                print("Failed to capture video")
                break

            # Add optimal distance text in top-left corner
            cv2.putText(frame, f"Optimal Distance: {self.optimal_distance}cm", 
                      (20, 40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_small_frame)
            
            # Add multiple faces warning
            if len(face_locations) > 1:
                warning_text = "WARNING: Multiple Faces Detected!"
                # Draw red background for warning
                cv2.rectangle(frame, (20, 60), (500, 100), (0, 0, 255), -1)
                cv2.putText(frame, warning_text, 
                          (30, 90), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)
            
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                
                # Calculate face height and estimate distance
                face_height = bottom - top
                distance = self.calculate_distance(face_height)
                
                # Determine distance status and color
                if abs(distance - self.optimal_distance) <= self.distance_tolerance:
                    status = "Good Distance"
                    color = (0, 255, 0)  # Green
                elif distance < self.optimal_distance:
                    status = "Move Back"
                    color = (0, 0, 255)  # Red
                else:
                    status = "Move Closer"
                    color = (0, 0, 255)  # Red

                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.5)
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]
                    if status == "Good Distance":
                        self.mark_attendance(name)

                # Draw face rectangle with color based on distance
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                
                # Create filled rectangle for name display
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), 
                          cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)

            cv2.imshow('Attendance System', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('d'):
                self.display_attendance_status()

        video_capture.release()
        cv2.destroyAllWindows()

        print("\nFinal Attendance Status:")
        self.display_attendance_status()
        self.send_absent_alert()

if __name__ == "__main__":
    attendance_system = AttendanceSystem()
    attendance_system.start_recognition()