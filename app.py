from flask import Flask, request, send_file, render_template
import json
import os
from waitress import serve

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Debugging print statements
        print("Received POST request")
        print(f"Form data: {request.form}")

        try:
            name = request.form['name']
            grid_data = request.form['grid_data']
            width = int(request.form['width'])
            height = int(request.form['height'])

            # Debugging print statements
            print(f"Name: {name}")
            print(f"Width: {width}, Height: {height}")
            print(f"Grid data: {grid_data}")

            grid = json.loads(grid_data)
            if not isinstance(grid, list) or not all(isinstance(row, list) for row in grid):
                raise ValueError('Invalid grid data')

            # Generate .gate file content
            gate_content = f"Width: {width}\nHeight: {height}\n"
            for row in grid:
                gate_content += ' '.join(row) + '\n'

            # Save the content to a .gate file
            gate_filename = f"{name}.gate"
            with open(gate_filename, 'w') as file:
                file.write(gate_content)

            return send_file(gate_filename, as_attachment=True)

        except KeyError as e:
            return f"Missing data: {e}", 400
        except (json.JSONDecodeError, ValueError) as e:
            return f"Error: {e}", 400

    return render_template('index.html')


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8002)
