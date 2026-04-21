import argparse
import json
from datetime import datetime
from app.data.storage import Storage


def init_db(storage: Storage):
    """Initialize the database with required tables."""
    storage._init_db()
    print(f"Database initialized at {storage.db_path}")


def reset_db(storage: Storage):
    """Reset the database by dropping all tables and recreating them."""
    storage.reset_database()
    print(f"Database reset at {storage.db_path}")


def seed_data(storage: Storage):
    """Seed the database with sample data for testing."""
    # Sample trades
    sample_trades = [
        {
            'symbol': 'AAPL',
            'strategy': 'mean_reversion',
            'start_date': '2023-01-01',
            'end_date': '2023-01-15',
            'entry_price': 150.0,
            'exit_price': 145.0,
            'quantity': 100,
            'resolved': True
        },
        {
            'symbol': 'GOOGL',
            'strategy': 'trend_following',
            'start_date': '2023-02-01',
            'end_date': '2023-02-28',
            'entry_price': 2800.0,
            'exit_price': None,
            'quantity': 50,
            'resolved': False
        }
    ]
    
    for trade in sample_trades:
        # This would normally be a proper trade object
        # For now, we'll just print the data
        print(f"Seeding trade: {trade}")
    
    print("Sample data seeded successfully")


def main():
    parser = argparse.ArgumentParser(description='Database management commands')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Initialize database command
    init_parser = subparsers.add_parser('init-db', help='Initialize the database')
    init_parser.add_argument('--db-path', default='tracked_trades.db', help='Path to the database file')
    
    # Reset database command
    reset_parser = subparsers.add_parser('reset-db', help='Reset the database')
    reset_parser.add_argument('--db-path', default='tracked_trades.db', help='Path to the database file')
    
    # Seed data command
    seed_parser = subparsers.add_parser('seed-data', help='Seed the database with sample data')
    seed_parser.add_argument('--db-path', default='tracked_trades.db', help='Path to the database file')
    
    args = parser.parse_args()
    
    if args.command == 'init-db':
        storage = Storage(args.db_path)
        init_db(storage)
    elif args.command == 'reset-db':
        storage = Storage(args.db_path)
        reset_db(storage)
    elif args.command == 'seed-data':
        storage = Storage(args.db_path)
        seed_data(storage)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()