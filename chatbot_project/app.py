from flask import Flask, render_template, request, jsonify,session
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Define keyword-based intents
intents = {
    "greeting": {
        "keywords": ["hello","Hlo","hi", "hey", "greetings", "good morning", "good afternoon", "good evening", "what's up", "yo"],
        "responses": [
            "Hello! How can I assist you today? 😊", 
            "Hi there! 👋 What can I help you with?", 
            "Hey! Welcome to our store. How may I help you?"
        ]
    },
    "clothes": {
        "keywords": ["clothes", "dress", "t-shirt", "shirt", "jeans", "jacket", "hoodie", "sweater", "pants", "shorts", "skirt", "blouse", "top", "outfit", "fashion"],
        "responses": [
            "We offer a wide range of clothes including shirts, t-shirts, jeans, jackets, and more! 👕👖🧥", 
            "Looking for something stylish? Check out our latest collection of dresses, hoodies, and casual wear! 👗", 
            "We have trendy tops, jeans, and jackets available. What style are you looking for?"
        ]
    },
    "sizes": {
        "keywords": ["size", "sizes", "available sizes", "what sizes do you have", "size guide", "measurements"],
        "responses": [
            "We have sizes from XS to XXL. Need help finding your perfect fit? 📏", 
            "Our size range is XS to XXL. Check our size guide for accurate measurements!", 
            "Not sure about your size? Let me help you with our sizing chart!"
        ]
    },
    "order_tracking": {
        "keywords": ["track", "order", "order status", "where is my order", "tracking", "order id", "package status"],
        "responses": [
            "Please provide your order ID so I can check the status for you. 📦", 
            "To track your order, share your order number, and I’ll look it up!", 
            "Want to know where your package is? Just give me your order ID!"
        ]
    },
    "return_policy": {
        "keywords": ["return", "refund", "return policy", "can I return", "how to return", "return process"],
        "responses": [
            "You can return the product within 30 days of delivery for a full refund. 🔄", 
            "Our return policy allows returns within 30 days with the original receipt.", 
            "Not satisfied? No worries! Returns are accepted within 30 days."
        ]
    },
    "payment_methods": {
        "keywords": ["payment", "pay", "credit card", "debit card", "cash on delivery", "upi", "paypal", "net banking", "how to pay", "payment options"],
        "responses": [
            "We accept UPI, Credit/Debit Cards, PayPal, and Cash on Delivery. 💳💵", 
            "You can pay via card, UPI, or choose Cash on Delivery at checkout!", 
            "Multiple payment options available: Card, UPI, Net Banking, and COD."
        ]
    },
    "delivery_time": {
        "keywords": ["delivery time", "when will it arrive", "shipping", "delivery days", "how long for delivery", "shipment time", "estimated delivery"],
        "responses": [
            "Delivery usually takes **3-5 business days**. 🚚", 
            "Your order will arrive within 3-5 working days. Express shipping is also available!", 
            "Standard shipping takes 3-5 days. Need it faster? Check our express delivery option!"
        ]
    },
    "exchange_policy": {
        "keywords": ["exchange", "replace", "exchange policy", "can I exchange", "wrong size exchange", "how to exchange"],
        "responses": [
            "We allow product exchanges within **15 days** of delivery. 🔁", 
            "Need a different size or color? Exchanges are possible within 15 days!", 
            "You can exchange your item within 15 days if it’s unused and in original packaging."
        ]
    },
    "discounts": {
        "keywords": ["discount", "offer", "sale", "coupon", "promo code", "deals", "special offer", "any discounts"],
        "responses": [
            "Check our website for the latest **deals and offers**! 💸", 
            "We have ongoing sales! Use code **WELCOME10** for 10% off your first order!", 
            "Looking for discounts? Subscribe to our newsletter for exclusive promo codes!"
        ]
    },
    "store_location": {
        "keywords": ["store", "location", "address", "shop", "physical store", "where are you located", "visit store"],
        "responses": [
            "We are an **online store**, but you can shop directly from our website! 🛒", 
            "Currently, we operate online for a seamless shopping experience. Visit us at [Website URL]!", 
            "No physical stores yet, but you can explore our entire collection online!"
        ]
    },
    "support": {
        "keywords": ["help", "support", "contact", "customer care", "customer service", "need help", "talk to someone"],
        "responses": [
            "You can reach our support team at **support@example.com** or call us at **+1-XXX-XXX-XXXX**. 📧", 
            "Need assistance? Our customer care team is available 24/7 at support@example.com!", 
            "For any queries, email us at support@example.com or chat with a live agent!"
        ]
    },
    "goodbye": {
        "keywords": ["bye", "goodbye", "see you", "later", "thanks", "thank you", "that's all"],
        "responses": [
            "Goodbye! Have a great day! 😊", 
            "Thanks for chatting! See you soon! 👋", 
            "Happy shopping! Come back anytime!"
        ]
    },
    "out_of_stock": {
        "keywords": ["out of stock", "not available", "when will it be back", "restock", "sold out"],
        "responses": [
            "This item is currently out of stock, but it’ll be back soon! Check again later.", 
            "Sorry, this product is sold out. Would you like a similar recommendation?", 
            "We’re restocking soon! Sign up for notifications to get an alert when it’s available."
        ]
    },
    "product_recommendation": {
        "keywords": ["recommend", "suggest", "what should I buy", "best product", "popular items"],
        "responses": [
            "Our bestsellers include [Shirt], [shoes], and [t-shirts]. Want details on any?", 
            "Looking for something trendy? Check out our new arrivals!", 
            "Based on your preferences, I’d recommend [Product X]. Would you like more options?"
        ]
    },
    "website_help": {
        "keywords": ["how to use website", "navigate", "where to find", "how to order", "website guide"],
        "responses": [
            "Need help navigating? Visit our **FAQ section** or follow the step-by-step guide!", 
            "Stuck? Click on ‘Help’ at the top of the page for instructions.", 
            "To place an order, simply browse, add to cart, and checkout. Need a walkthrough?"
        ]
    },
    "feedback": {
        "keywords": ["feedback", "review", "rate", "how was your experience", "suggest improvement"],
        "responses": [
            "We’d love your feedback! Share your thoughts on our products or service. 💬",  
            "Your opinion matters! Rate your experience or suggest how we can improve.",  
            "Thanks for shopping with us! Would you like to leave a review?"
        ]
    },
    "loyalty_program": {
        "keywords": ["loyalty program", "rewards", "membership", "discount for regulars", "points system"],
        "responses": [
            "Join our **Loyalty Program** to earn points on every purchase and get exclusive discounts! 🎁",  
            "Sign up for rewards! Earn 1 point per $1 spent and redeem them later.",  
            "Regular customers get special perks! Ask me how to enroll in our rewards program."
        ]
    },
    "bulk_orders": {
        "keywords": ["bulk order", "wholesale", "corporate order", "buy in bulk", "large quantity"],
        "responses": [
            "Interested in bulk purchases? Email **sales@example.com** for wholesale pricing! 📦",  
            "We offer discounts for bulk/wholesale orders. Let me connect you with our sales team.",  
            "For corporate or large orders, visit our ‘Wholesale’ page or contact us directly."
        ]
    },
    "new_arrivals": {
        "keywords": ["new arrivals", "latest collection", "just launched", "trending now", "what's new"],
        "responses": [
            "Check out our **New Arrivals** for the freshest styles this season! 👗🔥",  
            "Our latest collection just dropped! Want a sneak peek?",  
            "New items added weekly! Explore now before they sell out."
        ]
    },
    "care_instructions": {
        "keywords": ["how to wash", "fabric care", "washing instructions", "dry clean", "maintain clothes"],
        "responses": [
            "For best results, wash in cold water and avoid direct sunlight to preserve colors. 🧼",  
            "Check the label inside your garment for specific care instructions.",  
            "Need fabric care tips? Most of our items are machine-washable, but delicate pieces may need handwashing."
        ]
    },
    "price_match": {
        "keywords": ["price match", "lower price elsewhere", "competitor price", "can you beat this price"],
        "responses": [
            "We offer **price matching** on select items! Share the competitor’s link for verification. 💰",  
            "Found it cheaper elsewhere? Contact support with details, and we’ll try to match it!",  
            "Our prices are already competitive, but we’ll review price-match requests case by case."
        ]
    },
    "gift_cards": {
        "keywords": ["gift card", "voucher", "e-gift", "present", "birthday gift"],
        "responses": [
            "Gift cards are available in any amount! Perfect for birthdays or holidays. 🎁",  
            "Surprise someone with a digital gift card—delivered instantly via email!",  
            "Need a last-minute gift? Our e-gift cards never expire!"
        ]
    },
    "style_advice": {
        "keywords": ["style tips", "what to wear", "outfit ideas", "fashion advice", "how to style"],
        "responses": [
            "Need outfit inspiration? Try pairing jeans with our oversized blazers for a chic look! 👖👔",  
            "Pro tip: Layer a turtleneck under your dress for winter. Want more suggestions?",  
            "Check our blog for seasonal style guides and trend breakdowns!"
        ]
    },
    "sustainability": {
        "keywords": ["eco-friendly", "sustainable", "ethical fashion", "recycled materials", "environment"],
        "responses": [
            "We’re committed to sustainability! Many items use organic cotton/recycled fabrics. 🌱",  
            "Learn about our eco-initiatives on the ‘Sustainability’ page in our footer.",  
            "Ethical fashion matters! We partner with fair-trade certified suppliers."
        ]
    },
    "holiday_hours": {
        "keywords": ["holiday hours", "christmas closure", "new year timing", "open on thanksgiving"],
        "responses": [
            "We’ll be closed on **December 25th** but open with limited hours on the 24th. 🎄",  
            "Check our ‘Holiday Schedule’ page for special hours during festivals.",  
            "Customer support operates 24/7, but deliveries may delay during holidays."
        ]
    },
    "international_shipping": {
        "keywords": ["international shipping", "ship abroad", "deliver overseas", "global delivery"],
        "responses": [
            "We ship worldwide! Delivery fees and times vary by country. 🌍",  
            "International orders may take 7–14 business days. Customs fees could apply.",  
            "Enter your address at checkout to see shipping options for your country."
        ]
    },
    "cancellation_request": {
        "keywords": ["cancel order", "change order", "stop shipment", "ordered by mistake"],
        "responses": [
            "Need to cancel? We’ll try if it hasn’t shipped yet. Share your **order ID**. ✋",  
            "Order cancellations are possible within 1 hour of placement. Want me to check?",  
            "Contact support ASAP with your order number to request cancellation."
        ]
    },
    
}


default_response = "Sorry, I didn't understand that. Can you rephrase it? 🤖"

def get_response(user_input):
    user_input = user_input.lower()
    for intent in intents.values():
        for keyword in intent["keywords"]:
            if keyword in user_input:
                return intent["responses"][0]
    return default_response

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    user_input = request.form["msg"]
    response = get_response(user_input)
    return jsonify({"response": response})

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.form.get('Body')
    response_text = get_response(incoming_msg)
    resp = MessagingResponse()
    resp.message(response_text)
    return str(resp)

@app.route("/faq")
def faq():
    return render_template("faq.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
