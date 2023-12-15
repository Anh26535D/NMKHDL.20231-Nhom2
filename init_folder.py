import os

if os.path.exists('dataset/prices'):
    print('Folder dataset already exists!')
else:
    os.mkdir('dataset/prices')
    print('Folder dataset created!')