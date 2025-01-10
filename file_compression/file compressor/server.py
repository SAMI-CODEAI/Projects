from flask import Flask, request, send_file
from io import BytesIO
import gzip

app = Flask(__name__)

@app.route('/compress', methods=['POST'])
def compress_file():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    file_contents = file.read()

    # Compress the file using gzip
    compressed_data = BytesIO()
    with gzip.GzipFile(mode='wb', fileobj=compressed_data) as f:
        f.write(file_contents)

    compressed_data.seek(0)

    return send_file(compressed_data, mimetype='application/gzip', as_attachment=True,
                     download_name=f'{file.filename}.gz')

if __name__ == '__main__':
    app.run(debug=True)