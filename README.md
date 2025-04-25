Here's a sample **README.md** file for your Face Recognition-based Attendance System:

---

# Face Recognition Attendance System 📸✅

This project is a Python-based Face Recognition Attendance System that:
- Recognizes faces via webcam using the `face_recognition` library.
- Automatically marks attendance and logs it in an Excel sheet.
- Estimates face distance to ensure proper recognition conditions.
- Sends email alerts to absent students.

---

## 📂 Features

- ✅ **Face recognition-based attendance**
- 📏 **Distance estimation** to ensure optimal recognition accuracy
- 📄 **Excel sheet generation** for daily attendance tracking
- ⚠️ **Alerts for multiple faces**
- 📧 **Email notification** for absent students

---

## 🧰 Requirements

Install the following Python packages:

```bash
pip install opencv-python face_recognition pandas openpyxl numpy
```

To enable email alerts, also install:

```bash
pip install secure-smtplib
```

---

## 📁 Project Structure

```
attendance_system/
│
├── attendance.xlsx           # Automatically generated Excel sheet
├── face_images/              # Folder for face images (you should create this)
├── attendance_system.py      # Main Python script
└── README.md                 # Project documentation
```

---

## 🧑‍🏫 Usage Instructions

1. **Prepare student data:**

   - Replace all `"USER_NAME"` keys with real names.
   - Add corresponding `"email"` for each student.
   - Add actual image paths for each `"USER_NAME"` in the `face_data` dictionary.

   Example:
   ```python
   self.students = {
       "Alice": {"present": False, "time": None, "email": "alice@example.com", "alert_shown": False},
       "Bob": {"present": False, "time": None, "email": "bob@example.com", "alert_shown": False},
   }

   self.face_data = {
       "Alice": "face_images/alice.jpg",
       "Bob": "face_images/bob.jpg",
   }
   ```

2. **Update email credentials:**

   Replace `USERMAIL@gmail.com` and `USER PASSKEY` with the sender email and app-specific password.

   ⚠️ **Tip:** Use [App Passwords](https://support.google.com/accounts/answer/185833) instead of your main Gmail password.

3. **Run the system:**

   ```bash
   python attendance_system.py
   ```

4. **Controls:**
   - Press `d` to display attendance status in the console.
   - Press `q` to quit and send email alerts to absentees.

---

## ⚙️ How It Works

- Captures video from your webcam.
- Detects and encodes faces in real-time.
- Matches the face against known images.
- Checks if the user is at the **optimal distance (60 ± 15 cm)**.
- Marks them present in `attendance.xlsx`.
- Sends an absent alert email to students not detected by the end.

---

## 📌 Notes

- Ensure you have good lighting for accurate face detection.
- For large groups, you might consider extending this to detect multiple faces concurrently.
- Use HD images of students (frontal faces) for better recognition.

---

## 📧 Future Improvements

- Add GUI with Tkinter or PyQt
- Integrate database storage (MySQL or Firebase)
- Schedule automatic attendance sessions

---

## 🛡️ Disclaimer

This system is for educational purposes. Always ensure privacy and ethical handling of biometric data.

---

