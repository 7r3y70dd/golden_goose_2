This is the first state of the readme.md

please add and delete from this to document changes as you go

this application is meant to search for the best stock options trades with eventual automated trading.

this application should be designed with security in mind

it should follow the api style and have a ui element

## Data Schemas

The application uses typed schemas for market data including equity bars and options contracts. These schemas define the canonical structure for OHLCV data, options chains, implied volatility, and open interest.

### Files

- `app/data/schemas.py` - Contains data models for equity bars and options contracts
- `app/data/validators.py` - Contains validation helpers for market data
- `tests/test_data_schemas.py` - Unit tests for data schemas and validators

## Data Providers

The application uses a provider abstraction to support multiple market data backends.

### Files

- `app/data/providers/base.py` - Abstract base class for market data providers
- `app/data/providers/mock.py` - Mock implementation for development and testing
- `tests/test_provider_interface.py` - Unit tests for provider interface and mock implementation

## Data Storage

The application uses a parquet-based storage layer for persisting historical market data.

### Files

- `app/data/storage.py` - Storage layer implementation using parquet files
- `app/data/repository.py` - Repository layer providing clean interface for data access
- `tests/test_storage.py` - Unit tests for storage and repository functionality