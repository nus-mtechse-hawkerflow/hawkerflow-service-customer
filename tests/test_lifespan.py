from unittest.mock import MagicMock, patch

import pytest
from fastapi import FastAPI

from lifecycle.lifespan import startup


class TestLifespan:
    @pytest.mark.anyio
    @patch("lifecycle.lifespan.DBSession")
    @patch("lifecycle.lifespan.SQLModel")
    @patch("lifecycle.lifespan.CustomerRepo")
    @patch("lifecycle.lifespan.CustomerOrdersRepo")
    @patch("lifecycle.lifespan.UserService")
    async def test_startup_lifespan(
        self,
        mock_user_service_cls,
        mock_orders_repo_cls,
        mock_customer_repo_cls,
        mock_sqlmodel,
        mock_db_session_cls,
    ):
        mock_session_instance = MagicMock()
        mock_db_session_cls.return_value = mock_session_instance
        mock_user_service_instance = MagicMock()
        mock_user_service_cls.return_value = mock_user_service_instance

        app = FastAPI()
        async with startup(app):
            assert hasattr(app.state, "config")
            assert app.state.session is mock_session_instance
            assert app.state.user_service is mock_user_service_instance

            mock_db_session_cls.assert_called_once()
            mock_sqlmodel.metadata.create_all.assert_called_once_with(
                mock_session_instance.engine
            )
            mock_customer_repo_cls.assert_called_once_with(mock_session_instance.engine)
            mock_orders_repo_cls.assert_called_once_with(mock_session_instance.engine)
            mock_user_service_cls.assert_called_once()
