import streamlit as st
from inference import cari_resep, cari_resep_dengan_context

# Page config
st.set_page_config(
    page_title="Recipe AI Chat",
    page_icon="🍳",
    layout="wide"
)

st.title("🍳 Recipe AI Chat - Asisten Resep Pintar")
st.markdown("*Tanya resep berdasarkan bahan atau budget yang Anda punya!*")

# Inisialisasi session state untuk menyimpan chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Tambahkan pesan welcome
    st.session_state.messages.append({
        "role": "assistant", 
        "content": """👋 **Halo! Saya Recipe AI, asisten resep pintar Anda!**

Saya bisa membantu Anda menemukan resep berdasarkan:
- 🥘 **Bahan yang tersedia**: "ayam, bawang, nasi"
- 💰 **Budget**: "budget 25ribu untuk 2 orang"
- ⏰ **Waktu memasak**: "resep cepat 15 menit"

Silakan tanya apa saja tentang resep masakan! 😊"""
    })

# Tampilkan chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input chat dari user
prompt = st.chat_input("Tanya resep atau masukkan bahan yang Anda punya...")

if prompt:
    # Tampilkan pesan dari user
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Simpan pesan user ke session state
    st.session_state.messages.append({
        "role": "user", 
        "content": prompt
    })
    
    # Generate response dengan context
    with st.chat_message("assistant"):
        with st.spinner("🔍 Mencari resep..."):
            try:
                response = cari_resep_dengan_context(prompt, st.session_state.messages)
            except Exception as e:
                response = f"❌ Maaf, terjadi kesalahan: {str(e)}"
        st.markdown(response)
    
    # Simpan response bot ke session state
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response
    })

# Sidebar dengan tips dan contoh
with st.sidebar:
    st.header("💡 Tips Penggunaan")
    
    st.subheader("🥘 Contoh Pertanyaan:")
    st.markdown("""
    - "Saya punya ayam, bawang, dan nasi. Bisa buat apa?"
    - "Budget 20ribu untuk 3 orang, ada resep apa?"
    - "Resep vegetarian yang cepat dan mudah"
    - "Makanan sehat untuk diet"
    - "Resep dengan telur dan sayuran"
    """)
    
    st.subheader("⚡ Tips:")
    st.markdown("""
    - Sebutkan bahan yang Anda punya
    - Tentukan budget jika ada keterbatasan
    - Sebutkan preferensi diet (vegetarian, halal, dll)
    - Tanya tips memasak untuk resep tertentu
    """)
    
    # Tombol clear chat
    if st.button("🗑️ Hapus Chat History"):
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Chat history telah dihapus! Silakan mulai percakapan baru. 😊"
        })
        st.rerun()

# Footer
st.markdown("---")
st.markdown("*Dibuat menggunakan Streamlit dan Google Gemini AI*")