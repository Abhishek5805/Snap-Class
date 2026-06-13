import streamlit as st
import pandas as pd

from datetime import datetime

from src.pipelines.voice_pipeline import process_bulk_audio
from src.database.config import supabase
from src.components.dialog_attendence_results import show_attendance_result


@st.dialog("Voice Attendance")
def voice_attendance_dialog(selected_subject_id):

    st.write(
        "Record audio of students saying 'I am present'. "
        "AI will recognize enrolled students from their voice profiles."
    )

    audio_data = st.audio_input("Record classroom audio")

    if st.button("Analyze Audio", width="stretch", type="primary"):

        if audio_data is None:
            st.error("Please record audio before clicking Analyze Audio.")
            return

        with st.spinner("Processing audio data..."):

            try:
                enrolled_res = (
                    supabase.table("subject_students")
                    .select("*, students(*)")
                    .eq("subject_id", selected_subject_id)
                    .execute()
                )

                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning("No students enrolled in this course.")
                    return

                candidates_dict = {}

                for row in enrolled_students:

                    student = row.get("students")

                    if (
                        student
                        and student.get("student_id")
                        and student.get("voice_embedding")
                    ):
                        candidates_dict[
                            int(student["student_id"])
                        ] = student["voice_embedding"]

                if not candidates_dict:
                    st.error(
                        "No enrolled students have voice profiles registered."
                    )
                    return

                audio_bytes = audio_data.read()

                if not audio_bytes:
                    st.error("Recorded audio is empty.")
                    return

                detected_scores = process_bulk_audio(
                    audio_bytes,
                    candidates_dict
                )

                results = []
                attendance_to_log = []

                current_timestamp = datetime.now().strftime(
                    "%Y-%m-%dT%H:%M:%S"
                )

                for row in enrolled_students:

                    student = row["students"]

                    score = float(
                        detected_scores.get(
                            student["student_id"],
                            0.0
                        )
                    )

                    is_present = True if score > 0 else False

                    results.append(
                        {
                            "Name": student["name"],
                            "ID": int(student["student_id"]),
                            "Score": round(score, 3)
                            if is_present
                            else "-",
                            "Status": (
                                "✅ Present"
                                if is_present
                                else "❌ Absent"
                            ),
                        }
                    )

                    attendance_to_log.append(
                        {
                            "student_id": int(student["student_id"]),
                            "subject_id": int(selected_subject_id),
                            "timestamp": str(current_timestamp),
                            "is_present": bool(is_present),
                        }
                    )

                print("Attendance Logs:")
                print(attendance_to_log)

                for log in attendance_to_log:
                    print(
                        "is_present type:",
                        type(log["is_present"])
                    )

                st.session_state.voice_attendance_results = (
                    pd.DataFrame(results),
                    attendance_to_log,
                )

                st.success(
                    f"Voice analysis completed. "
                    f"{len(detected_scores)} student(s) detected."
                )

            except Exception as e:
                st.error(f"Error: {str(e)}")

    if (
        "voice_attendance_results" in st.session_state
        and st.session_state.voice_attendance_results is not None
    ):

        st.divider()

        df_results, logs = (
            st.session_state.voice_attendance_results
        )

        show_attendance_result(df_results, logs)