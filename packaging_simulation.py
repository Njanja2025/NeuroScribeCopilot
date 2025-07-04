import zipfile
import os
import shutil
from datetime import datetime

def simulate_packaging(project_directory, output_name="NjaxCopilot_Package"):
    """
    Simulate packaging a project directory into a ZIP file
    
    Args:
        project_directory (str): Path to the project directory
        output_name (str): Name for the output ZIP file
    """
    
    # Get current directory
    current_dir = os.getcwd()
    
    # Create output path
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_zip_path = f"{output_name}_{timestamp}.zip"
    
    print(f"🚀 Starting packaging simulation...")
    print(f"📁 Project Directory: {project_directory}")
    print(f"📦 Output ZIP: {output_zip_path}")
    print("=" * 60)
    
    # Check if project directory exists
    if not os.path.exists(project_directory):
        print(f"❌ Error: Project directory '{project_directory}' not found!")
        print(f"💡 Using current directory instead: {current_dir}")
        project_directory = current_dir
    
    # Create a zip file from the specified project directory
    try:
        with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            file_count = 0
            total_size = 0
            
            for root, dirs, files in os.walk(project_directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    
                    # Skip certain files/directories
                    if any(skip in file_path for skip in ['.git', '__pycache__', '.pyc', '.DS_Store']):
                        continue
                    
                    # Get relative path for the ZIP
                    arcname = os.path.relpath(file_path, project_directory)
                    
                    # Add file to ZIP
                    zipf.write(file_path, arcname)
                    
                    # Update counters
                    file_count += 1
                    file_size = os.path.getsize(file_path)
                    total_size += file_size
                    
                    print(f"📦 Added: {arcname} ({file_size} bytes)")
            
            print("=" * 60)
            print(f"✅ Packaging completed successfully!")
            print(f"📊 Files packaged: {file_count}")
            print(f"📊 Total size: {total_size / 1024:.1f} KB")
            print(f"📦 ZIP file: {output_zip_path}")
            print(f"📁 ZIP size: {os.path.getsize(output_zip_path) / 1024:.1f} KB")
            
            return output_zip_path
            
    except Exception as e:
        print(f"❌ Error during packaging: {e}")
        return None

def create_simple_package():
    """Create a simple demonstration package"""
    
    # Create a temporary project structure
    temp_project = "temp_project_demo"
    os.makedirs(temp_project, exist_ok=True)
    
    # Create some demo files
    demo_files = {
        "main.py": "print('Hello from NjaxCopilot!')\n",
        "README.md": "# NjaxCopilot Demo\nThis is a demonstration package.\n",
        "requirements.txt": "streamlit\nopenai\npandas\n",
        "config.json": '{"name": "NjaxCopilot", "version": "1.0.0"}\n',
        "src/__init__.py": "# Source package\n",
        "src/utils.py": "def helper_function():\n    return 'Helper function'\n",
        "docs/guide.md": "# User Guide\nFollow these instructions.\n"
    }
    
    for file_path, content in demo_files.items():
        full_path = os.path.join(temp_project, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'w') as f:
            f.write(content)
    
    print(f"📁 Created demo project structure in: {temp_project}")
    
    # Package the demo project
    result = simulate_packaging(temp_project, "NjaxCopilot_Demo")
    
    # Clean up
    shutil.rmtree(temp_project)
    
    return result

if __name__ == "__main__":
    print("🎯 NjaxCopilot Packaging Simulation")
    print("=" * 60)
    
    # Option 1: Package current directory
    print("\n1️⃣ Packaging current directory...")
    current_package = simulate_packaging(".", "NjaxCopilot_Current")
    
    # Option 2: Create demo package
    print("\n2️⃣ Creating demo package...")
    demo_package = create_simple_package()
    
    print("\n" + "=" * 60)
    print("🎉 Packaging simulation complete!")
    print("=" * 60)
    
    if current_package:
        print(f"✅ Current directory package: {current_package}")
    
    if demo_package:
        print(f"✅ Demo package: {demo_package}")
    
    print("\n💡 Usage examples:")
    print("   # Package current directory")
    print("   python packaging_simulation.py")
    print("   ")
    print("   # Package specific directory")
    print("   simulate_packaging('/path/to/project', 'MyProject')")
    print("   ")
    print("   # Create demo package")
    print("   create_simple_package()") 