## This is basic streamlit app, we are running this using three ways


## Stremlit app
This is simple streamlit app. In which we are using stremlit with backend to perform operation


# -------------------------------------------------------------------------------------------------

## 1st way) Using `auto_activate.sh` Script

When you first create a shell script (like `auto_activate.sh`), it is just a **plain text file**.  
Your system does not yet know that it is supposed to be runnable.

To make it executable and run it, follow these steps:

1. **Make the script executable** (only the first time):

    chmod +x auto_activate.sh

it will create env using requirement.txt file if env is not present 

2. **Run the script using**: to activate env for terminal

    source auto_activate.sh

go to backend folder: cd backend 
run using 
    backend % python main.py 

got to frontend folder: cd frontend
run using
    streamlit run app.py


above is create env if not then run both backend and streamlit seperately through diffferent terminal. in Both cases need to activate env using "source auto_activate.sh" before running banckend/main.py & frontend/app.py


# -------------------------------------------------------------------------------------------------

## 2nd way) Now `auto_activate_run_all.sh` script (all in one)

This Bash script:

1) Moves to the project root to ensure paths are correct.

2) Activates a virtual environment if it exists, or creates a new one.

3) Installs required Python packages from requirements.txt if creating a new environment.

4) Starts FastAPI backend in the background.

5) Runs Streamlit frontend.

6) Stops the backend automatically when you close Streamlit.


# --------------------------------------------------------------------------------------------------
## 3rd way) using docker

To run your backend and frontend using Docker, follow these steps:

1) Open a terminal and navigate to your project directory:
    cd /Users/user/python_streamlit

2) Build and start both services using Docker Compose:
    docker-compose up --build


This will:

Build the backend and frontend Docker images.
Start both containers: FastAPI backend (port 8000) and Streamlit frontend (port 8501).
Access your apps in your browser:
Backend: http://localhost:8000
Frontend: http://localhost:8501

To stop the services, press Ctrl+C in the terminal, then run:
    docker-compose down

This will stop and remove the containers.