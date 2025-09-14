import re
import argparse
import yt_dlp
import os

def parse_vtt(vtt_content):
    segments = []
    blocks = re.split(r'\n\n', vtt_content.strip())
    
    if blocks and blocks[0].startswith("WEBVTT"):
        blocks = blocks[1:]

    for block in blocks:
        if not block.strip():
            continue

        lines = block.split('\n')
        
        time_line = ""
        text_lines = []
        for line in lines:
            if "-->" in line:
                time_line = line
            elif line.strip() and not line.startswith("NOTE"):
                text_lines.append(line)
        
        if not time_line or not text_lines:
            continue

        times = re.findall(r'(\d{2}:\d{2}:\d{2}\.\d{3})', time_line)
        if len(times) == 2:
            start_time_str, end_time_str = times
            
            text = " ".join(text_lines)
            text = re.sub(r'<[^>]+>', '', text)
            text = re.sub(r'\s+', ' ', text).strip()
            
            segments.append({
                "start": start_time_str,
                "end": end_time_str,
                "text": text
            })
    return segments

def download_subtitles(youtube_url, output_dir=".", lang="en"):
    ydl_opts = {
        'writesubtitles': True,
        'subtitlesformat': 'vtt',
        'subtitleslangs': [lang],
        'skip_download': True, # Only download subtitles, not video
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        video_title = info_dict.get('title', 'unknown_video')
        
        # Extract 'day X' from the video title
        match = re.search(r'[Dd]ay\s*(\d+)', video_title)
        day_number = match.group(1) if match else 'unknown'
        
        subtitle_filename_base = f"subtitles_day_{day_number}"
        expected_subtitle_file = os.path.join(output_dir, f"{subtitle_filename_base}.{lang}.vtt")
        
        if os.path.exists(expected_subtitle_file):
            print(f"Субтитры для 'day {day_number}' уже существуют: {expected_subtitle_file}. Пропускаем скачивание.")
            return expected_subtitle_file, day_number
        
        print(f"Скачивание субтитров для видео: {video_title} (day {day_number})...")
        # Update outtmpl to ensure correct naming for subtitles
        ydl_opts['outtmpl'] = os.path.join(output_dir, f"{subtitle_filename_base}")
        ydl_opts['skip_download'] = True # Still skip video download
        ydl_opts['writesubtitles'] = True # Ensure subtitles are written
        ydl_opts['writeautomaticsub'] = True # Also try to download automatic subtitles

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl_download:
                ydl_download.download([youtube_url])
        except Exception as e:
            print(f"Ошибка при скачивании субтитров: {e}")
            return None, day_number
        
        # After download, yt-dlp might save with .vtt.en.vtt or just .en.vtt, need to check
        # Let's try to find the actual downloaded file based on the expected pattern
        # yt-dlp usually adds the language code and then the extension
        actual_subtitle_file = os.path.join(output_dir, f"{subtitle_filename_base}.{lang}.vtt")
        
        if os.path.exists(actual_subtitle_file):
            print(f"Субтитры успешно скачаны: {actual_subtitle_file}")
            return actual_subtitle_file, day_number
        else:
            print(f"Ошибка: Не удалось найти скачанные субтитры для 'day {day_number}' по пути: {actual_subtitle_file}. Проверьте, были ли они скачаны и их точное имя.")
            # Fallback: try to find any .vtt file that starts with the base name
            downloaded_files = [f for f in os.listdir(output_dir) if f.startswith(subtitle_filename_base) and f.endswith(".vtt")]
            if downloaded_files:
                print(f"Найдены субтитры с другим именем: {downloaded_files[0]}. Используем его.")
                return os.path.join(output_dir, downloaded_files[0]), day_number
            else:
                return None, day_number

def main():
    parser = argparse.ArgumentParser(description="Скачивание и очистка субтитров YouTube-видео.")
    parser.add_argument("youtube_url", type=str, help="URL YouTube-видео.")
    args = parser.parse_args()
    
    youtube_url = args.youtube_url
    
    # Download subtitles or get existing path
    subtitle_file_path, day_number = download_subtitles(youtube_url)
    if not subtitle_file_path:
        print("Не удалось получить файл субтитров. Выход.")
        return

    cleaned_output_file_path = f"./cleaned_subtitles_day_{day_number}.txt"

    try:
        with open(subtitle_file_path, "r", encoding="utf-8") as f:
            vtt_content = f.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл субтитров не найден по пути: {subtitle_file_path}")
        return
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return

    segments = parse_vtt(vtt_content)

    if not segments:
        print("Не удалось распарсить сегменты субтитров. Выходной файл не будет создан.")
        return

    try:
        with open(cleaned_output_file_path, "w", encoding="utf-8") as outfile:
            for s in segments:
                outfile.write(f"{s['start']} --> {s['end']}\n")
                outfile.write(f"{s['text']}\n\n")
        print(f"Очищенные субтитры сохранены в файл: {cleaned_output_file_path}")
    except Exception as e:
        print(f"Ошибка при записи в выходной файл: {e}")

if __name__ == "__main__":
    main()
