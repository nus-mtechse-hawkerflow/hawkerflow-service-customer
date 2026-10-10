import pytest

from endpoints.health_routes import health, health_router


class TestHealthRoutes:
    @pytest.mark.anyio
    async def test_health_endpoint(self):
        response = await health()
        assert response == {"status": "ok"}

    def test_health_router_configuration(self):
        routes = {route.path: route.methods for route in health_router.routes}
        assert "/health" in routes
        assert "GET" in routes["/health"]
