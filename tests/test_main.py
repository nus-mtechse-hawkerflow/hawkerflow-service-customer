from unittest.mock import patch

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from main import HawkerFlowCustomer


class TestMain:
    def test_hawkerflow_customer_init(self):
        app_wrapper = HawkerFlowCustomer()

        assert isinstance(app_wrapper._app, FastAPI)
        assert app_wrapper._app.title == "Hawkerflow Service Customer"
        assert app_wrapper._app.docs_url == app_wrapper._config.service.docs_url
        assert app_wrapper._app.redoc_url == app_wrapper._config.service.redoc_url
        assert app_wrapper._app.root_path == app_wrapper._config.service.root_path

        # Verify middlewares exist on user middleware stack
        middleware_classes = [m.cls for m in app_wrapper._app.user_middleware]
        assert TrustedHostMiddleware in middleware_classes
        assert CORSMiddleware in middleware_classes

        # Verify router paths are mounted
        route_paths = []
        for r in app_wrapper._app.routes:
            if hasattr(r, "path"):
                route_paths.append(r.path)
            elif hasattr(r, "original_router"):
                for sub in r.original_router.routes:
                    route_paths.append(sub.path)

        assert "/v1/customer/register" in route_paths
        assert "/v1/customer/check_account_exist" in route_paths
        assert "/v1/customer/user/{cust_sub}" in route_paths
        assert "/v1/customer/user/update_order" in route_paths
        assert "/health" in route_paths

    @patch("main.uvicorn.run")
    def test_hawkerflow_customer_start(self, mock_uvicorn_run):
        app_wrapper = HawkerFlowCustomer()
        app_wrapper.start()

        mock_uvicorn_run.assert_called_once_with(
            app_wrapper._app,
            host=app_wrapper._config.service.host,
            port=app_wrapper._config.service.port,
        )
