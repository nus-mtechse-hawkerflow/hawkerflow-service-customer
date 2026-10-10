import pytest

from drivers.postgres_driver import PostgresDriver
from drivers.sqlite_driver import SQLiteDriver
from factory.database_factory import DatabaseFactory
from factory.driver_factory import DriverFactory


class TestFactory:
    def test_abstract_driver_factory_cannot_be_instantiated(self):
        with pytest.raises(TypeError):
            DriverFactory()

    def test_database_factory_creates_sqlite_driver(self):
        factory = DatabaseFactory()
        driver_cls = factory.create_driver("drivers.sqlite_driver", "SQLiteDriver")
        assert driver_cls is SQLiteDriver

    def test_database_factory_creates_postgres_driver(self):
        factory = DatabaseFactory()
        driver_cls = factory.create_driver("drivers.postgres_driver", "PostgresDriver")
        assert driver_cls is PostgresDriver

    def test_database_factory_invalid_package_raises_error(self):
        factory = DatabaseFactory()
        with pytest.raises(ModuleNotFoundError):
            factory.create_driver("drivers.non_existent", "NonExistent")

    def test_database_factory_invalid_class_raises_error(self):
        factory = DatabaseFactory()
        with pytest.raises(AttributeError):
            factory.create_driver("drivers.sqlite_driver", "NonExistentDriver")
