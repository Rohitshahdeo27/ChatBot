# 🛍️ Shopping Chatbot (Flask + Twilio WhatsApp)

This is a simple **AI-like chatbot** built using **Flask** that can handle customer queries for an online store.  
It supports both **web-based chat** and **WhatsApp integration** via Twilio.  

---

## 🚀 Features
- Keyword-based **intent detection** (e.g., greetings, product queries, order tracking).
- **Predefined responses** for FAQs like return policy, delivery time, payments, etc.
- **Web Interface** (`index.html`) for direct chat.
- **Twilio WhatsApp API** integration for real-time WhatsApp chat.
- Easily customizable **intents and responses**.

---

## 🛠️ Tech Stack
- **Python 3.8+**
- **Flask** (Web framework)
- **Twilio** (WhatsApp Messaging API)
- **HTML/CSS/JS** (Frontend templates)

---

## 📂 Project Structure
```
project/
│── app.py              # Main Flask application
│── templates/
│   ├── index.html      # Chat UI
│   ├── faq.html        # FAQ Page
│── static/             # CSS/JS/Images (if any)
│── README.md           # Project Documentation
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/yourusername/shopping-chatbot.git
cd shopping-chatbot
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

### 3️⃣ Install Dependencies
```bash
pip install flask twilio
```

### 4️⃣ Run Flask App
```bash
python app.py
```
Server runs on:  
👉 http://127.0.0.1:5000  

---

## 💬 Usage

### 🖥️ Web Chat
- Open `http://127.0.0.1:5000` in your browser.
- Type messages, chatbot responds instantly.

### 📱 WhatsApp Chat (via Twilio)
1. Set up a **Twilio WhatsApp Sandbox**.
2. Configure the **Webhook URL** in Twilio to:
   ```
   http://<your-server-ip>:5000/whatsapp
   ```
3. Send a message on WhatsApp → Bot replies automatically.

---

## 🔑 API Endpoints

| Endpoint     | Method | Description |
|--------------|--------|-------------|
| `/`          | GET    | Renders the homepage (chat UI). |
| `/get`       | POST   | Accepts user input from web chat and returns bot response (JSON). |
| `/whatsapp`  | POST   | Handles incoming WhatsApp messages (via Twilio). |
| `/faq`       | GET    | Displays FAQ page. |

---

## 🧠 Intents & Responses
- **Greeting** → "Hello", "Hi", "Hey" → Friendly welcome.
- **Clothes** → "shirt", "jeans", "jacket" → Clothing suggestions.
- **Order Tracking** → "track order", "where is my order" → Asks for order ID.
- **Return Policy** → "return", "refund" → Explains return rules.
- **Delivery Time** → "when will it arrive" → 3-5 business days.
- ...and many more! (see `intents` dictionary in `app.py`)

Default response:  
```
"Sorry, I didn't understand that. Can you rephrase it? 🤖"
```

---

## 🛠️ Customization
- Open `app.py` → modify the **`intents` dictionary**.
- Add new keywords and responses as needed.
- Update frontend (`index.html`) for UI enhancements.

---

## 📌 Future Enhancements
- Use **NLP libraries** (NLTK, spaCy, Transformers) for smarter intent detection.
- Connect with a **real database** for dynamic order tracking.
- Add **admin panel** for managing FAQs and responses.

---

## 📜 License
This project is open-source. You may use and modify it for personal or commercial projects.
