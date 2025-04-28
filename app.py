import pickle
import streamlit as st
import numpy as np
import streamlit.components.v1 as components

# Load models and data
model = pickle.load(open('artifacts/model.pkl', 'rb'))
book_names = pickle.load(open('artifacts/book_names.pkl', 'rb'))
final_rating = pickle.load(open('artifacts/final_rating.pkl', 'rb'))
book_pivot = pickle.load(open('artifacts/book_pivot.pkl', 'rb'))

# Function to fetch book info
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

# Function to recommend books
def recommend_books(book_name):
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors=6)
    book_data = fetch_book_info(suggestion)
    return book_data

# Main Streamlit UI
st.markdown("<h1 style='text-align: left;'>InkSpire - Book Recommendation System</h1><p>A System To Help You Find Your Next Read</p>", unsafe_allow_html=True)

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
