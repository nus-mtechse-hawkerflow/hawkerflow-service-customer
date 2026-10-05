# hawkerflow-service-customer

The HawkerFlow **customer service**: registers diners, checks whether an
account exists, returns a diner's profile, and records the orders a diner has
placed.

FastAPI + SQLModel on PostgreSQL. The other HawkerFlow services (order,
hawker, analytics) and the two web apps (`hawker-ui`, `diner-ui`) live in
their own repositories.

## API

Served under `/customer` on port 8080.

| Method | Path | Purpose |
|---|---|---|
| POST | `/customer/v1/customer/register` | Register a diner |
| POST | `/customer/v1/customer/check_account_exist` | Check whether an account exists |
| GET | `/customer/v1/customer/user/{cust_sub}` | A diner's details, by Cognito user |
| POST | `/customer/v1/customer/user/update_order` | Record an order against a diner |
| GET | `/customer/health` | Health check used by the load balancer |

## Data model

Tables `customer`, `customer_loyalty` and `customer_orders`, created at
startup in the shared `hawkerflow` database.

## Configuration

`resources/config.yml` holds the service settings. The database host, port,
name, user and password come from the `DB_HOST`, `DB_PORT`, `DB_NAME`,
`DB_USERNAME` and `DB_PASSWORD` environment variables.

## Deployment

The service runs on ECS Fargate behind API Gateway and an internal load
balancer, defined in the `hawkerflow-terraform` repository. To release a
change, run from that repository:

```bash
./scripts/release-service.sh customer ../hawkerflow-service-customer
```
