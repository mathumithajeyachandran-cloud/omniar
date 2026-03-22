import streamlit as st
import requests, json, cv2, tempfile, os
from ultralytics import YOLO

st.set_page_config(page_title="OmniBuild 5D AI", page_icon="🏗️")
st.title("🏗️ OmniBuild 5D - Autonomous AI Engine")

# CONFIG
firebase_url = "https://omniar-db-8ab03-default-rtdb.firebaseio.com/"
model = YOLO('yolov8n.pt')

uploaded_file = st.file_uploader("Upload Site Video for 5D Audit...", type=["mp4"])

if uploaded_file is not None:
    st.warning("🔄 AI Scanning Site... Please wait.")
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    
    # AI Scan (Sampling for speed)
    cap = cv2.VideoCapture(tfile.name)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 10)
    ret, frame = cap.read()
    
    if ret:
        results = model.predict(source=frame, save=False, conf=0.25, verbose=False)
        actual_detected = len(results[0].boxes)
        
        # Logic Calculation
        planned_target = 15
        progress = int((actual_detected / planned_target) * 100)
        if progress > 100: progress = 100
        
        # Data Sync
        data = {
            "percentage": progress,
            "actual_days": 5, "planned_days": 5,
            "planned_objects": planned_target, "actual_objects": actual_detected,
            "delay_msg": "🟢 ON-TIME" if progress >= 90 else f"🔴 {planned_target-actual_detected} UNITS DELAYED",
            "predicted_date": "28 March 2025"
        }
        
        requests.put(f"{firebase_url}/construction_progress.json", data=json.dumps(data))
        st.success(f"✅ AUDIT SUCCESS! Dashboard updated to {progress}%")
        st.balloons()
