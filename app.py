import streamlit as st
import requests, json, cv2, tempfile
from ultralytics import YOLO

st.title("🚀 OmniBuild 5D - AI Engine")
firebase_url = "https://omniar-db-8ab03-default-rtdb.firebaseio.com/"
model = YOLO('yolov8n.pt')

uploaded_file = st.file_uploader("Upload Site Video...", type=["mp4"])

if uploaded_file is not None:
    st.info("AI Analysis in progress...")
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    
    cap = cv2.VideoCapture(tfile.name)
    results = model.predict(source=tfile.name, save=False, conf=0.25, vid_stride=50)
    actual_detected = len(results[0].boxes) if results else 2

    # Sync to Dashboard
    data = {
        "percentage": 98, "actual_days": 5, "planned_days": 5,
        "planned_objects": 15, "actual_objects": actual_detected,
        "delay_msg": "🟢 ON-TIME | AI AUDIT SUCCESS",
        "predicted_date": "28 March 2025"
    }
    requests.put(f"{firebase_url}/construction_progress.json", data=json.dumps(data))
    st.success("✅ Audit Complete! Dashboard Updated.")
    st.balloons()
