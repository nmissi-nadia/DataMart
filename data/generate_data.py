import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_ecommerce_data(n_orders=5000, seed=42):
    np.random.seed(seed)
    random.seed(seed)

    categories = {
        "Électronique": {"price_range": (50, 1500), "margin": 0.20},
        "Mode": {"price_range": (15, 300), "margin": 0.55},
        "Maison & Jardin": {"price_range": (10, 500), "margin": 0.40},
        "Sport": {"price_range": (20, 400), "margin": 0.35},
        "Beauté": {"price_range": (5, 150), "margin": 0.60},
        "Livres": {"price_range": (5, 40), "margin": 0.30},
    }

    products = {
        "Électronique": ["Smartphone", "Laptop", "Écouteurs", "Tablette", "Montre connectée", "TV 4K"],
        "Mode": ["T-shirt", "Jean", "Robe", "Veste", "Chaussures", "Sac à main"],
        "Maison & Jardin": ["Lampe LED", "Coussin", "Plante", "Tapis", "Bougie", "Cadre photo"],
        "Sport": ["Vélo", "Tapis de yoga", "Haltères", "Chaussures running", "Sac de sport"],
        "Beauté": ["Crème visage", "Parfum", "Mascara", "Sérum", "Rouge à lèvres"],
        "Livres": ["Roman", "BD", "Manga", "Guide pratique", "Biographie"],
    }

    regions = ["Île-de-France", "Auvergne-Rhône-Alpes", "Nouvelle-Aquitaine",
               "Occitanie", "Hauts-de-France", "Provence-Alpes-Côte d'Azur",
               "Grand Est", "Normandie", "Bretagne", "Pays de la Loire"]

    channels = ["Site web", "Application mobile", "Marketplace", "Réseaux sociaux"]
    payment_methods = ["Carte bancaire", "PayPal", "Virement", "Apple Pay"]
    statuses = ["Livré", "En cours", "Annulé", "Retourné"]
    status_weights = [0.75, 0.15, 0.06, 0.04]

    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)

    data = []
    for i in range(n_orders):
        cat = random.choice(list(categories.keys()))
        product = random.choice(products[cat])
        price_min, price_max = categories[cat]["price_range"]
        margin_rate = categories[cat]["margin"]

        price = round(np.random.uniform(price_min, price_max), 2)
        quantity = np.random.choice([1, 2, 3, 4, 5], p=[0.60, 0.25, 0.10, 0.03, 0.02])
        revenue = round(price * quantity, 2)
        margin = round(revenue * margin_rate, 2)

        order_date = start_date + timedelta(
            seconds=random.randint(0, int((end_date - start_date).total_seconds()))
        )
        # Seasonal boost (Q4)
        if order_date.month in [11, 12]:
            if random.random() < 0.3:
                quantity = min(quantity + 1, 5)
                revenue = round(price * quantity, 2)
                margin = round(revenue * margin_rate, 2)

        customer_id = f"C{random.randint(1000, 3000):04d}"
        region = random.choice(regions)
        channel = random.choice(channels)
        payment = random.choice(payment_methods)
        status = np.random.choice(statuses, p=status_weights)

        data.append({
            "order_id": f"ORD-{i+1:05d}",
            "customer_id": customer_id,
            "order_date": order_date,
            "category": cat,
            "product": product,
            "unit_price": price,
            "quantity": quantity,
            "revenue": revenue,
            "margin": margin,
            "region": region,
            "channel": channel,
            "payment_method": payment,
            "status": status,
        })

    df = pd.DataFrame(data)
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    df["week"] = df["order_date"].dt.isocalendar().week
    df["year"] = df["order_date"].dt.year
    df["day_of_week"] = df["order_date"].dt.day_name()

    # Customer segments
    customer_spending = df.groupby("customer_id")["revenue"].sum()
    df["customer_segment"] = df["customer_id"].map(
        lambda x: "VIP" if customer_spending.get(x, 0) > 2000
        else "Fidèle" if customer_spending.get(x, 0) > 800
        else "Occasionnel"
    )

    return df


if __name__ == "__main__":
    df = generate_ecommerce_data()
    df.to_csv("ecommerce_data.csv", index=False)
    print(f"✅ Dataset généré : {len(df)} commandes")
    print(df.head())
