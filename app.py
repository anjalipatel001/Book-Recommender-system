import pickle
import streamlit as st
import numpy as np

# Step: Page tracker
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

model = pickle.load(open('artifacts/model.pkl', 'rb'))
book_names = pickle.load(open('artifacts/book_names.pkl', 'rb'))
final_rating = pickle.load(open('artifacts/final_rating.pkl', 'rb'))
book_pivot = pickle.load(open('artifacts/book_pivot.pkl', 'rb'))


def show_welcome_page():
    # Custom page background and styles
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(to bottom right, #0f2027, #203a43, #2c5364);
            color: white;
            font-family: 'Segoe UI', sans-serif;
        }
        .title {
            font-size: 48px;
            font-weight: bold;
            text-align: center;
            margin-top: 30px;
        }
        .subtitle {
            font-size: 20px;
            text-align: center;
            color: #cccccc;
            margin-bottom: 30px;
        }
        .logo-container {
            display: flex;
            justify-content: center;
            margin-top: 50px;
            margin-bottom: 20px;
        }
        div.stButton > button {
            background-color: #111827;
            color: white;
            font-weight: bold;
            padding: 0.75em 2em;
            border-radius: 10px;
            border: none;
            transition: background-color 0.3s;
        }
        div.stButton > button:hover {
            background-color: #1f2937;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Centered logo using st.image
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("images/InkSpire_Logo.png", width=200)


    # Title and subtitle
    st.markdown("<div class='title'>Welcome to InkSpire</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Discover your next favorite book</div>", unsafe_allow_html=True)


   
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📚 Start Exploring", key="start_button"):
            st.session_state.page = 'main'
            st.rerun()


# Footer at bottom
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Made with ❤️ by <b>Anjali</b></p>", unsafe_allow_html=True)



           


def show_main_page():
    st.header("InkSpire-Book Recommendation System")

    with st.expander("📖 How It Works"):
        st.write("""
        - Select a Book – Choose any book from the dropdown menu. 📚
        - Analyze Ratings – The system checks how other users have rated similar books. ⭐
        - Find Similar Users – It looks at users who liked the same book as you. 👥
        - Recommend Books – Based on their choices, it suggests 5 similar books for you. 🔍
        - Show Covers – The recommended books appear with their cover images. 🎨
        """)

    selected_books = st.selectbox(
        "Type or select a book from the dropdown",
        book_names
    )

    import streamlit.components.v1 as components

    if st.button('Show Recommendation'):
        recommended_data = recommend_books(selected_books)
        cols = st.columns(5)

        for i in range(1, 6):  # Skip the selected book (index 0)
            with cols[i - 1]:
                components.html(f"""
                    <div style="position: relative; width: 100%;">
                        <img src="{recommended_data[i]['image']}" style="width: 100%; border-radius: 10px;">
                        <div style="
                            position: absolute;
                            bottom: 0;
                            background: rgba(0, 0, 0, 0.7);
                            color: white;
                            width: 100%;
                            padding: 10px;
                            box-sizing: border-box;
                            opacity: 0;
                            transition: opacity 0.3s;
                            font-size: 12px;
                            border-bottom-left-radius: 10px;
                            border-bottom-right-radius: 10px;
                        " onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=0">
                            <b>{recommended_data[i]['title']}</b><br>
                            {recommended_data[i]['author']}<br>
                            {recommended_data[i]['publisher']} ({recommended_data[i]['year']})
                        </div>
                    </div>
                """, height=250)


def fetch_book_info(suggestion):
    book_name = []
    ids_index = []
    book_data = []

    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])

    for name in book_name[0]:
        ids = np.where(final_rating['Title'] == name)[0][0]
        ids_index.append(ids)

    for idx in ids_index:
        data = {
            'title': final_rating.iloc[idx]['Title'],
            'author': final_rating.iloc[idx]['Author'],
            'publisher': final_rating.iloc[idx]['Publisher'],
            'year': final_rating.iloc[idx]['year'],
            'image': final_rating.iloc[idx]['Image-URL-L']
        }
        book_data.append(data)

    return book_data
  

def recommend_books(book_name):
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors=6)
    book_data = fetch_book_info(suggestion)
    return book_data


# Call appropriate page
# Page control logic
if st.session_state.page == 'welcome':
    show_welcome_page()
else:
    show_main_page()
