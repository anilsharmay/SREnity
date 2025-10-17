"""
Configuration management for SREnity
"""
import os
from typing import Optional
from dataclasses import dataclass
from langchain_openai import OpenAIEmbeddings, ChatOpenAI


@dataclass
class Config:
    """Configuration class for SREnity application"""
    
    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    
    # Qdrant Configuration (for vector storage)
    qdrant_url: str = "../qdrant_db"
    qdrant_collection_name: str = "srenity_runbooks"
    
    # External APIs for enhanced retrieval
    tavily_api_key: str = None
    cohere_api_key: str = None
    
    # Observability
    langsmith_api_key: str = None
    langsmith_project: str = "srenity"
    
    # Application Configuration
    log_level: str = "INFO"
    max_tokens: int = 4000
    temperature: float = 0.1
    
    # Data Configuration
    data_dir: str = "data"
    runbooks_dir: str = "data/runbooks"
    synthetic_incidents_dir: str = "data/synthetic_incidents"
    
    @classmethod
    def from_env(cls) -> 'Config':
        """Create configuration from environment variables"""
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        return cls(
            openai_api_key=openai_api_key,
            # Only read sensitive data from env, use defaults for everything else
            tavily_api_key=os.getenv("TAVILY_API_KEY"),
            cohere_api_key=os.getenv("COHERE_API_KEY"),
            langsmith_api_key=os.getenv("LANGSMITH_API_KEY"),
            langsmith_project=os.getenv("LANGCHAIN_PROJECT", "srenity")
        )


class ModelFactory:
    """Factory class for creating model instances with centralized configuration"""
    
    def __init__(self, config: Config):
        self.config = config
    
    def get_embeddings(self):
        """Get embeddings model instance"""
        return OpenAIEmbeddings(
            model=self.config.openai_embedding_model,
            openai_api_key=self.config.openai_api_key
        )
    
    def get_llm(self):
        """Get LLM model instance"""
        return ChatOpenAI(
            model=self.config.openai_model,
            openai_api_key=self.config.openai_api_key,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
    
    def get_llm_for_streaming(self):
        """Get LLM model instance configured for streaming"""
        return ChatOpenAI(
            model=self.config.openai_model,
            openai_api_key=self.config.openai_api_key,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            streaming=True
        )


# Global config instance
config: Optional[Config] = None


def get_config() -> Config:
    """Get global configuration instance"""
    global config
    if config is None:
        config = Config.from_env()
    return config


def set_config(new_config: Config) -> None:
    """Set global configuration instance"""
    global config
    config = new_config


def get_model_factory() -> ModelFactory:
    """Get model factory instance"""
    return ModelFactory(get_config())
