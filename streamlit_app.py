import streamlit as st

# Add custom CSS to hide the GitHub icon
hide_github_icon = """
<style>
#GithubIcon {
  visibility: hidden;
}
</style>
"""
st.markdown(hide_github_icon, unsafe_allow_html=True)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("Jan Carlos Placencio")
st.write(
    "Bienvenidos a mi página web"
)
