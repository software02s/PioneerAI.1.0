from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# List of cars (simplified as a dictionary for this example)
makinat = [
    {"marka": "Mercedes" , "modeli": "C-Class", "viti": 2022, "ngjyra": "E bardhë", "karburanti": "Benzinë", "motori": "2.0L", "cmimi": 80},
    {"marka": "Rolls", "modeli": "Phantom", "viti": 2021, "ngjyra": "E zezë", "karburanti": "Naftë", "motori": "6.6L", "cmimi": 70},
    {"marka": "Range", "modeli": "Sport", "viti": 2020, "ngjyra": "Gri", "karburanti": "Benzinë", "motori": "3.0L", "cmimi": 65},
    {"marka": "Porsh", "modeli": "911", "viti": 2023, "ngjyra": "E kuqe", "karburanti": "Benzinë", "motori": "3.8L", "cmimi": 60},
    {"marka": "Golf", "modeli": "Golf", "viti": 2020, "ngjyra": "Argjend", "karburanti": "Benzinë", "motori": "1.4L", "cmimi": 55},
    {"marka": "Toyota", "modeli": "Corolla", "viti": 2019, "ngjyra": "Blu", "karburanti": "Nafte", "motori": "1.4L", "cmimi": 40},
    {"marka": "BMW", "modeli": "X5", "viti": 2022, "ngjyra": "E zezë", "karburanti": "Naftë", "motori": "3.0L", "cmimi": 50},
    {"marka": "Audi", "modeli": "A4", "viti": 2021, "ngjyra": "Gri", "karburanti": "Benzinë", "motori": "2.0L", "cmimi": 50},
    {"marka": "Hundai", "modeli": "Tucson", "viti": 2020, "ngjyra": "E gjelbër", "karburanti": "Benzinë", "motori": "2.0L", "cmimi": 60}
]

# Load ratings 
RATING_FILE_PATH = 'ratings.json'

def load_ratings():
    try:
        with open(RATING_FILE_PATH, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return empty list if file doesn't exist or is empty

# Save ratings to a rate,jscon
def save_ratings(ratings):
    try:
        with open(RATING_FILE_PATH, 'w') as file:
            json.dump(ratings, file, indent=4)
    except Exception as e:
        print(f"Error saving ratings: {e}")

# Function to return chatbot response based on user message
def merr_përgjigje_bot(user_message):
    mesazhi_i_përdoruesit = user_message.lower()

    if any(keyword in mesazhi_i_përdoruesit for keyword in ["makina", "makinat", "makin", "makine" , "makinash"]):
        lista_e_makinave = [makina['marka'] for makina in makinat]
        if lista_e_makinave:
            return f"Këtu janë disa makina të disponueshme: {', '.join(lista_e_makinave)}."
        else:
            return "Na vjen keq, nuk mund të gjejmë makina të disponueshme."

    # Respond based on car brand (Mercedes, Rolls-Royce, etc.)
    for makina in makinat:
        if makina['marka'].lower() in mesazhi_i_përdoruesit:
            return f"Modeli: {makina['modeli']}, Viti: {makina['viti']}, Ngjyra: {makina['ngjyra']}, Karburanti: {makina['karburanti']}, Motori: {makina['motori']}, Çmimi: {makina['cmimi']} €."

    # Default responses for common phrases
    if "pershendetje" in mesazhi_i_përdoruesit or "hi" in mesazhi_i_përdoruesit:
        return "Përshëndetje! Si mund të ju ndihmoj sot?"
    elif "ndihme" in mesazhi_i_përdoruesit:
        return "Sigurisht! Si mund te ndihmoj?"
    elif "faleminderit" in mesazhi_i_përdoruesit or "flm" in mesazhi_i_përdoruesit:
        return "Ju faleminderit! Më njoftoni nëse keni nevojë për diçka tjetër."
    elif "bye" in mesazhi_i_përdoruesit or "pacim" in mesazhi_i_përdoruesit:
        return "Mirupafshim! Shpresoj që të keni një ditë të shkëlqyer!"
    elif "sygjerime" in mesazhi_i_përdoruesit or "sygjero" in mesazhi_i_përdoruesit:
        return "Ju sygjeroj disa nga makinat me te preferuara nga klientet tane si Rolls Royce, Audi, Mercedes, BMW, Prosche"
    elif "prenotoj" in mesazhi_i_përdoruesit or "prenotim" in mesazhi_i_përdoruesit or "pagesa" in mesazhi_i_përdoruesit or "paguaj" in mesazhi_i_përdoruesit or "rezervoj" in mesazhi_i_përdoruesit:
        return "Mund te prenotoni Online ose Fizikisht. Si deshironi?"
    elif "online" in mesazhi_i_përdoruesit or "paguaj online" in mesazhi_i_përdoruesit:
        return "Per te prenotuar online ndiqni linku-n www.paypal.al"
    elif "fizikisht" in mesazhi_i_përdoruesit or "fizik" in mesazhi_i_përdoruesit or "adresa" in mesazhi_i_përdoruesit:
        return "Per te paguar fizikisht ose per te pare makinat nga afer ju lutem paraqituni prane 21 Dhjetori perball BKT Bank"
    elif "familjare" in mesazhi_i_përdoruesit or "ekonomike" in mesazhi_i_përdoruesit or "familje" in mesazhi_i_përdoruesit or "ekonomik" in mesazhi_i_përdoruesit:
        return "Nje makine qe kemi per ju eshte Toyota Corolla 2019 1.4 Nafte, per vetem 40 Euro  "
    elif "dasma" in mesazhi_i_përdoruesit or "dasem" in mesazhi_i_përdoruesit or "raste" in mesazhi_i_përdoruesit or "fejese" in mesazhi_i_përdoruesit:
        return "Si thoni per nje Rolls Royce Phantom 2022? Cfare marke deshironi ju?"
    elif "ok" in mesazhi_i_përdoruesit:
        return "Kenaqesi të të asistoja."
    else:
        return "Më vjen keq, nuk e kuptova mirë. Mund ta riformuloni atë?"

# Route to handle chatbot messages
@app.route('/api/message', methods=['POST'])
def merr_mesazhin():
    mesazhi_i_përdoruesit = request.json.get('message')
    if not mesazhi_i_përdoruesit:
        return jsonify({"error": "Nuk është dërguar asnjë mesazh"}), 400
    
    përgjigja_e_botit = merr_përgjigje_bot(mesazhi_i_përdoruesit)
    
    return jsonify({"response": përgjigja_e_botit})

# Route to submit ratings
@app.route('/api/rating', methods=['POST'])
def post_rating():
    try:
        data = request.get_json()
        rating_value = data.get("rating", None)
        
        if rating_value is not None and 1 <= rating_value <= 5:
            # Load current ratings from the file
            ratings = load_ratings()
            
            # Add new rating
            ratings.append({"rating": rating_value, "time": data.get("time", None)})
            
            # Save updated ratings to the file
            save_ratings(ratings)
            
            return jsonify({"message": "Rating saved successfully!"}), 200
        else:
            return jsonify({"message": "Invalid rating. Rating must be between 1 and 5."}), 400
    except Exception as e:
        print(f"Error saving rating: {e}")
        return jsonify({"message": "Error saving rating"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
