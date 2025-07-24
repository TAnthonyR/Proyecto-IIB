import requests

def buscar_por_nombre(nombre):
    url = f"https://db.ygoprodeck.com/api/v7/cardinfo.php?name={nombre}"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()["data"][0]
    return None

def buscar_similares_por_nombre(nombre):
    url = f"https://db.ygoprodeck.com/api/v7/cardinfo.php?fname={nombre.split()[0]}"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()["data"][:5]
    return []

def buscar_por_tipo(tipo):
    url = f"https://db.ygoprodeck.com/api/v7/cardinfo.php?type={tipo}"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()["data"][:10]  # Limitamos a 10 resultados
    return []
