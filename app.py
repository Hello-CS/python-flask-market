"""
Importing sqlalchemy will result in circular imports
2 files trying to import from each other resulting in missing info, forbidden in python
Python introduces packages for this
"""

#pulls market package and run it
from market import app

#checks if our run.py file has executed directly and not imported    
if __name__ == '__main__': 
    app.run(debug=True)