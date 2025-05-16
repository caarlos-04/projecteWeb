# Projecte Web - SpotyStats
**Group members**:  
- Blai Gené  
- Pol Masip  
- Carlos Mazarico  
- David Mola  
- Oriol Viñes  

**University**: Universitat de Lleida (UdL)  
**Course**: 3rd of Computer Engineering 
**Academic Year**: 2024–2025  

---

## 1. GitHub Public Address

The project is available at the following public GitHub repository:  

[https://github.com/caarlos-04/projecteWeb.git](https://github.com/caarlos-04/projecteWeb.git)

---

## 2. Steps to Run the Application

### 2.1. Clone the repository

To get a local copy of the project, use the following command in your terminal:

git clone https://github.com/caarlos-04/projecteWeb.git

### 2.2. Run the Docker App

Search the Docker app in you computer and just open it. Do not introduce any command yet.

### 2.3. Create a .env file with the follwing content

In order to connect to the Spotify API, you need to provide your API credentials. 
These credentials are not stored in the GitHub repository (they are excluded via .gitignore), 
so you'll need to manually create a .env file at the root of the project directory.

Create a file in the root of the project called just ".env" and paste the following content inside:

SPOTIPY_CLIENT_ID=017ef90642c14d9ab50c22f1d73f507b
SPOTIPY_CLIENT_SECRET=0e87e669caad4ee8bae84864f190162a
SPOTIPY_REDIRECT_URI=http://localhost:8000/music/spotify-callback/

### 2.4. Introduce the following Docker commands
In order to prevent errors and start from a clean state,  rebuild the images without using 
any cache, and restart everything, execute the following sequence of commands:

docker compose down
docker compose build --no-cache
docker compose up

This commands will:

- Build the necessary Docker image using the provided Dockerfile.

- Install all required dependencies.

- Start the Django web application along with any other defined services (e.g., database).

- Expose the application on your local machine via port 8000.

Make sure you have done step 2.2. so Docker is installed and running on your machine before 
executing this command.

### 2.5. Check the localhost 8000 in the URL

After running the app, open a web browser and go to:

http://localhost:8000

This should load the main page of the Django web application. You should see the Home page
of our application, SpotyStats, asking for some credentials to log in.

### 2.6. Introduce the credentials

Use the following credentials to log in:

- Username: edf

- Password: 12345678

Once logged in, you'll be able to manage models, users, and data through a graphical web 
interface.

---

## 3. 
