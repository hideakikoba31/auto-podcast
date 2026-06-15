import os
from pydub import AudioSegment

def mix_audio_with_bgm(voice_file, bgm_file, output_file="assets/final_episode.mp3"):
    """
    生成された音声データ（voice_file）とBGM（bgm_file）を合成します。
    BGMは音声の長さに合わせてループし、音量を調整して背景で流れるようにします。
    """
    if not os.path.exists(voice_file):
        raise FileNotFoundError(f"Voice file not found: {voice_file}")
    
    if not os.path.exists(bgm_file):
        print(f"Warning: BGM file not found: {bgm_file}. Proceeding without BGM.")
        # BGMがない場合はそのままコピー
        voice = AudioSegment.from_mp3(voice_file)
        voice.export(output_file, format="mp3")
        return output_file

    # 音声とBGMを読み込み
    voice = AudioSegment.from_mp3(voice_file)
    bgm = AudioSegment.from_mp3(bgm_file)

    # BGMの音量を下げる（-15dB〜-20dB程度が自然）
    bgm = bgm - 18

    # 音声の長さに合わせてBGMをループまたはカット
    voice_duration = len(voice)
    
    # BGMが短い場合はループさせて長くする
    while len(bgm) < voice_duration:
        bgm += bgm
        
    # 音声の長さにぴったり合わせる
    bgm = bgm[:voice_duration]
    
    # BGMにフェードイン・フェードアウトを追加（最初と最後の2秒間）
    bgm = bgm.fade_in(2000).fade_out(2000)

    # 音声とBGMを合成 (overlay)
    final_audio = bgm.overlay(voice)

    # エクスポート
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    final_audio.export(output_file, format="mp3")
    print(f"Mixed audio saved to '{output_file}'")
    
    return output_file

if __name__ == "__main__":
    # テスト用
    mix_audio_with_bgm("assets/raw_audio.mp3", "assets/bgm.mp3")
