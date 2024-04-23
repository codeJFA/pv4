from tqdm import tqdm
import time

def init_progress_bar(total):
    return tqdm(total=total, desc="Betöltés", colour='white')

def update_progress_bar(progress_bar):
    progress_bar.update(1)

def close_progress_bar(progress_bar):
    progress_bar.close()

def simulate_loading(loading_time):
    progress_bar = init_progress_bar(loading_time)
    for _ in range(loading_time):
        time.sleep(0.21)
        update_progress_bar(progress_bar)
    close_progress_bar(progress_bar)
    print("A betöltés befejeződött!")
