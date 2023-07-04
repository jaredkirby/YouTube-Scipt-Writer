import streamlit as st
from utils.stream import StreamHandler
from langchain.chat_models import ChatOpenAI
import tools.titles as titles, tools.three_outlines as three_outlines, tools.single_outline as single_outline, tools.rough_script as rough_script, tools.final_script as final_script

openai_api_key = st.secrets["OPENAI_API_KEY"]
PAGE_TITLE = "ScriptPilot"
PAGE_ICON = "📺"
LAYOUT = "centered"

def set_page_config():
    st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=LAYOUT)

def create_chat(temperature, model, stream_handler):
    chat = ChatOpenAI(
        temperature=temperature, 
        model=model, 
        openai_api_key=openai_api_key, 
        request_timeout=250,
        streaming=True, 
        callbacks=[stream_handler]
    )
    return chat

def main():
    set_page_config()
    st.markdown(
        f"<h1 style='text-align: center;'>{PAGE_TITLE} {PAGE_ICON}<br>Tools for YouTube Script Writing!</h1>",
        unsafe_allow_html=True,
    )

    # Set up tabs
    tab1, tab2, tab3 = st.tabs(["Video Titles", "Video Outline", "Video Script"])

    # Video Titles Tab
    with tab1:
        handle_video_titles_tab()

    # Video Outline Tab
    with tab2:
        handle_video_outline_tab()

    # Video Script Tab
    with tab3:
        handle_video_script_tab()

    st.markdown(
        """
    ---
    Built by **Jared Kirby** :wave:

    [Twitter](https://twitter.com/Kirby_) | [GitHub](https://github.com/jaredkirby) | [LinkedIn](https://www.linkedin.com/in/jared-kirby/) | [Portfolio](https://www.jaredkirby.me)

        """
    )

def handle_video_titles_tab():
    temperature = st.slider('Select temperature', min_value=0.0, max_value=2.0, step=0.1, value=1.0, key="title_temp")
    model = 'gpt-3.5-turbo'
    titles_button = st.button("Generate Video Titles")
    if titles_button:
        titles_chat_box = st.empty()
        stream_handler = StreamHandler(titles_chat_box)
        titles_chat = create_chat(temperature, model, stream_handler)
        titles.get_titles(titles_chat)

def handle_video_outline_tab():
    user_input = st.text_area("Input Title", key="title_input")
    temperature = st.slider('Select temperature', min_value=0.0, max_value=2.0, step=0.1, value=1.0, key="outline_temp")
    model = 'gpt-4'
    outlines_button = st.button("Generate Video Outlines")
    if outlines_button:
        single_chat_box = st.empty()
        single_stream_handler = StreamHandler(single_chat_box)
        single_chat = create_chat(temperature, model, single_stream_handler)
        
        three_chat_box = st.empty()
        three_stream_handler = StreamHandler(three_chat_box)
        three_chat = create_chat(temperature, model, three_stream_handler)
        
        three_results = three_outlines.get_outlines(three_chat, outlines_input=user_input)
        single_outline.get_outline(single_chat, selected_input=three_results)

def handle_video_script_tab():
    outline_input = st.text_area("Input Outline", key="outline_input")
    research_input = st.text_area("Input Research", key="research_input")
    temperature = st.slider('Select temperature', min_value=0.0, max_value=2.0, step=0.1, value=1.0, key="script_temp")
    model = 'gpt-3.5-turbo-16k'
    script_button = st.button("Generate Video Script")
    if script_button:
        final_chat_box = st.empty()
        final_stream_handler = StreamHandler(final_chat_box)
        final_chat = create_chat(temperature, model, final_stream_handler)
        
        draft_chat_box = st.empty()
        draft_stream_handler = StreamHandler(draft_chat_box)
        draft_chat = create_chat(temperature, model, draft_stream_handler)
        
        _rough_script = rough_script.get_rough_script(draft_chat, outline=outline_input)
        final_script.get_final_script(final_chat, outline=outline_input, rough_script=_rough_script)

if __name__ == "__main__":
    main()
