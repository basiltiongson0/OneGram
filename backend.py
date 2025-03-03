from flask import Flask,request,jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={
    r"/*": {
        "origins": ["http://127.0.0.1:5501"],  # Your frontend URL
        "methods": ["GET", "POST", "OPTIONS"],  # Allowed methods
        "allow_headers": ["Content-Type"]       # Allowed headers
    }
})

# @app.route('/name', methods=['POST', 'GET','PUT','DELETE'])

# Load Firebasekey JSON file
cred = credentials.Certificate("spark-91799-firebase-adminsdk-fbsvc-50fa19bc6b.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore (NoSQL Database)
db = firestore.client()

@app.route('/')
def root():
    return ''

#this function captures the request to save the data to firebase
@app.route('/save-settings', methods=['POST'])
def save_settings():
    data = request.json
    profile_id = data.get('userID')
    
    db.collection("settings").document(profile_id).set(data)
    return jsonify({"message": "Settings saved successfully"})

#this gets the layout from the firebase, 
# should be called when rendering profile page
@app.route('/get-settings', methods = ['GET','OPTIONS'])
def get_settings():
    user_id = request.args.get('userID')

    if not user_id:
        return jsonify({'error': 'User ID Required'}),400
    # print("running")
    doc = db.collection('settings').document(user_id).get()
    # print("ran")
    return jsonify(doc.to_dict())

#this saves the theme for the user profile
@app.route('/save-theme',methods=['POST'])
def save_theme():
    data = request.json
    profile_id = data.get('userID')
    db.collection("themes").document(profile_id).set(data)
    return jsonify({"message": "Theme saved successfully"})

    
#this gets the theme for the user's profile
@app.route('/get-theme',methods=['GET','OPTIONS'])
def get_theme():
    user_id = request.args.get('userID')

    if not user_id:
        return jsonify({'error': 'User ID Required'}),400
    
    doc = db.collection('themes').document(user_id).get()

    return jsonify(doc.to_dict())

@app.route('/get-communities-info',methods=['GET'])
def get_communities():
    community_id = request.args.get('communities')

    if not community_id:
        return jsonify({'error': 'User ID Required'}),400
    
    doc = db.collection('communities').document(community_id).get()

    return jsonify(doc.to_dict())

@app.route('/add-community',methods=['POST'])
def add_community():
    community_id = request.args.get("community")
    data = request.json
    if not community_id:
        return jsonify({'error': 'User ID Required'}),400
    db.collection("communities").document(community_id).set(data)
    return jsonify({"message": "Community saved successfully"})

@app.route('/set-page-num',methods=['POST'])
def set_page_num():
    data = request.json
    print(data)

    if not data:
        return jsonify({"error":"Community Required"})
    print("HELLO")
    db.collection('page').document("temp").set(data)
    print("HI")
    return jsonify({"message": "Community saved successfully"})

@app.route('/get-page-type',methods=['GET'])
def get_page_type():
    doc = db.collection('page').document("temp").get()
    return jsonify(doc.to_dict())

if __name__ == "__main__":
    app.run()
