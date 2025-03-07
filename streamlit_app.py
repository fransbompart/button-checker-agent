import streamlit as st
from agent.button_checker_agent import ButtonCheckerAgent
import asyncio
import glob

st.title("👆🤖 Button Checker Agent")

async def run_agent():
    agent = ButtonCheckerAgent()
    buttons_output = await agent.check()
    return buttons_output

def get_first_video():
    video_files = glob.glob("recordings/*.webm")
    if video_files:
        return video_files[0]
    return None

# Botón para ejecutar el agente
if st.button("Run Agent"):
    buttons_output = asyncio.run(run_agent())
    
    st.write("Buttons output:")
    for button in buttons_output.outputs:
        st.write(f"Button Name: {button.button_name}")
        st.write(f"Button Action Result Description: {button.button_action_result_description}")
        st.write(f"Button Action Result Success: {button.button_action_result_success}")
        st.write("---")
    
    st.write("Recording:")
    video_path = get_first_video()
    if video_path:
        st.video(video_path)
    else:
        st.write("No video found in the recordings folder.")
