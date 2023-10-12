
import requests

def get_random_users(n):
    random_users = []

    for _ in range(n):
        response = requests.get("https://randomuser.me/api/")
        if response.status_code == 200:
            data = response.json()
            user = data["results"][0]
            random_users.append(user)
        else:
            print("Failed to fetch a random user.")

    return random_users

n = 10  # Specify the number of random users you want
random_users = get_random_users(n)
