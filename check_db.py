import environ
import pymysql

# Initialize environment variables reading from .env file
env = environ.Env()
environ.Env.read_env()

def test_connection():
    try:
        # Connect to the database using parameters from .env
        connection = pymysql.connect(
            host=env('DB_HOST'),
            user=env('DB_USER'),
            password=env('DB_PASSWORD'),
            database=env('DB_NAME'),
            port=int(env('DB_PORT', default=3306))
        )
        print(f" Successfully connected to database '{env('DB_NAME')}' at host '{env('DB_HOST')}'!")
        connection.close()
    except Exception as e:
        # Output the specific error message if connection fails
        print(f" Connection error: {e}")

if __name__ == "__main__":
    test_connection()