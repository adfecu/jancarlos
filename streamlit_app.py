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



# --- Custom Layout CRUD App ---
st.header('CRUD Demo (Custom Layout)')


# Database setup
conn = sqlite3.connect('items.db')
c = conn.cursor()
# Add 'order' column if not exists
c.execute('''CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, "order" INTEGER)''')
conn.commit()
# Ensure all items have an order value
c.execute('SELECT id FROM items WHERE "order" IS NULL')
missing_order = c.fetchall()
if missing_order:
    c.execute('SELECT MAX("order") FROM items')
    max_order = c.fetchone()[0] or 0
    for idx, (item_id,) in enumerate(missing_order, start=1):
        c.execute('UPDATE items SET "order" = ? WHERE id = ?', (max_order + idx, item_id))
    conn.commit()




# Top row: Single text input for search and create
top1, top2, top3 = st.columns([2,1,1])
with top1:
    text_bar = st.text_input('Buscar o Añadir', key='main_text')
with top2:
    search_btn = st.button('Buscar', key='search_btn')
with top3:
    add_btn = st.button('Añadir', key='add_btn')

# Logic for both buttons
rows = []
if add_btn:
    if text_bar.strip():
        c.execute('SELECT MAX("order") FROM items')
        max_order = c.fetchone()[0] or 0
        c.execute('INSERT INTO items (name, "order") VALUES (?, ?)', (text_bar.strip(), max_order + 1))
        conn.commit()
        st.success(f'Añadido: {text_bar.strip()}')
        st.experimental_rerun()
    else:
        st.warning('No se permiten entradas vacías.')
elif search_btn:
    if text_bar.strip():
        c.execute('SELECT id, name, "order" FROM items WHERE name LIKE ? ORDER BY "order"', (f'%{text_bar.strip()}%',))
        rows = c.fetchall()
        if not rows:
            st.info('No se encontraron coincidencias.')
    else:
        st.warning('No se permiten búsquedas vacías.')
        rows = []
else:
    c.execute('SELECT id, name, "order" FROM items ORDER BY "order"')
    rows = c.fetchall()


# Item list table
st.markdown('---')
st.subheader('Lista de Items')
if rows:
    item_ids = [r[0] for r in rows]
    for idx, (item_id, item_name, item_order) in enumerate(rows):
        row1, row2, row3, row4, row5 = st.columns([6,1,1,2,1])
        with row1:
            st.text_input(f'Item {item_id}', value=item_name, key=f'edit_{item_id}', disabled=True)
        with row2:
            if st.button('Eliminar', key=f'del_{item_id}'):
                c.execute('DELETE FROM items WHERE id = ?', (item_id,))
                conn.commit()
                st.experimental_rerun()
        with row3:
            edit_mode = st.session_state.get(f'edit_mode_{item_id}', False)
            if st.button('Editar', key=f'edit_btn_{item_id}'):
                st.session_state[f'edit_mode_{item_id}'] = True
                st.experimental_rerun()
            if edit_mode:
                edit_val = st.text_input('Nuevo valor', value=item_name, key=f'edit_val_{item_id}')
                if st.button('Guardar', key=f'save_{item_id}'):
                    if edit_val.strip():
                        c.execute('UPDATE items SET name = ? WHERE id = ?', (edit_val.strip(), item_id))
                        conn.commit()
                        st.session_state[f'edit_mode_{item_id}'] = False
                        st.success(f'Item {item_id} actualizado.')
                        st.experimental_rerun()
                    else:
                        st.warning('No se permiten entradas vacías.')
        with row4:
            move_options = [f'Después de {r[0]}' for r in rows if r[0] != item_id]
            if move_options:
                move_target = st.selectbox('Mover a:', move_options, key=f'move_target_{item_id}')
                if st.button('Mover', key=f'move_{item_id}'):
                    # Get target id
                    target_id = int(move_target.split()[-1])
                    # Get target order
                    c.execute('SELECT "order" FROM items WHERE id = ?', (target_id,))
                    target_order = c.fetchone()[0]
                    # Move current item after target
                    c.execute('SELECT id, "order" FROM items WHERE "order" > ?', (target_order,))
                    following = c.fetchall()
                    # Shift following items down
                    for f_id, f_order in following:
                        c.execute('UPDATE items SET "order" = ? WHERE id = ?', (f_order + 1, f_id))
                    # Set moved item's order
                    c.execute('UPDATE items SET "order" = ? WHERE id = ?', (target_order + 1, item_id))
                    conn.commit()
                    st.success(f'Item {item_id} movido después de {target_id}.')
                    st.experimental_rerun()
            else:
                st.write('No hay otros items')
        with row5:
            st.write(f'Orden: {item_order}')
else:
    st.info('No hay items.')
