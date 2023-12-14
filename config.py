from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class SelenoidSettings(BaseSettings):
    """Settings Selenoid."""

    class Config:
        env_file = ".env"
        env_prefix = "SELENOID_"
        env_file_encoding = "utf-8"

    # Enabling browser management capabilities
    enable_vnc: bool = True
    # Enabling video recording
    enable_video: bool = False
    # Browser Version
    browser_version: str = "114.0"
    # Path to Selenoid
    hub: str = "http://192.168.0.10:8080/wd/hub"


class PostgresDB(BaseSettings):
    """Config postgresql."""

    class Config:
        env_file = ".env"
        env_prefix = "DB_POSTGRES_"
        env_file_encoding = "utf-8"

    db_type: str = "postgresql"
    host: str = ""
    port: str = ""
    db_name: str = ""
    user: str = ""
    password: str = ""


class MysqlDB(BaseSettings):
    """Config mysql."""

    class Config:
        env_file = ".env"
        env_prefix = "DB_MYSQL_"
        env_file_encoding = "utf-8"

    db_type: str = "mysql"
    host: str = ""
    db_name: str = ""
    user: str = ""
    password: str = ""


class OracleDB(BaseSettings):
    """Config oracle."""

    class Config:
        env_file = ".env"
        env_prefix = "DB_ORACLE_"
        env_file_encoding = "utf-8"

    db_type: str = "oracle"
    host: str = ""
    port: str = ""
    db_name: str = ""
    user: str = ""
    password: str = ""


class MssqlDB(BaseSettings):
    """Config mssql."""

    class Config:
        env_file = ".env"
        env_prefix = "DB_MSSQL_"
        env_file_encoding = "utf-8"

    db_type: str = "mssql"
    host: str = ""
    db_name: str = ""
    user: str = ""
    password: str = ""


class SqliteDB(BaseSettings):
    """Config sqlite."""

    class Config:
        env_file = ".env"
        env_prefix = "DB_SQLITE_"
        env_file_encoding = "utf-8"

    db_type: str = "sqlite"
    path: str = ""


class DB(BaseSettings):
    """Settings database."""

    class Config:
        env_file = ".env"
        env_prefix = "DB_"
        env_file_encoding = "utf-8"

    postgres: PostgresDB = PostgresDB()
    mysql: MysqlDB = MysqlDB()
    oracle: OracleDB = OracleDB()
    mssql: MssqlDB = MssqlDB()
    sqlite: SqliteDB = SqliteDB()


class Settings(BaseSettings):
    """Настройки для тестов."""

    # Configuration of settings
    class Config:
        env_file = ".env"
        env_prefix = "AUTOTEST_"
        env_file_encoding = "utf-8"

    # URL of the application frontend
    application_url: str = "https://google.com/"

    # Browser Name
    browser_name: str = "chrome"
    # Browser width
    browser_window_width: str = "1920"
    # Browser Height
    browser_window_height: str = "1080"
    # Element timeout
    timeout: int = 30
    # Selenoid Configuration
    selenoid: SelenoidSettings = SelenoidSettings()
    db: DB = DB()


settings_config = Settings()
