"""Configuration service for dependency injection."""

import os
from enum import Enum

from dotenv import load_dotenv

from game_ai import RandomSelection, StrategicAI
from game_engine import StandardGameEngine
from storage import InMemoryGameStorage

# Load environment variables from .env file if it exists
load_dotenv()


class Environment(str, Enum):
    """Environment enumeration."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


class ConfigService:
    """Service for managing application configuration and dependencies."""

    def __init__(self, environment: Environment | None = None) -> None:
        """Initialize the configuration service.

        Args:
            environment: The environment to use. If None, will be determined from
                        the ENVIRONMENT environment variable or default to DEVELOPMENT.
        """
        if environment is None:
            env_str = os.getenv("ENVIRONMENT", "development").lower()
            try:
                self.environment = Environment(env_str)
            except ValueError:
                self.environment = Environment.DEVELOPMENT
        else:
            self.environment = environment

        # Initialize dependencies
        self._storage = None
        self._engine = None
        self._ai = None

    def get_storage(self):
        """Get the storage service instance.

        Returns:
            Storage service instance (configured based on environment).
        """
        if self._storage is None:
            self._storage = self._create_storage()
        return self._storage

    def get_engine(self):
        """Get the game engine instance.

        Returns:
            Game engine instance (configured based on environment).
        """
        if self._engine is None:
            self._engine = self._create_engine()
        return self._engine

    def get_ai(self):
        """Get the AI instance.

        Returns:
            AI instance (configured based on environment).
        """
        if self._ai is None:
            self._ai = self._create_ai()
        return self._ai

    def _create_storage(self):
        """Create storage service based on environment.

        Returns:
            Storage service instance.
        """
        # For now, all environments use in-memory storage
        # In the future, production could use database storage, etc.
        if self.environment == Environment.TESTING:
            # Testing might want a fresh storage for each test
            return InMemoryGameStorage()
        elif self.environment == Environment.PRODUCTION:
            # Production could use persistent storage
            # TODO: Implement persistent storage when needed
            return InMemoryGameStorage()
        else:
            # Development and staging use in-memory
            return InMemoryGameStorage()

    def _create_engine(self):
        """Create game engine based on environment.

        Returns:
            Game engine instance.
        """
        # All environments use StandardGameEngine for now
        return StandardGameEngine()

    def _create_ai(self):
        """Create AI instance based on environment.

        Returns:
            AI instance.
        """
        engine = self.get_engine()

        # Determine AI type from environment variable or default
        ai_type = os.getenv("AI_TYPE", "strategic").lower()

        if ai_type == "random":
            return RandomSelection(engine)
        else:
            return StrategicAI(engine)

