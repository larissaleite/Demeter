import os
from app import app

#DO NOT PUT AS DEBUG, BECAUSE IT INITIALIZES TWICE!!!
app.run(debug=False, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), processes=1)
