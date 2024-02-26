import csv
import faker

# Create a Faker instance
fake = faker.Faker()

# Define the number of fake records you want to generate
num_records = 50000  # Adjust this number based on your needs

# File path for the new CSV with extended data
file_path = 'soccer_teams.csv'

# Define club names to mix with fake ones for variety
fake_club_names = [
    "FC Dynamo Dreamland", "Galactic Guardians FC", "Atlantis Aquanauts", "Quantum Quokkas FC",
    "Mystic Meteors FC", "Neon Nomads SC", "Polar Pioneers FC", "Solar Sirens FC",
    "Cosmic Crusaders SC", "Aurora Avengers FC", "Eclipse Elites SC", "Phantom Phoenix FC",
    "Thunder Titans FC", "Vortex Voyagers SC", "Zenith Zeppelins FC", "Nebula Nomads SC",
    "Orbit Olympians FC", "Lunar Legends FC", "Stellar Spartans SC", "Nova Nightingales FC",
    "FC Fantasy 1", "FC Fantasy 2", "FC Fantasy 3", "FC Fantasy 4", "FC Fantasy 5",
    "FC Fantasy 6", "FC Fantasy 7"
]

with open(file_path, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(["name", "country", "city", "foundation", "stadium"])

    for _ in range(num_records):
        # Randomly choose to generate a completely fake club or use a real club name
        if fake.random_int(min=0, max=1) == 0:
            club_name = fake.word().capitalize() + " FC"
        else:
            club_name = fake.random_element(elements=fake_club_names)

        # Write a row with fake data
        writer.writerow([
            club_name,
            fake.country(),
            fake.city(),
            str(fake.year()),
            fake.word().capitalize() + " Stadium"
        ])

print(f"Generated {num_records} fake soccer club records in {file_path}.")
