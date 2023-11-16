from flask import Flask, jsonify, request, send_from_directory, send_file
import os
from audiocraft.models import MusicGen, MultiBandDiffusion
import scipy.io.wavfile
import librosa
import numpy as np
import matplotlib.pyplot as plt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/generate-music', methods=['POST'])
def generate_music():
    data = request.json
    duration = data.get('duration', 30)
    description = data.get('description', 'Music')

    # Initialize the model
    model = MusicGen.get_pretrained('facebook/musicgen-small')
    model.set_generation_params(use_sampling=True, top_k=250, duration=duration)

    # Generate music
    output = model.generate(descriptions=[description], progress=True, return_tokens=True)

    # Define the file path
    outfile_name = description.replace(" ", "_") + '.wav'
    output_path = os.path.join('static', 'generated', outfile_name)

    # Save the output as a WAV file
    scipy.io.wavfile.write(output_path, rate=model.sample_rate, data=output[0].cpu().numpy())

    #Generate and save the waveform plot as an image

    wave = (output[0].cpu().numpy()).flatten()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(wave)
    ax.set_xlim(0, len(wave))
    ax.set_title('Waveform')
    plt.savefig(output_path.replace('.wav', '.png'))

    # Return the name of the generated file (excluding the 'static' part)
    return jsonify({'message': 'Music generated successfully', 'file': outfile_name.replace('.wav', '')})

@app.route('/generated/<path:filename>', methods=['GET'])
def generated_files(filename):
    return send_from_directory('static/generated', filename)

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Flask server is running!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
