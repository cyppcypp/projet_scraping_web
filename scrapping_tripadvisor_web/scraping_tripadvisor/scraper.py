import requests
import time
import pandas as pd
import re
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

api_url_restaurant = (
    "https://tripadvisor16.p.rapidapi.com/api/v1/restaurant/searchRestaurants"
)
headers = {
    "X-RapidAPI-Key": os.getenv("TRIPADVISOR_API_KEY", "8dfbeaf8bfmsh1eed75490e0bedep151605jsnc9afdbbffbda"),
    "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com",
}

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_ANON_KEY")
supabase: Client = create_client(supabase_url, supabase_key)


def generate_unique_id(nom, ville):
    formatted_name = re.sub(r"[^a-zA-Z0-9]", "_", nom).lower()
    formatted_city = re.sub(r"[^a-zA-Z0-9]", "_", ville).lower()
    id_unique = f"{formatted_name}_{formatted_city}"
    return id_unique


def insert_restaurant(nom, note, nb_avis, ville, pays, pop_city, all_pop_city):
    try:
        if pays is None:
            pays = "Inconnu"
        if pop_city is None:
            pop_city = "0"
        if all_pop_city is None:
            all_pop_city = "0"

        id_unique = generate_unique_id(nom, ville)

        data = {
            "id_unique": id_unique,
            "nom": nom,
            "note": note,
            "nb_avis": nb_avis,
            "ville": ville,
            "pays": pays,
            "pop_city": str(pop_city),
            "all_pop_city": str(all_pop_city),
        }

        result = supabase.table("restaurant").upsert(
            data,
            on_conflict="id_unique"
        ).execute()

        print(f"Inséré : {nom}, ville : {ville}, pays : {pays}")
    except Exception as err:
        print(f"Erreur Supabase : {err}")


def fetch_restaurants(location_id):
    querystring = {
        "locationId": location_id,
        "limit": "50",
    }

    response = requests.get(api_url_restaurant, headers=headers, params=querystring)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 429:
        print("Trop de requêtes, attente de 20 secondes...")
        time.sleep(20)
        return fetch_restaurants(location_id)
    else:
        print(
            f"Erreur lors de l'appel à l'API des restaurants : {response.status_code} - {response.text}"
        )
        return None


city_data = pd.read_csv("data/Population_by_city.csv", encoding="utf-8")

city_pop_info = {
    row["Capitale"]: {
        "pays": row["Pays"],
        "pop_city": row["Population ville"],
        "all_pop_city": row["Population et périphérie"],
    }
    for _, row in city_data.iterrows()
}

city_ids = {
    "Paris": 187147,
    "Rome": 187791,
    "Ottawa": 155004,
    "Helsinki": 189934,
    "Berlin": 187323,
    "Tokyo": 298184,
    "Londres": 186338,
    "Pekin": 294212,
    "Canberra": 255057,
    "Tirana": 294446,
}

for city, location_id in city_ids.items():
    data = fetch_restaurants(location_id)

    if data:
        if isinstance(data, dict) and "data" in data and "data" in data["data"]:
            for restaurant in data["data"]["data"]:
                try:
                    name = restaurant.get("name")
                    rating = restaurant.get("averageRating")
                    reviews = restaurant.get("userReviewCount")

                    if city in city_pop_info:
                        pop_info = city_pop_info[city]
                        pays = pop_info["pays"]
                        pop_city = pop_info["pop_city"]
                        all_pop_city = pop_info["all_pop_city"]
                    else:
                        pays = pop_city = all_pop_city = None

                    if name and rating is not None and reviews is not None:
                        if isinstance(rating, (int, float)) and 1 <= rating <= 5:
                            insert_restaurant(
                                name,
                                rating,
                                reviews,
                                city,
                                pays,
                                pop_city,
                                all_pop_city,
                            )
                except Exception as e:
                    print(f"Erreur lors de l'extraction des données pour {city}: {e}")

try:
    result = supabase.table("restaurant").select("*").execute()
    restaurants = result.data

    columns = [
        "Nom",
        "Note",
        "Avis",
        "Ville",
        "Pays",
        "Population ville",
        "Population et périphérie",
    ]
    df = pd.DataFrame([
        {
            "Nom": r["nom"],
            "Note": r["note"],
            "Avis": r["nb_avis"],
            "Ville": r["ville"],
            "Pays": r["pays"],
            "Population ville": r["pop_city"],
            "Population et périphérie": r["all_pop_city"],
        }
        for r in restaurants
    ])

    df.to_csv("data/restaurants_export.csv", index=False, encoding="utf-8")
    print("Export des données vers restaurants_export.csv terminé !")
except Exception as err:
    print(f"Erreur Supabase lors de l'exportation des données : {err}")

print("Extraction et insertion dans la base de données terminées !")
