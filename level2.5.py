# --- START OF FILE denemeLm.py ---

try:
    from openai import OpenAI
except ImportError:
    import sys
    sys.stderr.write("Required package 'openai' is not installed.\n")
    sys.stderr.write("Install it with: python3 -m pip install openai\n")
    sys.stderr.write("Or run the script using the project's virtualenv: /Users/basakbal/Documents/mcp/.venv/bin/python level2.5.py\n")
    sys.exit(1)

# --- CONFIGURATION ---
# Model name set to Llama 3 8B as requested.
# If the exact name in LM Studio differs, copy and update this line from the server.
MODEL_ADI = "meta-llama/Meta-Llama-3-8B-Instruct-GGUF"

# 1. Connect to the LM Studio server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# 2. Chat history and system message
history = [
    {"role": "system", "content": "Sen, sorulara sadece Türkçe cevap veren, yardımsever ve bilgili bir asistansın. Cevapların net, anlaşılır ve kibar olmalı."},
]

# 3. Main chat loop
print(f"🤖 Yerel Asistan'a hoş geldiniz! (Model: {MODEL_ADI})")
print("   Çıkmak için 'çıkış' yazabilirsiniz.")
print("-" * 60)

while True:
    user_input = input("😀 Siz: ")

    if user_input.lower() in ["exit", "quit", "çıkış"]:
        print("👋 Görüşmek üzere!")
        break

    history.append({"role": "user", "content": user_input})

    try:
        completion = client.chat.completions.create(
            model=MODEL_ADI,
            messages=history,
            temperature=0.7,
        )

        response_message = completion.choices[0].message.content
        print(f"🤖 Asistan: {response_message}")

        history.append({"role": "assistant", "content": response_message})

    except Exception as e:
        print(f"\n❌ Bir Hata Oluştu: {e}")
        print("   Lütfen LM Studio'da sunucunun çalıştığından ve yukarıdaki model adının doğru olduğundan emin olun.")
        break