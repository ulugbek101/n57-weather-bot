from pymysql import connect
from pymysql.cursors import DictCursor


class Database:
    def __init__(self,
                 DB_NAME: str,
                 DB_USER: str,
                 DB_PASSWORD: str,
                 DB_HOST: str,
                 DB_PORT: int) -> None:
        self.DB_NAME = DB_NAME
        self.DB_USER = DB_USER
        self.DB_PASSWORD = DB_PASSWORD
        self.DB_HOST = DB_HOST
        self.DB_PORT = DB_PORT

    @property
    def connection(self):
        return connect(
            database=self.DB_NAME,
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            cursorclass=DictCursor
        )

    def execute(self,
                sql: str,
                args: tuple = (),
                commit: bool = False,
                fetchone: bool = False,
                fetchall: bool = False) -> None | dict | tuple:
        database = self.connection
        cursor = database.cursor()

        cursor.execute(sql, args)

        if fetchone:
            data = cursor.fetchone()
        elif fetchall:
            data = cursor.fetchall()
        else:
            data = None

        if commit:
            database.commit()

        return data

    def create_users_table(self) -> None:
        sql = """
            CREATE TABLE IF NOT EXISTS users(
                id INT PRIMARY KEY AUTO_INCREMENT,
                telegram_id VARCHAR(50) NOT NULL UNIQUE,
                username VARCHAR(100),
                fullname VARCHAR(100)
            )
        """
        self.execute(sql)

    def create_cities_table(self) -> None:
        sql = """
            CREATE TABLE IF NOT EXISTS cities(
                id INT PRIMARY KEY AUTO_INCREMENT,
                owner INT NOT NULL REFERENCES users(id),
                name VARCHAR(50) NOT NULL UNIQUE,
                CONSTRAINT city_name_and_owner_unique UNIQUE(owner, name)
            )
        """
        self.execute(sql)

    def get_user(self, telegram_id: int) -> dict:
        sql = """
            SELECT * FROM users WHERE telegram_id = %s
        """
        return self.execute(sql, (telegram_id,), fetchone=True)

    def get_cities(self, user_id: int) -> list:
        sql = """
            SELECT name FROM cities WHERE owner = %s
        """
        return self.execute(sql, (user_id,), fetchall=True)

    def register_user(self, telegram_id: int, username: str, fullname: str) -> None:
        sql = """
            INSERT INTO users (telegram_id, username, fullname)
            VALUES (%s, %s, %s)
        """
        self.execute(sql, (telegram_id, username, fullname), commit=True)

    def register_city(self, telegram_id: int, city_name: str) -> None:
        user = self.get_user(telegram_id)
        user_id = user.get("id")

        sql = """
            INSERT INTO cities (owner, name) 
            VALUES (%s, %s)
        """
        self.execute(sql, (user_id, city_name), commit=True)


db = Database(DB_NAME="n57_database",
              DB_USER="root",
              DB_PASSWORD="12345678",
              DB_HOST="localhost",
              DB_PORT=3306)


db.create_users_table()
db.create_cities_table()
