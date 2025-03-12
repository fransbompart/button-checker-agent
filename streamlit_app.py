import streamlit as st
from lmnr import Laminar

from dotenv import load_dotenv
from streamlit_option_menu import option_menu
from content_checker_by_section_agent.content_checker_by_section_agent_runner import ContentCheckerAgentRunner
from content_checker_by_section_agent.soyZen.soy_zen_content_checker_by_section_agent import SoyZenContentCheckerBySectionAgent
from content_checker_by_section_agent.vidaFit.vida_fit_content_checker_by_section_agent import VidaFitContentCheckerBySectionAgent
import asyncio
import os
import glob

load_dotenv()

Laminar.initialize(project_api_key=os.getenv('LMNR_PROJECT_API_KEY', ''))

async def show_content_checker_agent_output(app: str):
    content_output = await ContentCheckerAgentRunner.run(app)
    st.write("Matches:")
    st.json(content_output['matches']) 

    st.write("Previews:")
    st.json(content_output['previews']) 

    st.write("Contents:")
    st.json(content_output['contents']) 
       
    # st.write("Recordings:")

    # video_files = glob.glob('button_checker_agent/'+ app + '/recordings')
    # for i, video_file in enumerate(video_files):
    #     if video_file:
    #         st.video(video_file)
    #     else:
    #         st.write(f"Video {i} not found in the recordings folder.")


st.title("👆🤖 TDA Agents")

with st.sidebar:
    selected = option_menu(
        "Menú de Navegación",
        ["Content Checker", "Button Checker"],
        icons=["check-circle", "check-circle"],
        menu_icon="cast",
        default_index=0,
    )

if selected == "Button Checker":
    SOY_ZEN = "SoyZen"
    VIDA_FIT = "VidaFit"

    st.header("Button Checker Agent")
    content_checker_option = st.selectbox("Selecciona una opción", [SOY_ZEN])

    if content_checker_option == SOY_ZEN:
        if st.button("Run SoyZen Agent"):
            asyncio.run(show_content_checker_agent_output("SoyZen"))    
        

elif selected == "Content Checker":
    st.header("Content Checker Agent")
    content_checker_option = st.selectbox("Selecciona una opción", ["SoyZen", "VidaFit"])

    if content_checker_option == "SoyZen":
        if st.button("Run SoyZen Agent"):
            asyncio.run(show_content_checker_agent_output("SoyZen"))
    
    elif content_checker_option == "VidaFit":
        if st.button("Run VidaFit Agent"):
            asyncio.run(show_content_checker_agent_output("VidaFit"))
    
