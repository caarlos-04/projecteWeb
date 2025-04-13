
# 🎧 SpotyStats

**SpotyStats** is a web application that lets you explore your personalized Spotify statistics: top artists, songs, genres, and more. Built using Django and integrated with the Spotify API.

---

## 🚧 Project Status

This project is still **in development** and is part of a **university coursework** assignment. New features and improvements are continuously being added.

---

## 🚀 Features (In Progress)

- View your most listened-to artists and tracks
- Discover your top genres and albums
- Receive recommendations based on your music preferences
- Clean and user-friendly interface
- Dockerized for easy setup and deployment

---

## 📦 Requirements

- [Docker](https://www.docker.com/)
- A Spotify account with API access (for live data)

---

## 🛠️ How to Use

1. **Clone the repository**
   ```bash
   git clone https://github.com/caarlos-04/spotystats.git
   cd spotystats
   ```

2. **Switch to the latest branch**
   ```bash
   git checkout master
   ```

3. **Start the app using Docker Compose**
   ```bash
   docker compose up
   ```

4. **Access the web app in your browser**
   ```
   http://localhost:8000
   ```

---

## 📁 Project Structure

```
spotystats/
├── web/          # Main app (UI and routing)
├── music/        # Handles music data from Spotify
├── info/         # Displays user-specific information
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 👨‍🎓 About

This project is developed as part of a **university web development and database** course. It's intended for educational purposes only.

---

## 📜 License

This is an open-source project under academic use.
