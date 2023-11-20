import streamlit as st
from read_doc import read_doc
from open_ai import prompt_open_ai

st.set_page_config(
    page_title="Main",
    layout="wide"
)

# Initialize session state variables
if 'saved_paragraphs' not in st.session_state:
    st.session_state.saved_paragraphs = []

# Initialize session state variables
if 'long_response' not in st.session_state:
    st.session_state.long_response = ""

# Initialize session state variables
if 'option' not in st.session_state:
    st.session_state.option = ""

response_short = ""
response_long = ""

uploaded_file = st.file_uploader("Upload a file")

if uploaded_file is not None:
    section_paragraph = read_doc(uploaded_file)
    titles = [i for i in section_paragraph.keys()]

    # Create a Markdown string to store the content
    markdown_content = ""

    # Append each paragraph's content to the Markdown string
    for title, content in section_paragraph.items():
        markdown_content += f"## {title}\n\n{content}\n\n"

    # Display the Markdown content
    st.markdown(markdown_content)

    text_input_long = (
        "You are an AI assistant tasked with supporting the rewriting of documents." + "\n" +
        "For each interaction, you will receive a paragraph of the document to process." + "\n\n" +
        "For each paragraph, rewrite it according to the following rules:" + "\n" +
        "• If necessary, you are allowed to change the structure of the paragraph." + "\n" +
        "• Identify and correct potential redundancies or inconsistencies with respect to previous paragraphs." + "\n" +
        "• Make the text more high level, principle-based, and reader-friendly using different wording." + "\n" +
        "• Improve language, grammar, and articulation of contents." + "\n" +
        "• Do not add any new information beyond what's provided and do not change the overall meaning." + "\n\n" +
        "Please respond only with the processed paragraph."
    )

    if st.button('Generate') and text_input_long is not None:

        response_long = prompt_open_ai(text_input_long, section_paragraph)
        responses = ""

        if response_long is not None:

            for paragraph in response_long:
                responses += paragraph + "\n\n"

            st.markdown(responses)
            st.session_state.long_response = responses

else:
    st.write('Please upload a document')
