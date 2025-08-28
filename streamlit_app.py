import streamlit as st

hide_streamlit_style = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("Jan Carlos Placencio")
st.write(
    "Bienvenidos a mi página web"
)

# --- Simple CRUD App Demo ---
st.header('Simple CRUD App Demo')

# Simple in-memory data store
if 'items' not in st.session_state:
    st.session_state['items'] = []

# Create
st.subheader('Create Item')
new_item = st.text_input('Enter new item')
if st.button('Add Item'):
    if new_item:
        st.session_state['items'].append(new_item)
        st.success(f'Added: {new_item}')
    else:
        st.warning('Please enter an item.')

# Read
st.subheader('Items List')
if st.session_state['items']:
    for idx, item in enumerate(st.session_state['items']):
        st.write(f"{idx+1}. {item}")
else:
    st.info('No items yet.')

# Update
st.subheader('Update Item')
if st.session_state['items']:
    update_idx = st.number_input('Select item number to update', min_value=1, max_value=len(st.session_state['items']), step=1)
    updated_text = st.text_input('New value for item')
    if st.button('Update Item'):
        if updated_text:
            st.session_state['items'][update_idx-1] = updated_text
            st.success(f'Item {update_idx} updated.')
        else:
            st.warning('Please enter a new value.')
else:
    st.info('No items to update.')

# Delete
st.subheader('Delete Item')
if st.session_state['items']:
    delete_idx = st.number_input('Select item number to delete', min_value=1, max_value=len(st.session_state['items']), step=1)
    if st.button('Delete Item'):
        removed = st.session_state['items'].pop(delete_idx-1)
        st.success(f'Deleted: {removed}')
else:
    st.info('No items to delete.')
