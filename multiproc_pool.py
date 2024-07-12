import multiprocessing
import time
import os
import string


def get_txt_files(directory): # знаходимо всі txt-файли в каталозі
    if not os.path.exists(directory):
        print(f"Каталог {directory} не існує.")
        return []
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt')]

def clean_text(text): # приводимо до нижнього регістру та видаляємо символи пунктуації
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

def search_keywords_in_file(file_path, keywords):
    results = {keyword: [] for keyword in keywords}
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        text = clean_text(text)
        for keyword in keywords:
            if keyword in text:
                results[keyword].append(file_path)
    return results

def multiprocess_keyword_search(files, keywords, num_processes):
    with multiprocessing.Pool(num_processes) as pool:
        results = pool.starmap(search_keywords_in_file, [(file, keywords) for file in files])

    aggregated_results = {keyword: [] for keyword in keywords}
    for result in results:
        for keyword, file_paths in result.items():
            aggregated_results[keyword].extend(file_paths)

    return aggregated_results

if __name__ == "__main__":

    files = get_txt_files("files") # каталог з файлами
    if not files:
        exit()

    keywords = ["python", "модуль", "процесс"] # слова для пошуку
    num_processes = os.cpu_count()  # кількість процесів на рівні кількості ядер

    start_time = time.time()
    multiprocess_results = multiprocess_keyword_search(files, keywords, num_processes)
    end_time = time.time()

    print("Multiprocess results (pool):", multiprocess_results)
    print("Multiprocess execution time:", end_time - start_time, "seconds")
