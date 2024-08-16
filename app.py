from flask import Flask, render_template, request, send_file
import os
from waitress import serve

app = Flask(__name__)

# Define the structure of the .gate file based on the selected grid
def generate_gate_file(name, size, grid_data):
    gate_content = f"""
# {name} Gate Configuration
name: {name}
size: {size}
"""
    for row in grid_data:
        gate_content += ' '.join(row) + '\n'

    file_name = f"{name}.gate"
    with open(file_name, 'w') as file:
        file.write(gate_content.strip())
    return file_name

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        size = int(request.form['size'])
        grid_data = request.form.getlist('grid_data[]')

        # Generate .gate file
        gate_file = generate_gate_file(name, size, grid_data)

        # Send the file to the user for download
        return send_file(gate_file, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    # Serve the application using Waitress
    serve(app, host='0.0.0.0', port=8000)
