import io
import wave

from flask import jsonify, request, url_for, send_file
from pydub import AudioSegment

from models import db, AudioFile, Users


def init_routes(app):
    @app.route('/record', methods=['GET'])
    def download_audio():
        user_id = request.args.get('user')
        audio_id = request.args.get('id')
        audio_data = db.session.query(AudioFile).filter_by(id=audio_id).filter_by(user_id=user_id).first().audio_data

        mp3_stream = io.BytesIO(audio_data)
        audio_segment = AudioSegment.from_file(mp3_stream, format='mp3')
        file_like_object = io.BytesIO()
        audio_segment.export(file_like_object, format='mp3')

        return send_file(file_like_object, mimetype='audio/mpeg', as_attachment=True,
                         download_name='audio_file.mp3')

    @app.route('/api/users', methods=['POST'])
    def create_user():
        username = request.json['username']
        user_exists = db.session.query(Users).filter_by(name=username).first() is not None
        if not user_exists:
            user = Users(name=username)
            db.session.add(user)
            db.session.commit()
            response = jsonify({'user_id': user.id, 'access_token': user.uuid})
            response.status_code = 200
            return response
        else:
            response = jsonify({'error': 'User already exists'})
            response.status_code = 409
            return response

    @app.route("/api/upload", methods=['POST'])
    def upload_file():
        user_id = request.form['user_id']
        access_token = request.form['access_token']
        audio_file = request.files['audio_file']

        if not verify_access_token(user_id, access_token):
            return {'error': 'Invalid access token'}

        audio_content = process_audio(audio_file)

        new_audio_record = AudioFile(user_id=user_id, audio_data=audio_content)
        db.session.add(new_audio_record)
        db.session.commit()

        return url_for('download_audio', id=f'{new_audio_record.id}', user=f'{new_audio_record.user_id}',
                       _external=True)

    def verify_access_token(user_id, access_token):
        user = db.session.query(Users).filter(Users.id == user_id).first()
        if user:
            return access_token == user.uuid
        else:
            return False

    def process_audio(audio_content):
        audio_bytes = audio_content.read()
        wav_stream = io.BytesIO(audio_bytes)
        with wave.open(wav_stream, "rb") as wav_file:
            channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            frame_rate = wav_file.getframerate()
            frames = wav_file.readframes(wav_file.getnframes())

        audio = AudioSegment(
            data=frames,
            sample_width=sample_width,
            frame_rate=frame_rate,
            channels=channels
        )
        mp3_stream = io.BytesIO()
        audio.export(mp3_stream, format='mp3')

        return mp3_stream.getvalue()

    @app.route('/')
    def hello_world():
        return 'Hello World!'
