import pytest
from sqlalchemy import URL

from configurations.app_config import Database, DatabaseOptions, Datasource
from configurations.app_config import Driver as DriverConfig
from drivers.driver import Driver
from drivers.postgres_driver import PostgresDriver
from drivers.sqlite_driver import SQLiteDriver


class ConcreteDriver(Driver):
    def get_connection(self) -> str:
        return "mock://connection"


class TestDrivers:
    def test_abstract_driver_cannot_be_instantiated(self):
        with pytest.raises(TypeError):
            Driver()

    def test_concrete_driver_instantiation(self):
        driver = ConcreteDriver()
        assert driver.get_connection() == "mock://connection"

    def test_sqlite_driver(self):
        config = Datasource(
            driver=DriverConfig(package="drivers.sqlite_driver", driver_class="SQLiteDriver"),
            database=Database(connection_url="sqlite:///test.db", driver_name="sqlite"),
            options=DatabaseOptions(echo=False),
        )
        sqlite_driver = SQLiteDriver(config)
        conn1 = sqlite_driver.get_connection()
        assert conn1 == "sqlite:///test.db"

        # Verify caching
        conn2 = sqlite_driver.get_connection()
        assert conn2 is conn1

    def test_postgres_driver(self, monkeypatch):
        monkeypatch.setenv("PROJECT_PATH", "/tmp/project")
        config = Datasource(
            driver=DriverConfig(package="drivers.postgres_driver", driver_class="PostgresDriver"),
            database=Database(
                connection_url="",
                driver_name="postgresql+psycopg2",
                name="testdb",
                host="pg.internal",
                port=5432,
            ),
            options=DatabaseOptions(user="pguser", password="pgpassword", echo=False),
        )
        pg_driver = PostgresDriver(config)
        assert pg_driver._root == "/tmp/project"

        conn_url = pg_driver.get_connection()
        assert isinstance(conn_url, URL)
        assert conn_url.drivername == "postgresql+psycopg2"
        assert conn_url.username == "pguser"
        assert conn_url.password == "pgpassword"
        assert conn_url.host == "pg.internal"
        assert conn_url.port == 5432
        assert conn_url.database == "testdb"

        # Verify caching
        conn_url2 = pg_driver.get_connection()
        assert conn_url2 is conn_url
