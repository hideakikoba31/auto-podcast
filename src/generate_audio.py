import os
from google.cloud import texttospeech

def synthesize_speech(text, output_filename="assets/raw_audio.mp3"):
    """
    Google Cloud Text-to-Speechを使用して、テキストから音声を生成します。
    ※事前にGOOGLE_APPLICATION_CREDENTIALS環境変数の設定が必要です。
    """
    # クライアントの初期化（環境変数 GOOGLE_APPLICATION_CREDENTIALS のJSONキーを自動で読み込みます）
    client = texttospeech.TextToSpeechClient()

    # 入力テキストの設定
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # 音声のパラメーター設定
    # Neural2-B は落ち着いた女性の声（やわらかいトーンに合います）
    voice = texttospeech.VoiceSelectionParams(
        language_code="ja-JP",
        name="ja-JP-Neural2-B"
    )

    # 出力する音声ファイルの形式（MP3）と、話すスピードなどを設定
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.1,  # 少しだけテンポ良く
        pitch=0.0           # ピッチは標準
    )

    # APIリクエストを実行して音声を生成
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # 音声データをファイルに保存
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        
    print(f"Audio content written to file '{output_filename}'")
    return output_filename

if __name__ == "__main__":
    # テスト用
    sample_text = "おはようございます。本日は晴天なり。朝のコーヒーブレイクにぴったりの話題をお届けします。"
    try:
        synthesize_speech(sample_text)
    except Exception as e:
        print(f"Error during TTS: {e}")
