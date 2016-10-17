import os
from app import app

app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), processes=1)
