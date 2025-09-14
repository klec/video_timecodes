import re
import argparse
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

def main():
    parser = argparse.ArgumentParser(description="Очистка VTT-файла субтитров, оставляя только таймкоды и текст.")
    parser.add_argument("input_file", type=str, help="Путь к входному VTT-файлу.")
    parser.add_argument("output_file", type=str, help="Путь к выходному очищенному файлу.")
    args = parser.parse_args()

    input_file_path = args.input_file
    output_file_path = args.output_file

    if not os.path.exists(input_file_path):
        print(f"Ошибка: Входной файл не найден по пути: {input_file_path}")
        return

    try:
        with open(input_file_path, "r", encoding="utf-8") as f:
            vtt_content = f.read()
    except Exception as e:
        print(f"Ошибка при чтении входного файла: {e}")
        return

    segments = parse_vtt(vtt_content)

    if not segments:
        print("Не удалось распарсить сегменты субтитров. Выходной файл не будет создан.")
        return

    try:
        with open(output_file_path, "w", encoding="utf-8") as outfile:
            for s in segments:
                outfile.write(f"{s['start']} --> {s['end']}\n")
                outfile.write(f"{s['text']}\n\n")
        print(f"Очищенные субтитры сохранены в файл: {output_file_path}")
    except Exception as e:
        print(f"Ошибка при записи в выходной файл: {e}")

if __name__ == "__main__":
    main()
