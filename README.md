# Decision-Support System for Marketplace Pricing Strategy - Backend

You can read full information about this project (here)[https://github.com/sonina-marina/Decision-Support-System-for-Marketplace-Pricing-Strategy-Backend.wiki.git]

# Backend

FastAPI application with async SQLAlchemy, PostgreSQL, and Alembic migrations. No architecture diagram yet — this page describes the layering in words until one is drawn.

## Layers

The backend follows a strict layered structure, top to bottom:

```
API routes (src/api/v1/*)
      ↓
Services (src/services/*)
      ↓
Repositories (src/db/repositories/*)
      ↓
Models (src/db/models/*)  →  PostgreSQL
```

**API routes** parse the request, call exactly one service method, and translate known domain exceptions into HTTP responses (e.g. `ProductNotFoundError` → 404, `InvalidCredentialsError` → 401).

**Services** hold business logic and orchestrate repositories. They never talk to SQLAlchemy directly — no query building, no eager-loading options. If a service needs a related entity loaded, it calls a repository method named for that purpose (see below), not a generic `get_by_id` with ORM options passed in from the service layer.

**Repositories** are the only layer that knows about SQLAlchemy. Relationships that use `lazy='raise'` (an intentional guard against accidental N+1 queries) must be loaded explicitly via `selectinload`, and only inside a repository method — never in a service. Naming convention: a method that eager-loads a relationship says so in its name, e.g. `get_by_id_with_metrics`, `get_by_id_with_products`, so a service call site tells you at a glance whether the relationship is safe to read afterwards.

**Models** are plain SQLAlchemy models. All of them use soft deletion: an `is_deleted` boolean column instead of a real `DELETE`. The base repository's `exclude_deleted` / `exclude_deleted_from_list` helpers automatically filter out soft-deleted rows in `get_by_id` / `get_all`, so callers don't need to remember to filter manually.

## Domain model

- **User** — email, hashed password, `fullname`, `role` (`ADMIN` | `SELLER`)
- **Store** — belongs to a user; holds a `name` and a `currency` (Postgres enum: `USD` | `EUR` | `RUB`). Currency lives on the store, not on individual products, since all products in one store trade in the same currency — a product's `currency` field in API responses is computed by looking up its store, never stored redundantly on the product row.
- **Product** — belongs to a store; holds pricing, cost, funnel, and logistics data (price, COGS, marketplace commission, acquiring, tax, views, target actions, buyers, ad costs, inbound/direct/reverse logistics, return rate, defect rate, average storage/packaging cost, sales)
- **Metrics** — an append-only calculation record tied to a product. Every "Calculate metrics" action inserts a new row rather than overwriting the previous one, which is what powers the per-product calculation history.

## Authentication

A dedicated `/login/` router (outside the main `/api/v1` prefix) issues a JWT on successful login. The token payload carries:
- `sub` — user id (as a string)
- `role` — `ADMIN` or `SELLER`
- `exp` — expiry

All other endpoints require `Authorization: Bearer <token>` (`HTTPBearer` security scheme) and are grouped under `/api/v1`.

## Unit economics calculation

`MetricCalculator` (in the metrics service) implements the formulas:

- `conversion = targetActions / views`
- `cac = adCosts / buyers`
- `requiredCpa = adCosts / targetActions`
- `ltc = cogs + price×commission% + price×acquiring% + price×tax% + inboundLogistic + directLogistic + returnRate×reverseLogistic + cogs×returnRate×defectRate + avgStorage + avgPackaging`
- `cm = price − ltc`
- `ltv = cm × sales / buyers`
- `productRoi = (cm / ltc) × 100`

This exact formula set is also ported 1:1 to the frontend (see [Frontend](Front)) so the standalone calculator and scenario comparison can recalculate instantly on every keystroke without a network round trip. Only calculations that must be persisted (`POST /api/v1/metrics/`, `POST /api/v1/metrics/custom`) go through the API.

## Key endpoint groups

| Group | Examples |
|---|---|
| Auth | `POST /login/` |
| Users | `POST /api/v1/users/`, `GET /api/v1/users/`, password/fullname updates |
| Stores | `POST /api/v1/stores/`, `GET /api/v1/stores/by_user`, `DELETE /api/v1/stores/` |
| Products | `POST /api/v1/products/`, `GET /api/v1/products/by_store`, `GET /api/v1/products/metrics/` (product with full calculation history) |
| Metrics | `POST /api/v1/metrics/` (calculate & save), `POST /api/v1/metrics/custom` (calculate without saving), `GET /api/v1/metrics/by_product` |

## Testing

Unit tests (`tests/unit`) mock repositories and test service logic in isolation. API tests (`tests/api`) exercise routes through `TestClient` with the service layer mocked, so a route's request/response contract is tested independently of business logic.

## Setup Guide

```bash
cd dss_backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

alembic upgrade head

uvicorn src.main:app --reload
```
