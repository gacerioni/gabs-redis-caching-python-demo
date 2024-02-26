from locust import HttpUser, task, between
import random


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def search_clubs(self):
        fake_club_names = [
            "FC Dynamo Dreamland", "Galactic Guardians FC", "Atlantis Aquanauts", "Quantum Quokkas FC",
            "Mystic Meteors FC", "Neon Nomads SC", "Polar Pioneers FC", "Solar Sirens FC",
            "Cosmic Crusaders SC", "Aurora Avengers FC", "Eclipse Elites SC", "Phantom Phoenix FC",
            "Thunder Titans FC", "Vortex Voyagers SC", "Zenith Zeppelins FC", "Nebula Nomads SC",
            "Orbit Olympians FC", "Lunar Legends FC", "Stellar Spartans SC", "Nova Nightingales FC",
            "FC Fantasy 1", "FC Fantasy 2", "FC Fantasy 3", "FC Fantasy 4", "FC Fantasy 5",
            "FC Fantasy 6", "FC Fantasy 7"
        ]

        real_club_names = [
            "AC Milan", "Ajax", "Palmeiras", "Al Ahly", "Arsenal", "Barcelona",
            "Bayern Munich", "Borussia Dortmund", "Chelsea", "Corinthians",
            "Flamengo", "Juventus", "Liverpool", "Manchester United",
            "Real Madrid", "Santos", "Tottenham Hotspur", "Fake Club 1", "Fake Club 2"
            # Include some fake names to simulate bad searches
        ]

        final_club_list = real_club_names + fake_club_names

        club = random.choice(final_club_list)

        self.client.post("/search", data={"query": club})
