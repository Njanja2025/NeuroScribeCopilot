#!/usr/bin/env python3
import os
import zipfile
from datetime import datetime

def create_zip_package():
    version = "v1.0.0"
    timestamp = datetime.now().strftime("%Y%m%d")
    zip_name = f"NeuroScribeCopilot-{version}-{timestamp}.zip"
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('.'):
            for file in files:
                if not file.endswith('.zip'):
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, '.')
                    zipf.write(file_path, arc_name)
    
    print(f"✅ Created: {zip_name}")

if __name__ == "__main__":
    create_zip_package()
