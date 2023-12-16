import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def make_path(path):
    if os.path.exists(path):
        print(f'Folder {path} already exists!')
    else:
        os.makedirs(path)
        print(f'Folder {path} created!')

print('[START >>] Creating folders...')
print('#'*50)
make_path('data/raw/prices')
make_path('data/processed/prices')
make_path('datalogs')

print('#'*50)
print('[END <<] Creating folders...')