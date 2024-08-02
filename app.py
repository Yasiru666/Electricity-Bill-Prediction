from flask import Flask, request, render_template
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import matplotlib

# Set matplotlib backend to Agg
matplotlib.use('Agg')

app = Flask(__name__)

def process_csv_and_graph(file):
    try:
        df = pd.read_csv(file)
        
        if 'Value' not in df.columns or 'Category' not in df.columns:
            return None, "CSV file must contain 'Category' and 'Value' columns."
        
        # Use only the last 5 rows
        dff = df.tail()
        
        plt.figure(figsize=(6, 4), dpi=100)
        plt.plot(dff['Category'], dff['Value'], marker='o', linestyle='-', color='b', linewidth=2, markersize=8, markerfacecolor='r', markeredgewidth=2)

        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.title('Sample Line Chart', fontsize=14, fontweight='bold')
        plt.xlabel('Category', fontsize=12)
        plt.ylabel('Value', fontsize=12)

        for i in range(len(df)):
            plt.text(dff['Category'][i], dff['Value'][i], f'{dff["Value"][i]}', fontsize=9, ha='right')

        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plot_data = buffer.getvalue()
        plt.close()

        encoded_image = base64.b64encode(plot_data).decode('utf-8')
        return encoded_image, None
    except Exception as e:
        return None, str(e)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    graph_data = None
    message = None

    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', message='No file part')
        
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', message='No selected file')

        if file:
            graph_data, message = process_csv_and_graph(file)

    return render_template('index.html', graph_data=graph_data, message=message)

if __name__ == '__main__':
    app.run(debug=True)
