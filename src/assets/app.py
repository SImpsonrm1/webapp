# Required Packages
# pip install 'torch>=2.0'
# pip install -U audiocraft
def main():

    # facebook/musicgen-small  - 300M transformer decoder.
    # facebook/musicgen-medium - 1.5B transformer decoder.
    # facebook/musicgen-melody - 1.5B transformer decoder also supporting melody conditioning.
    # facebook/musicgen-large  - 3.3B transformer decoder.

    MODELS = ['small', 'medium', 'melody', 'large']
    MODEL = MODELS[0]

    from audiocraft.models import MusicGen
    from audiocraft.models import MultiBandDiffusion

    USE_DIFFUSION_DECODER = False
    # Using small model, better results would be obtained with `medium` or `large`.
    model = MusicGen.get_pretrained(f'facebook/musicgen-{MODEL}')
    if USE_DIFFUSION_DECODER:
        mbd = MultiBandDiffusion.get_mbd_musicgen()

    DURATION = int(input("\nDuration (seconds): "))
    description = input("Description: ")
    print(f"Generating... (Should take about {DURATION * 2} seconds)")


    model.set_generation_params(
        use_sampling=True,
        top_k=250,
        duration=DURATION
    )

    output = model.generate(
        descriptions=[
            #'80s pop track with bassy drums and synth',
            #'90s rock song with loud guitars and heavy drums',
            #'Progressive rock drum and bass solo',
            #'Punk Rock song with loud drum and power guitar',
            #'Bluesy guitar instrumental with soulful licks and a driving rhythm section',
            #'Jazz Funk song with slap bass and powerful saxophone'
            #'drum and bass beat with intense percussions'
            description
        ],
        progress=True, return_tokens=True
    )

    import scipy
    print(output)
    # Save to output directory
    outfile_name = description.replace(" ", "_") + '.wav'
    sampling_rate = model.sample_rate
    scipy.io.wavfile.write(('output\\' + outfile_name), rate=sampling_rate, data=output[0].cpu().numpy())
    print(f"Done Generating.\nSaved to {outfile_name}")

    import matplotlib.pyplot as plt
    import librosa
    import numpy as np

    wave = (output[0].cpu().numpy()).flatten()

    print(wave.flatten())

    fig, ax = plt.subplots(2)
    fig.set_figheight(6)
    fig.set_figwidth(10)
    ax[1].plot(wave)
    ax[1].set_xlim(0, len(wave))
    ax[1].set_title('Waveform')
    ax[1].set_xlabel('Samples')
    ax[1].set_ylabel('Amplitude')

    S = librosa.stft(wave, hop_length=512)

    S_dB = librosa.amplitude_to_db(np.abs(S), ref=np.max)

    img = librosa.display.specshow(S_dB, x_axis='time',
                                y_axis='log', ax=ax[0], sr=sampling_rate)
    ax[0].set_title('Log Spectra')

    onset_env = librosa.onset.onset_strength(y=wave, sr=sampling_rate)
    tempo = librosa.feature.tempo(onset_envelope=onset_env, sr=sampling_rate)
    tempo = np.round(tempo, 2)[0]

    plt.suptitle(f"'{description}' - Tempo: {tempo} bpm", fontsize=15)
    plt.tight_layout()
    plt.savefig(('output\\' + outfile_name))

if __name__ == '__main__':
    main()
