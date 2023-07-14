# Crear entorno de trabajo

    python -m venv .venv
    venv\Scripts\activate         (Windows)
    . .venv/bin/activate            (Linux)
    pip install -r requirements.txt

# Ejecutar la aplicación
    
    python app.py

# Si sale un error al instalar crpytography
    
    pip install flask flask-wtf pony pyopenxl qrcode flask-simplelogin email-validator
    python app-no-https.py

Nota: El scaner de QR no funcionará
