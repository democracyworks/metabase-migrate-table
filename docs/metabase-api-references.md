# Metabase API references

This file captures the key external references used to migrate this repository to MBQL 5 behavior.
Use it as the starting point for future maintenance.

## Official documentation

- API changelog page: https://www.metabase.com/docs/latest/developers-guide/api-changelog
- API reference page: https://www.metabase.com/docs/latest/api
- API changelog source in Metabase repo: https://github.com/metabase/metabase/blob/master/docs/developers-guide/api-changelog.md
- API keys docs: https://github.com/metabase/metabase/blob/master/docs/people-and-groups/api-keys.md

## Route and endpoint mounting

- API route map: https://github.com/metabase/metabase/blob/master/src/metabase/api_routes/routes.clj

Relevant mounted paths:

- `/api/card`
- `/api/cards`
- `/api/dashboard`
- `/api/table`
- `/api/field`

## Card endpoint behavior

- Card API implementation: https://github.com/metabase/metabase/blob/master/src/metabase/queries_rest/api/card.clj

Important MBQL 5 note:

- `GET /api/card/:id` returns MBQL 5 by default in v57+.
- `GET /api/card/:id?legacy-mbql=true` returns legacy MBQL shape for compatibility.

## Stable endpoints used by this repository

- Query cards for table: `GET /api/card?f=table&model_id=<table_id>`
  Source: https://github.com/metabase/metabase/blob/master/src/metabase/queries_rest/api/card.clj
- Card-to-dashboard lookup: `POST /api/cards/dashboards`
  Source: https://github.com/metabase/metabase/blob/master/src/metabase/queries_rest/api/cards.clj
- Table metadata: `GET /api/table/:id/query_metadata`
  Source: https://github.com/metabase/metabase/blob/master/src/metabase/warehouse_schema_rest/api/table.clj
- Field lookup: `GET /api/field/:id`
  Source: https://github.com/metabase/metabase/blob/master/src/metabase/warehouse_schema_rest/api/field.clj
- Update card: `PUT /api/card/:id`
  Source: https://github.com/metabase/metabase/blob/master/src/metabase/queries_rest/api/card.clj

## MBQL 5 structural references

- MBQL 5 query schema: https://github.com/metabase/metabase/blob/master/src/metabase/lib/schema.cljc
- MBQL ref schema (`:field`, `:aggregation`, `:expression`): https://github.com/metabase/metabase/blob/master/src/metabase/lib/schema/ref.cljc
- Legacy <-> MBQL 5 conversion internals: https://github.com/metabase/metabase/blob/master/src/metabase/lib/convert.cljc
- Query construction and conversion flow: https://github.com/metabase/metabase/blob/master/src/metabase/lib/query.cljc

## Auth references

- Session and API-key middleware behavior: https://github.com/metabase/metabase/blob/master/src/metabase/server/middleware/session.clj
- Static API-key middleware notes: https://github.com/metabase/metabase/blob/master/src/metabase/api/routes/common.clj

## Repository-specific migration notes

- This repository now assumes MBQL 5 for query cards.
- Environment variables are required:
  - `METABASE_API_KEY`
  - `METABASE_BASE_URL` (including `/api`)
- Main execution path is `main.py`.
