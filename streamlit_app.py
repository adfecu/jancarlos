import streamlit as st
import sqlite3

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


# --- Simple CRUD App Demo with SQLite ---
st.header('Simple CRUD App Demo (SQLite)')

# Database setup
conn = sqlite3.connect('items.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)''')
conn.commit()

# Create
st.subheader('Create Item')
new_item = st.text_input('Enter new item')
if st.button('Add Item'):
    if new_item:
        c.execute('INSERT INTO items (name) VALUES (?)', (new_item,))
        conn.commit()
        st.success(f'Added: {new_item}')
    else:
        st.warning('Please enter an item.')

# Read
st.subheader('Items List')
c.execute('SELECT id, name FROM items')
rows = c.fetchall()
if rows:
    for idx, (item_id, item_name) in enumerate(rows):
        st.write(f"{item_id}. {item_name}")
else:
    st.info('No items yet.')

# Update
st.subheader('Update Item')
if rows:
    update_id = st.number_input('Select item ID to update', min_value=1, max_value=max([r[0] for r in rows]), step=1)
    updated_text = st.text_input('New value for item')
    if st.button('Update Item'):
        if updated_text:
            c.execute('UPDATE items SET name = ? WHERE id = ?', (updated_text, update_id))
            conn.commit()
            st.success(f'Item {update_id} updated.')
        else:
            st.warning('Please enter a new value.')
else:
    st.info('No items to update.')

# Delete
st.subheader('Delete Item')
if rows:
    delete_id = st.number_input('Select item ID to delete', min_value=1, max_value=max([r[0] for r in rows]), step=1)
    if st.button('Delete Item'):
        c.execute('DELETE FROM items WHERE id = ?', (delete_id,))
        conn.commit()
        st.success(f'Deleted item {delete_id}')
else:
    st.info('No items to delete.')
