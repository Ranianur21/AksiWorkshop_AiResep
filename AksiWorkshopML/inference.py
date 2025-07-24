import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API KEY
api_key = os.getenv("GEMINI_API_KEY")

# Konfigurasi Gemini dan inisialisasi model
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Configure Gemini dengan API key
genai.configure(api_key=api_key)

try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
    except Exception as e2:
        raise

def cari_resep_dengan_context(user_input, chat_history=None):
    """
    Fungsi untuk cari resep dengan context dari chat history
    """
    
    system_prompt = """
    Anda adalah Recipe AI, asisten resep pintar yang membantu mencari resep masakan.
    
    Tugas Anda:
    1. Berikan resep berdasarkan bahan, budget, atau preferensi yang disebutkan
    2. Ingat percakapan sebelumnya dan berikan resep yang relevan
    3. Jika user minta "resep lain" atau "variasi", berikan yang berbeda dari sebelumnya
    4. Format resep dengan jelas dan mudah diikuti
    
    Format jawaban:
    **RESEP 1: [Nama]**
    - Bahan: [list bahan]
    - Cara: [langkah singkat]
    - Waktu: [estimasi]
    
    **RESEP 2: [Nama]**
    - Bahan: [list bahan]
    - Cara: [langkah singkat] 
    - Waktu: [estimasi]
    
    Buat yang mudah dan praktis! Jawab dalam bahasa Indonesia.
    """
    
    try:
        # ADA CHAT HISTORY
        if chat_history and len(chat_history) > 1:
            messages = []
            
            messages.append({
                "role": "user",
                "parts": [system_prompt]
            })
            messages.append({
                "role": "model", 
                "parts": ["Baik, saya siap membantu Anda mencari resep! Silakan tanya apa saja tentang resep masakan."]
            })
            
            # TAMBAH CHAT HISTORY
            for msg in chat_history[1:-1]:  
                if msg["role"] == "user":
                    messages.append({
                        "role": "user",
                        "parts": [msg["content"]]
                    })
                elif msg["role"] == "assistant":
                    messages.append({
                        "role": "model",
                        "parts": [msg["content"]]
                    })
            
            # CURRENT USER INPUT
            messages.append({
                "role": "user",
                "parts": [user_input]
            })
            
            # START CHAT DENGAN HISTORY
            chat = model.start_chat(history=messages[:-1])  # Semua kecuali message terakhir
            response = chat.send_message(user_input)
            
        else:
            # Jika tidak ada history, gunakan generate_content biasa
            full_prompt = f"""
            {system_prompt}
            
            User: {user_input}
            
            Berikan 2 resep sederhana berdasarkan permintaan user di atas.
            """
            response = model.generate_content(full_prompt)
        
        if response and response.text:
            print("✅ Resep berhasil digenerate")
            return response.text
        else:
            return "❌ Tidak mendapat response dari Gemini"
            
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error: {error_msg}")
        
        # ERROR HANDLING 
        if "quota" in error_msg.lower():
            return "❌ Quota API habis. Coba lagi besok atau upgrade akun Gemini."
        elif "api" in error_msg.lower() and "key" in error_msg.lower():
            return "❌ API key tidak valid. Cek file .env Anda."
        else:
            return f"❌ Error: {error_msg}"

def cari_resep(bahan_atau_budget):
    """
    Fungsi sederhana untuk cari resep (tanpa context)
    """
    return cari_resep_dengan_context(bahan_atau_budget)


# if __name__ == "__main__":
#     print("🚀 Starting inference test...")
    
#     # Test 1: Input normal
#     print("\n📝 Test 1: Ayam, bawang, nasi")
#     result1 = cari_resep("ayam, bawang, nasi")
#     print("Result:")
#     print(result1[:200] + "..." if len(result1) > 200 else result1)
    
#     # Test 2: Budget
#     print("\n📝 Test 2: Budget")
#     result2 = cari_resep("budget 25ribu untuk 2 orang")
#     print("Result:")
#     print(result2[:200] + "..." if len(result2) > 200 else result2)
    
#     print("\n✅ Testing completed!")