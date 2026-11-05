import os
import firebase_admin
from firebase_admin import credentials, firestore

# 1. Eliminamos la variable del emulador de la memoria de Python
os.environ.pop("FIRESTORE_EMULATOR_HOST", None)

# 2. Cargamos las credenciales del archivo local
cred = credentials.Certificate("serviceAccountKey.json")

# 3. Inicializamos Firebase Admin apuntando a la nube
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()