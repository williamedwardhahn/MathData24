from flask import Flask, render_template_string, request, redirect, url_for, send_file
import matplotlib.pyplot as plt
import io
app = Flask(__name__)

# Status dictionary to store the state of each light
status = {"light1": "OFF", "light2": "OFF"}

# HTML template for the dashboard
template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Demo Dashboard</title>
    <style>
        .status-light {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: inline-block;
            margin: 10px;
        }
        .green { background-color: green; }
        .red { background-color: red; }
    </style>
</head>
<body>
    <h1>Simple Demo Dashboard</h1>
    <div>
        <h2>Light 1: <span class="status-light {{ 'green' if status['light1'] == 'ON' else 'red' }}"></span></h2>
        <form action="{{ url_for('toggle_light', light='light1') }}" method="post">
            <button type="submit">Toggle Light 1</button>
        </form>
    </div>
    <div>
        <h2>Light 2: <span class="status-light {{ 'green' if status['light2'] == 'ON' else 'red' }}"></span></h2>
        <form action="{{ url_for('toggle_light', light='light2') }}" method="post">
            <button type="submit">Toggle Light 2</button>
        </form>
    </div>

    <h2>Enter 10 Numbers to Plot as Bar Graph</h2>
    <form action="{{ url_for('plot_graph') }}" method="post">
        {% for i in range(10) %}
            <input type="number" name="numbers" required>
        {% endfor %}
        <button type="submit">Go</button>
    </form>

    <div>
        {% if graph_url %}
            <img src="{{ graph_url }}" alt="Bar Graph">
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(template, status=status, graph_url=None)

@app.route("/toggle/<light>", methods=["POST"])
def toggle_light(light):
    if light in status:
        status[light] = "ON" if status[light] == "OFF" else "OFF"
    return redirect(url_for("home"))

@app.route("/plot_graph", methods=["POST"])
def plot_graph():
    numbers = request.form.getlist("numbers")
    numbers = list(map(float, numbers))  # Convert to floats

    # Generate bar graph
    fig, ax = plt.subplots()
    ax.bar(range(1, 11), numbers)
    ax.set_xlabel("Index")
    ax.set_ylabel("Value")
    ax.set_title("Bar Graph of Input Numbers")

    # Save plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)

    # Serve the generated image
    return send_file(buf, mimetype="image/png")

# Expose the app via ngrok
public_url = ngrok.connect(5000)
print("Dashboard URL:", public_url)

app.run(port=5000)
