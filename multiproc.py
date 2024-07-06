import multiprocessing
import time
import os
import string
from math import ceil

def get_txt_files(directory): # знаходимо всі txt-файли в каталозі
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt')]

def clean_text(text): # приводимо до нижнього регістру та видаляємо символи пунктуації
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

def search_keywords_in_files_mp(file_paths, keywords, result_queue):
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            text = clean_text(text)
            for keyword in keywords:
                if keyword in text:
                    result_queue.put((keyword, file_path))

def multiprocess_keyword_search(files, keywords, num_processes):
    processes = []
    result_queue = multiprocessing.Queue()

    chunk_size = ceil(len(files) / num_processes)
    file_chunks = [files[i:i + chunk_size] for i in range(0, len(files), chunk_size)]

    for i, file_chunk in enumerate(file_chunks):
        process = multiprocessing.Process(target=search_keywords_in_files_mp, args=(file_chunk, keywords, result_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    results = {keyword: [] for keyword in keywords}
    while not result_queue.empty():
        keyword, file_path = result_queue.get()
        results[keyword].append(file_path)

    return results


if __name__ == "__main__":

    files = get_txt_files("files") # каталог з файлами
    keywords = ["python", "модуль", "процесс"] # слова для пошуку
    num_processes = os.cpu_count()  # кількість процесів на рівні кількості ядер

    start_time = time.time()
    multiprocess_results = multiprocess_keyword_search(files, keywords, num_processes)
    end_time = time.time()

    print("Multiprocess results:", multiprocess_results)
    print("Multiprocess execution time:", end_time - start_time, "seconds")
