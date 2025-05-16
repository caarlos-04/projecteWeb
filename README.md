# Projecte Web - SpotyStats
**Group members**:  
- GENÉ MORA, BLAI  
- MASIP DOMINGO, POL 
- MAZARICO BALLARIN, CARLOS 
- MOLA FERRER, DAVID 
- VIÑES BOTARGUES, ORIOL 

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

## 3. Model Comparison: Final vs Previous Version

In this section, we compare the data models implemented in the final version of the project with 
those used in the previous milestone. The changes reflect both structural improvements and feature 
enhancements to better support user functionality, especially around playlist management and media 
presentation.

### 3.1. Summary of Previous Models

The earlier version of the project included four main models to represent musical content and 
listening history:

- **Artist**: Stored artist names.  
- **Album**: Linked to an artist and included a title and release date.  
- **Track**: Linked to both an artist and (optionally) an album. Included duration and popularity 
metrics.  
- **ListeningHistory**: Recorded when a track was played, storing artist, track, and timestamp.

These models provided a solid foundation for representing Spotify-like data structures and enabled 
tracking and analysis of user listening patterns.

### 3.2. Final Models Overview

In the current version, we have made several key changes and improvements:

#### 3.2.1. Artist
- **Same as before**: Stores the name of the artist and implements `__str__()` for readability.

#### 3.2.2. Album
- **Similar to before**: Linked to an `Artist` and includes a title.
- **Differences**: `release_date` field has been removed for simplicity.

#### 3.2.3. Track
- **Refined fields**:
  - Retains `title`, `artist`, and optional `album`.
  - Introduces a new `image` field (an `ImageField`) to store artwork or visual representation 
  for each track.
- **Removed fields**:
  - `duration_ms` and `popularity` fields are no longer present in the final model.

#### 3.2.4. Playlist
- **New functionality** added to support user interaction:
  - `title`: Name of the playlist.
  - `tracks`: A many-to-many relationship with `Track`.
  - `user`: Foreign key linking to Django's built-in `User` model, allowing user-specific playlists.
- **Meta constraint**:
  - `unique_together = ('title', 'user')` ensures that each user cannot create multiple playlists 
  with the same title.

#### 3.2.5. Removed Model: ListeningHistory
- The `ListeningHistory` model from the previous version has been removed.
- As a result, the app no longer tracks when songs are played or how often, reducing complexity 
and focusing more on user-created content (playlists).

#### 3.2.6. Why changing?

- **User Experience**: Adding playlists and image fields improves the app’s usefulness and visual 
appeal.
- **Simplification**: Removing `ListeningHistory`, `popularity`, and `duration_ms` reduces 
unnecessary complexity.
- **Focus Shift**: The app has evolved from being analytics-focused to being user-interaction 
focused.
