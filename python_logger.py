import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Değişiklikleri kaydedeceğimiz dosyanın yolu
log_file_path = "/home/ubuntu/bsm/logs/changes.json"

# İzlenecek dizin
watch_directory = "/home/ubuntu/bsm/test"

# JSON dosyasını yükleyip, mevcut verileri okuyalım
def load_log():
    try:
        with open(log_file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# JSON dosyasına verileri yazma fonksiyonu
def save_log(data):
    with open(log_file_path, "w") as f:
        json.dump(data, f, indent=4)

# Dosya sistemi olaylarını dinleyecek sınıf
class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            self.record_change(event, "modified")

    def on_created(self, event):
        if not event.is_directory:
            self.record_change(event, "created")

    def on_deleted(self, event):
        if not event.is_directory:
            self.record_change(event, "deleted")

    def record_change(self, event, event_type):
        # Olayın kaydedilmesi
        event_data = {
            "event_type": event_type,
            "file": event.src_path,
            "timestamp": time.time()
        }
        
        # JSON dosyasındaki mevcut verileri yükleyelim
        logs = load_log()
        logs.append(event_data)
        
        # Yeni log verisini JSON dosyasına kaydedelim
        save_log(logs)
        print(f"{event_type.capitalize()} event: {event.src_path}")

# İzleme başlatma fonksiyonu
def start_watching():
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, watch_directory, recursive=False)
    
    # İzlemeyi başlat
    observer.start()
    print(f"Watching directory: {watch_directory}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("Stopping observer...")
    observer.join()

if __name__ == "__main__":
    start_watching()
