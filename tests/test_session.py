from unittest.mock import MagicMock, patch

from sqlalchemy.engine import Engine

from configurations.app_config import Database, DatabaseOptions, Datasource, Driver
from session.db_session import DBSession


class TestDBSession:
    def test_db_session_lazy_engine_creation(self):
        config = Datasource(
            driver=Driver(package="drivers.sqlite_driver", driver_class="SQLiteDriver"),
            database=Database(connection_url="sqlite:///:memory:", driver_name="sqlite"),
            options=DatabaseOptions(echo=False),
        )
        db_session = DBSession(config)
        assert db_session._engine is None

        engine = db_session.engine
        assert isinstance(engine, Engine)
        # Calling again returns cached engine
        assert db_session.engine is engine

    def test_db_session_engine_setter(self):
        config = Datasource(
            driver=Driver(package="drivers.sqlite_driver", driver_class="SQLiteDriver"),
            database=Database(connection_url="sqlite:///:memory:", driver_name="sqlite"),
            options=DatabaseOptions(echo=False),
        )
        db_session = DBSession(config)
        custom_engine = MagicMock(spec=Engine)
        db_session.engine = custom_engine

        assert db_session.engine is custom_engine

    @patch("session.db_session.DatabaseFactory")
    def test_get_connection_invokes_factory(self, mock_factory_cls):
        mock_factory = MagicMock()
        mock_driver_cls = MagicMock()
        mock_driver_instance = MagicMock()
        mock_driver_instance.get_connection.return_value = "sqlite:///:memory:"

        mock_driver_cls.return_value = mock_driver_instance
        mock_factory.create_driver.return_value = mock_driver_cls
        mock_factory_cls.return_value = mock_factory

        config = Datasource(
            driver=Driver(package="drivers.sqlite_driver", driver_class="SQLiteDriver"),
            database=Database(connection_url="sqlite:///:memory:", driver_name="sqlite"),
            options=DatabaseOptions(echo=False),
        )
        db_session = DBSession(config)
        connection = db_session._get_connection()

        mock_factory.create_driver.assert_called_once_with(
            "drivers.sqlite_driver", "SQLiteDriver"
        )
        mock_driver_cls.assert_called_once_with(config)
        assert connection == "sqlite:///:memory:"
