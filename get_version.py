def get_version():
    with open('VERSION', 'r') as version_file:
        return version_file.read().strip()


if __name__ == "__main__":
    print(get_version())
