import hvac
import json

client = hvac.Client(
    url='https://18.135.61.61:8200',
    token='h**.************************',
    verify='/home/****/cloud/vault.crt',
)

print(client.is_authenticated())
if not client.is_authenticated():
    print("Error: No se pudo autenticar en Vault.")
else:
    # Lee un secret desde Vault (reemplaza 'secret/path' con la ruta real de tu secret)
    secret_path = 'kv/data/****'
    response = client.read(secret_path)

    if response is not None and 'data' in response:
        data = response['data']
        for key, value in data.items():
            print(value.get("user"))
    else:
        print(f"No se pudo encontrar el secret en {secret_path}")