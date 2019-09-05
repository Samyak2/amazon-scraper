### config.py ###

# Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URI = 'postgres+psycopg2://{}'.format(os.environ["DATABASE_URL"][11:])