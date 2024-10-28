import pymysql.cursors


def get_db_connection():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='sijo',  # Replace with your MySQL username
            password='password',  # Replace with your MySQL password
            db='gdeproj1',  # Replace with your MySQL database name
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None

def create_table():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Define your table creation SQL query
            create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                user_name VARCHAR(50) NOT NULL,
                creation_date VARCHAR(50) NOT NULL
            )
            """
            cursor.execute(create_table_query)
        connection.commit()
    except pymysql.Error as e:
        print(f"Error creating table: {e}")
    finally:
        connection.close()
