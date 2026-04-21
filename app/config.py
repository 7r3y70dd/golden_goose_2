import os
from typing import Optional
from pydantic import BaseSettings


class DataConfig(BaseSettings):
    """
    Configuration for data handling.
    """
    data_refresh_interval: int = 300
    data_storage_path: str = "/tmp/data"
    data_freshness_threshold: int = 3600


class DatabaseConfig(BaseSettings):
    """
    Configuration for database connections.
    """
    db_url: str = "sqlite:///app.db"
    db_pool_size: int = 10
    db_max_overflow: int = 20


class ModelConfig(BaseSettings):
    """
    Configuration for model settings.
    """
    model_path: str = "models/model.pkl"
    model_threshold: float = 0.5
    model_features: list = ["feature1", "feature2"]


class UIConfig(BaseSettings):
    """
    Configuration for UI settings.
    """
    ui_host: str = "localhost"
    ui_port: int = 8000
    ui_debug: bool = True


class LoggingConfig(BaseSettings):
    """
    Configuration for logging.
    """
    log_level: str = "INFO"
    log_file: str = "app.log"


class LabelConfig(BaseSettings):
    """
    Configuration for label generation.
    """
    default_label_window: int = 30
    default_threshold: float = 0.1
    supported_symbols: list = []
    labeling_enabled: bool = True


class AppConfig(BaseSettings):
    """
    Main application configuration.
    """
    data: DataConfig = DataConfig()
    database: DatabaseConfig = DatabaseConfig()
    model: ModelConfig = ModelConfig()
    ui: UIConfig = UIConfig()
    logging: LoggingConfig = LoggingConfig()
    label: LabelConfig = LabelConfig()

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global config instance
config = AppConfig()

class Config:
    """
    Application configuration.
    """
    # ... existing config ...
    
    # Liquidity thresholds
    LIQUIDITY_MIN_VOLUME: int = int(os.getenv('LIQUIDITY_MIN_VOLUME', '1000'))
    LIQUIDITY_MIN_OPEN_INTEREST: int = int(os.getenv('LIQUIDITY_MIN_OPEN_INTEREST', '100'))
    LIQUIDITY_MAX_SPREAD_WIDTH: float = float(os.getenv('LIQUIDITY_MAX_SPREAD_WIDTH', '0.05'))

    # ... existing config ...
