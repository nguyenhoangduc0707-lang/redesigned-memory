import os
import shutil

def cleanup():
    print("Cleaning uploads/ directory...")
    uploads_dir = "uploads"
    if os.path.exists(uploads_dir):
        for item in os.listdir(uploads_dir):
            item_path = os.path.join(uploads_dir, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        print("Uploads cleaned.")
    else:
        print("No uploads directory found.")

    print("Removing Python cache files...")
    for root, dirs, files in os.walk("."):
        if "__pycache__" in dirs:
            cache_path = os.path.join(root, "__pycache__")
            shutil.rmtree(cache_path)
            print(f"Removed {cache_path}")
    print("Cache cleanup done.")

if __name__ == "__main__":
    cleanup()