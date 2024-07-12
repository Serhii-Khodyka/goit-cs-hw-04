import threading
import time
import os
import string
from math import ceil

def get_txt_files(directory): # знаходимо всі txt-файли в каталозі
    if not os.path.exists(directory):
        print(f"Каталог {directory} не існує.")
        return []
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt')]

def clean_text(text): # приводимо до нижнього регістру та видаляємо символи пунктуації
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

def search_keywords_in_files(file_paths, keywords, results):
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            text = clean_text(text)
            for keyword in keywords:
                if keyword in text:
                    results[keyword].append(file_path)

def threaded_keyword_search(files, keywords, num_threads):
    threads = []
    results = {keyword: [] for keyword in keywords}

    chunk_size = ceil(len(files) / num_threads)
    file_chunks = [files[i:i + chunk_size] for i in range(0, len(files), chunk_size)]

    for i, file_chunk in enumerate(file_chunks):
        thread = threading.Thread(target=search_keywords_in_files, args=(file_chunk, keywords, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results


if __name__ == "__main__":

    files = get_txt_files("files") # каталог з файлами
    if not files:
        exit()
        
    keywords = ["python", "модуль", "процесс"] # слова для пошуку
    num_threads = os.cpu_count()  # кількість потоків на рівні кількості ядер

    start_time = time.time()
    threaded_results = threaded_keyword_search(files, keywords, num_threads)
    end_time = time.time()

    print("Threaded results:", threaded_results)
    print("Threaded execution time:", end_time - start_time, "seconds")
