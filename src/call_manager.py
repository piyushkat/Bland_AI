import json
import time
import requests
import streamlit as st
from .config import API_KEY, CALL_URL, TRANSCRIPT_FILE

def make_call(phone_number, task=None, doc_query=None):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    greeting_message = "Hello! How are you? How may I assist you today?"
    effective_task = task if task else "Ask me anything about the document."
    
    data = {
        "phone_number": str(phone_number),
        "task": f"{greeting_message} {effective_task}",
        "voice": "June",
        "wait_for_greeting": False,
        "record": True,
        "amd": False,
        "answered_by_enabled": False,
        "noise_cancellation": False,
        "interruption_threshold": 100,
        "block_interruptions": False,
        "max_duration": 12,
        "model": "base",
        "language": "en",
        "background_track": "none",
        "endpoint": "https://api.bland.ai",
        "voicemail_action": "hangup"
    }

    if doc_query:
        data["context"] = doc_query

    try:
        response = requests.post(CALL_URL, headers=headers, json=data)
        if response.status_code == 200:
            call_id = response.json().get("call_id")
            if call_id:
                st.sidebar.success(f"✅ Call initiated successfully! Call ID: {call_id}")
                return call_id
        else:
            st.sidebar.error(f"❌ Error initiating call: {response.status_code} - {response.text}")
    except Exception as e:
        st.sidebar.error(f"❌ Error connecting to Bland AI API: {e}")
    return None

def save_transcript(call_id, transcript):
    transcript_data = {"call_id": call_id, "transcript": transcript}
    try:
        with open(TRANSCRIPT_FILE, "w") as f:
            json.dump(transcript_data, f, indent=4)
    except Exception as e:
        st.error(f"Error saving transcript: {e}")

def get_transcript(call_id):
    transcript_url = f"{CALL_URL}/{call_id}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    final_transcript = []
    seen_entries = set()
    transcript_placeholder = st.empty()

    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            response = requests.get(transcript_url, headers=headers)
            if response.status_code == 200:
                call_data = response.json()
                status = call_data.get("status", "")
                new_transcripts = call_data.get("transcripts", [])

                if new_transcripts:
                    for entry in new_transcripts:
                        entry_tuple = (entry.get("id"), entry.get("user"), entry.get("text"), entry.get("created_at"))
                        if entry_tuple not in seen_entries:
                            seen_entries.add(entry_tuple)
                            final_transcript.append(entry)

                    with transcript_placeholder.container():
                        st.markdown("## 📞 Live Call Transcript")
                        st.markdown(f"**Call ID:** `{call_id}`")
                        st.markdown(f"**Status:** `{status}`")
                        for entry in final_transcript:
                            speaker = entry.get("user", "")
                            message = entry.get("text", "")
                            if speaker == "user":
                                st.markdown(f"""
                                    <div style="background-color: #D6EAF8; padding: 10px; border-radius: 8px; margin-bottom: 5px;">
                                        <b>User:</b> {message}
                                    </div>
                                """, unsafe_allow_html=True)
                            elif speaker == "assistant":
                                st.markdown(f"""
                                    <div style="background-color: #D5F5E3; padding: 10px; border-radius: 8px; margin-bottom: 5px;">
                                        <b>Assistant:</b> {message}
                                    </div>
                                """, unsafe_allow_html=True)

                if status == "completed":
                    st.success("✅ Call ended. Final transcript saved.")
                    save_transcript(call_id, final_transcript)
                    break
            else:
                st.error(f"❌ Error fetching transcript: {response.status_code}")
                break
        except requests.exceptions.JSONDecodeError:
            st.error("❌ API returned an invalid response.")
            break
        except Exception as e:
            st.error(f"❌ Error: {e}")
            break
        time.sleep(2)
        retry_count += 1
    
    if retry_count >= max_retries:
        st.warning("Reached maximum polling attempts. Check the call status manually.")