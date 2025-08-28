import streamlit as st

# Add custom CSS to hide the GitHub icon
hide_github_icon = """
#GithubIcon {
  visibility: hidden;
}
"""
st.markdown(hide_github_icon, unsafe_allow_html=True)

st.title("Jan Carlos Placencio")
st.write(
    "Bienvenidos a mi página web"
)
