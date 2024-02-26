import csv
from dotenv import load_dotenv
from database import init_db, load_initial_data, Session

# Load environment variables
load_dotenv()


def load_csv_data(csv_file):
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
    return data


def main():
    init_db()
    session = Session()
    data = load_csv_data('data/soccer_teams.csv')
    load_initial_data(session, data)
    session.close()


if __name__ == "__main__":
    main()
