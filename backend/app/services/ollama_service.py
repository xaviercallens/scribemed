"""Ollama service for local LLM inference."""
import ollama
from typing import Dict, Any, Optional
import logging

from ..config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class OllamaService:
    """Service for interacting with local Ollama models."""
    
    def __init__(self, model: Optional[str] = None):
        """Initialize Ollama service.
        
        Args:
            model: Model name to use (defaults to settings.ollama_model)
        """
        self.model = model or settings.ollama_model
        self.base_url = settings.ollama_base_url
        logger.info(f"Initialized Ollama service with model: {self.model}")
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate text using Ollama.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt for context
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional Ollama parameters
            
        Returns:
            Dict with 'response' and metadata
        """
        try:
            messages = []
            
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            logger.info(f"Generating with {self.model}, temp={temperature}")
            
            response = ollama.chat(
                model=self.model,
                messages=messages,
                options={
                    "temperature": temperature,
                    "num_predict": max_tokens,
                    **kwargs
                }
            )
            
            return {
                "response": response['message']['content'],
                "model": self.model,
                "done": response.get('done', True),
                "total_duration": response.get('total_duration'),
                "load_duration": response.get('load_duration'),
                "prompt_eval_count": response.get('prompt_eval_count'),
                "eval_count": response.get('eval_count'),
            }
            
        except Exception as e:
            logger.error(f"Ollama generation failed: {e}")
            raise Exception(f"Failed to generate with Ollama: {str(e)}")
    
    def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        **kwargs
    ):
        """Generate text with streaming response.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt
            temperature: Sampling temperature
            **kwargs: Additional parameters
            
        Yields:
            Response chunks
        """
        try:
            messages = []
            
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            stream = ollama.chat(
                model=self.model,
                messages=messages,
                stream=True,
                options={
                    "temperature": temperature,
                    **kwargs
                }
            )
            
            for chunk in stream:
                yield chunk['message']['content']
                
        except Exception as e:
            logger.error(f"Ollama streaming failed: {e}")
            raise Exception(f"Failed to stream with Ollama: {str(e)}")
    
    def check_model_available(self) -> bool:
        """Check if the configured model is available.
        
        Returns:
            True if model is available, False otherwise
        """
        try:
            models_response = ollama.list()
            available_models = [m.model for m in models_response.models]
            return self.model in available_models
        except Exception as e:
            logger.error(f"Failed to check model availability: {e}")
            return False
    
    def pull_model(self) -> bool:
        """Pull the model if not available.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Pulling model: {self.model}")
            ollama.pull(self.model)
            return True
        except Exception as e:
            logger.error(f"Failed to pull model: {e}")
            return False


# Singleton instance
_ollama_service: Optional[OllamaService] = None


def get_ollama_service() -> OllamaService:
    """Get or create Ollama service instance.
    
    Returns:
        OllamaService instance
    """
    global _ollama_service
    if _ollama_service is None:
        _ollama_service = OllamaService()
    return _ollama_service
