import subprocess
import sys
import os

def install_libraries():
    # Path to your virtual environment's Python executable
    venv_python = os.path.expanduser("~/python_envs/shared_env/bin/python")

    # List of libraries to install
    libraries = [
        "matplotlib", "numpy", "pandas", "polars", "seaborn",
        "tensorflow", "keras", "torch", "scikit-learn", "xgboost",
        "lightgbm", "catboost", "statsmodels", "plotly", "dash",
        "opencv-python", "sympy", "networkx", "nltk", "spacy",
        "pillow", "requests", "beautifulsoup4", "flask", "django",
        ]

    for lib in libraries:
        try:
            # Use the virtual environment's Python executable to install libraries
            subprocess.check_call([venv_python, "-m", "pip", "install", lib])
            print(f"Successfully installed {lib}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {lib}: {e}")

if __name__ == "__main__":
    install_libraries()

    print("Libraries installed in the virtual environment.")

    # Instructions for activating the shared virtual environment
    print("\nTo activate the shared virtual environment:")
    print("source ~/python_envs/shared_env/bin/activate")
    print("\nTo run your clustering script:")
    print("python3 /home/kondr/football_manager_proj/fman_initial_Dat_Analysis_test/clustering.py")