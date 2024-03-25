from flask import Flask, request, jsonify
from flask_cors import CORS

import main

app = Flask(__name__)
CORS(app, resources={r"/upload": {"origins": ["http://localhost:4200"]}})

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        file = request.files['file']
        if file:
            file_path = 'uploaded_image.jpg'
            file.save(file_path)

            personal_information = main.getInfoFromCI(file_path)

            return jsonify(personal_information)

        return jsonify({'error': 'No file provided'})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
