from comics import app
import os

# running w/o gunicorn
if __name__ == "__main__":
    app.run(debug=True)
