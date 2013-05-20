from comics import app
import os

if __name__ == "__main__":
    DEBUG = os.getenv('COMICS_DEBUG', False)
    # if COMICS_DEBUG is set to anything, == True
    app.run(debug=bool(DEBUG))
