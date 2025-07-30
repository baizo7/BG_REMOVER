from flask import Flask, request, send_file, render_template
from rembg import remove
import io
import os

# Debug print to verify app is loading on Render
print("==== Flask app is being loaded ====")

# Create Flask app instance
app = Flask(__name__, template_folder="../templates")

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Route to remove background
@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return 'No file uploaded', 400

    file = request.files['image']
    input_image = file.read()
    try:
        output_image = remove(input_image)
        return send_file(
            io.BytesIO(output_image),
            mimetype='image/png',
            download_name='output.png'
        )
    except Exception as e:
        print("Error during image processing:", e)
        return 'Error processing image', 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
    app.run(host='0.0.0.0', port=port, debug=debug)
