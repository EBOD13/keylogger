import pyaudio
from flask import Flask, Response, render_template

app = Flask(__name__, template_folder="template")

# Audio streaming parameters
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024

# Initialize PyAudio
audio_stream = pyaudio.PyAudio()


# Generate the header for the streaming
def genHeader(sample_rate, bits_per_sample, channels):
    """
    Generates a WAV file header.

    Args:
        sample_rate (int): The sampling rate in Hz (e.g., 44100).
        bits_per_sample (int): The number of bits per sample (e.g., 16 for PCM).
        channels (int): The number of audio channels (e.g., 1 for mono, 2 for stereo).

    Returns:
        bytes: The generated WAV file header as a byte string.
    """

    datasize = 2000 * 10 ** 6  # Arbitrary large data size
    stream_audio = bytes("RIFF", "ascii")  # Marks file as RIFF
    stream_audio += (datasize + 36).to_bytes(4, 'little')  # File size in bytes
    stream_audio += bytes("WAVE", 'ascii')  # File type
    stream_audio += bytes("fmt ", 'ascii')  # Format Chunk Marker
    stream_audio += (16).to_bytes(4, 'little')  # Length of the above format data
    stream_audio += (1).to_bytes(2, 'little')  # Format type (1 is PCM)
    stream_audio += channels.to_bytes(2, 'little')  # Number of channels
    stream_audio += sample_rate.to_bytes(4, 'little')  # Sample rate
    stream_audio += (sample_rate * channels * bits_per_sample // 8).to_bytes(4, 'little')  # Byte rate
    stream_audio += (channels * bits_per_sample // 8).to_bytes(2, 'little')  # Block align
    stream_audio += bits_per_sample.to_bytes(2, 'little')  # Bits per sample
    stream_audio += bytes("data", "ascii")  # Data Chunk Marker
    stream_audio += datasize.to_bytes(4, 'little')  # Data size
    return stream_audio


def Sound():
    bits_per_sample = 16
    wav_header = genHeader(RATE, bits_per_sample, CHANNELS)
    stream = audio_stream.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    first_run = True
    while True:
        try:
            if first_run:
                data = wav_header + stream.read(CHUNK)
                first_run = False
            else:
                data = stream.read(CHUNK)
            yield data
        except Exception as e:
            print(f"Audio stream error: {e}")
            break


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/audio")
def audio():
    return Response(Sound(), mimetype="audio/aac",
                    headers={"Cache-Control": "no-cache", "Transfer-Encoding": "chunked"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5454, threaded=True)
