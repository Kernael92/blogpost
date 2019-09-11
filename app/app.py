from quart import Quart 
from app import models


app = Quart(__name__)

@app.route('/')
async def hello():
    return '<a href="/admin/">Click me to get to Admin!</a>'


if __name__ =='__main__':
    # Create admin
    app.run(debug = True)