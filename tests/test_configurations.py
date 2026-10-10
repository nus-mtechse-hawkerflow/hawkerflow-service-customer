import os
from unittest.mock import patch

from configurations.app_config import (
    AppConfig,
    Database,
    DatabaseOptions,
    Datasource,
    Driver,
    Service,
)


class TestAppConfig:
    def test_service_model(self):
        service = Service(
            title="Test Service",
            root_path="/test",
            port=9000,
            host="127.0.0.1",
            allow_origins=["*"],
            methods=["GET"],
            headers=["*"],
            docs_url="/docs",
            redoc_url="/redoc",
            reload=False,
            scheme="https",
            credentials=True,
        )
        assert service.title == "Test Service"
        assert service.port == 9000
        assert service.host == "127.0.0.1"
        assert service.allow_origins == ["*"]
        assert service.credentials is True

    def test_database_model_defaults(self):
        with patch.dict(os.environ, {}, clear=True):
            db = Database(connection_url="sqlite:///test.db", driver_name="sqlite")
            assert db.name == "hawkerflow"
            assert db.host == "localhost"
            assert db.port == 5432

    def test_database_model_custom_values(self):
        db = Database(
            connection_url="postgresql://...",
            driver_name="postgresql",
            name="custom_db",
            host="db.internal",
            port=5433,
        )
        assert db.name == "custom_db"
        assert db.host == "db.internal"
        assert db.port == 5433

    def test_driver_model(self):
        driver = Driver(package="drivers.sqlite_driver", driver_class="SQLiteDriver")
        assert driver.package == "drivers.sqlite_driver"
        assert driver.driver_class == "SQLiteDriver"

    def test_database_options_defaults(self):
        with patch.dict(os.environ, {}, clear=True):
            options = DatabaseOptions(echo=True)
            assert options.user == "user"
            assert options.password == "root"
            assert options.echo is True

    def test_database_options_custom_values(self):
        options = DatabaseOptions(user="admin", password="secretpassword", echo=False)
        assert options.user == "admin"
        assert options.password == "secretpassword"
        assert options.echo is False

    def test_datasource_model(self):
        driver = Driver(package="drivers.postgres_driver", driver_class="PostgresDriver")
        db = Database(connection_url="postgres://...", driver_name="postgresql")
        opts = DatabaseOptions(echo=False)
        datasource = Datasource(driver=driver, database=db, options=opts)
        assert datasource.driver.driver_class == "PostgresDriver"
        assert datasource.options.echo is False

    def test_app_config_load_from_yaml(self):
        config = AppConfig()
        assert config.service.title == "HawkerFlow Service Customer"
        assert config.service.port == 8080
        assert config.service.host == "0.0.0.0"
        assert config.datasource.driver.driver_class == "PostgresDriver"
        assert config.datasource.database.driver_name == "postgresql+psycopg2"
