#!/usr/bin/env python3
"""
AI Manager - Handles AI model interactions and responses.

Copyright (C) 2073-2025 Prof. B3, University of Temporal Transfer
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"O copyright e d'o pateterno" - Copyright belongs to the ancestors
Knowledge flows freely across timelines and dimensions.
"""

import requests
import json
import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

@dataclass
class ModelConfig:
    name: str
    endpoint: str
    temperature: float = 0.7
    max_tokens: int = 2048
    context_length: int = 4096

class AIManager:
    """Manages AI model interactions and model switching."""
    
    def __init__(self, config_path: str = "config/ai_models.json"):
        self.config_path = config_path
        self.models: Dict[str, ModelConfig] = {}
        self.current_model: Optional[str] = None
        self.ollama_base_url = "http://localhost:11434"
        self.logger = logging.getLogger(__name__)
        self.session = self._create_session()
        self.load_models()
    
    def _create_session(self) -> requests.Session:
        """Create a requests session with retry logic and better timeout handling."""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def test_ollama_connection(self) -> Dict[str, Any]:
        """Test if Ollama server is reachable and responding."""
        try:
            # Test basic connectivity
            response = self.session.get(
                f"{self.ollama_base_url}/api/tags",
                timeout=10
            )
            
            if response.status_code == 200:
                models = response.json().get("models", [])
                available_models = [model.get("name", "") for model in models]
                
                return {
                    "status": "connected",
                    "available_models": available_models,
                    "response_time": response.elapsed.total_seconds()
                }
            else:
                return {
                    "status": "error",
                    "error": f"HTTP {response.status_code}",
                    "available_models": []
                }
                
        except requests.exceptions.Timeout:
            return {
                "status": "timeout",
                "error": "Connection timeout",
                "available_models": []
            }
        except requests.exceptions.ConnectionError:
            return {
                "status": "connection_error",
                "error": "Cannot connect to Ollama server",
                "available_models": []
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "available_models": []
            }
    
    def load_models(self):
        """Load model configurations from JSON file."""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                for model_name, model_data in config.items():
                    self.models[model_name] = ModelConfig(**model_data)
            self.logger.info(f"Loaded {len(self.models)} AI models")
        except FileNotFoundError:
            self.logger.warning(f"Config file {self.config_path} not found, using defaults")
            self._create_default_models()
    
    def _create_default_models(self):
        """Create default model configurations."""
        default_models = {
            "mixtral": ModelConfig(
                name="mixtral:latest",
                endpoint="/api/generate",
                temperature=0.7,
                max_tokens=2048
            ),
            "llama3.2": ModelConfig(
                name="llama3.2:3b",
                endpoint="/api/generate", 
                temperature=0.8,
                max_tokens=1024
            ),
            "codellama": ModelConfig(
                name="codellama:latest",
                endpoint="/api/generate",
                temperature=0.3,
                max_tokens=4096
            )
        }
        self.models.update(default_models)
    
    def set_model(self, model_name: str) -> bool:
        """Set the current active model."""
        if model_name in self.models:
            self.current_model = model_name
            self.logger.info(f"Switched to model: {model_name}")
            return True
        else:
            self.logger.error(f"Model {model_name} not found")
            return False
    
    def get_model_status(self) -> Dict[str, Any]:
        """Get status of all models."""
        status = {}
        connection_status = self.test_ollama_connection()
        
        if connection_status["status"] != "connected":
            # If Ollama is not available, mark all models as unavailable
            for model_name in self.models:
                status[model_name] = False
            return status
        
        available_models = connection_status["available_models"]
        
        for model_name in self.models:
            try:
                model_config = self.models[model_name]
                status[model_name] = any(
                    model.startswith(model_config.name)
                    for model in available_models
                )
            except Exception as e:
                self.logger.error(f"Error checking model {model_name}: {e}")
                status[model_name] = False
        return status
    
    def generate_response(self, prompt: str, model_name: Optional[str] = None, max_retries: int = 2) -> str:
        """Generate a response using the specified or current model with retry logic."""
        if model_name:
            if not self.set_model(model_name):
                return "Error: Model not found"
        
        if not self.current_model:
            self.current_model = list(self.models.keys())[0]
        
        model_config = self.models[self.current_model]
        
        # Test connection first
        connection_status = self.test_ollama_connection()
        if connection_status["status"] != "connected":
            self.logger.error(f"Ollama not available: {connection_status['error']}")
            return self._generate_fallback_response(prompt)
        
        for attempt in range(max_retries + 1):
            try:
                payload = {
                    "model": model_config.name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": model_config.temperature,
                        "num_predict": model_config.max_tokens
                    }
                }
                
                # Use shorter timeout for retries
                timeout = 60 if attempt == 0 else 30
                
                response = self.session.post(
                    f"{self.ollama_base_url}{model_config.endpoint}",
                    json=payload,
                    timeout=timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("response", "No response generated")
                else:
                    self.logger.error(f"API request failed: {response.status_code}")
                    if attempt == max_retries:
                        return f"Error: API request failed with status {response.status_code}"
                    
            except requests.exceptions.Timeout:
                self.logger.warning(f"Timeout on attempt {attempt + 1}/{max_retries + 1}")
                if attempt == max_retries:
                    return self._generate_fallback_response(prompt)
                time.sleep(2 ** attempt)  # Exponential backoff
                
            except Exception as e:
                self.logger.error(f"Error generating response (attempt {attempt + 1}): {e}")
                if attempt == max_retries:
                    return self._generate_fallback_response(prompt)
                time.sleep(1)
        
        return self._generate_fallback_response(prompt)
    
    def _generate_fallback_response(self, prompt: str) -> str:
        """Generate a fallback response when AI service is unavailable."""
        self.logger.warning("Using fallback response generator")
        
        # Simple template-based fallback for common requests
        prompt_lower = prompt.lower()
        
        if "create a python module" in prompt_lower or "generate code" in prompt_lower:
            return self._generate_fallback_module_code(prompt)
        elif "analyze" in prompt_lower:
            return self._generate_fallback_analysis(prompt)
        else:
            return """I apologize, but the AI service is currently unavailable. 

To resolve this issue:
1. Make sure Ollama is running: ollama serve
2. Check if your models are downloaded: ollama list
3. Try restarting Ollama: ollama stop && ollama serve

For now, I'll provide a basic template response. Please try again when the AI service is available."""
    
    def _generate_fallback_module_code(self, prompt: str) -> str:
        """Generate basic module code template when AI is unavailable."""
        return '''#!/usr/bin/env python3
"""
Auto-generated module template.
Generated when AI service was unavailable.
Please customize this template for your specific needs.
"""

import logging
from typing import Dict, Any, Optional
from pathlib import Path

class TemplateManager:
    """Template manager class - customize for your needs."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = {}
    
    def initialize(self) -> bool:
        """Initialize the manager."""
        try:
            self.logger.info("Template manager initialized")
            return True
        except Exception as e:
            self.logger.error(f"Initialization failed: {e}")
            return False
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data - customize this method."""
        try:
            # Add your processing logic here
            result = {"status": "processed", "data": data}
            self.logger.info("Data processed successfully")
            return result
        except Exception as e:
            self.logger.error(f"Processing failed: {e}")
            return {"status": "error", "error": str(e)}

def main():
    """Main function for CLI usage."""
    manager = TemplateManager()
    if manager.initialize():
        print("Template manager ready")
    else:
        print("Template manager initialization failed")

if __name__ == "__main__":
    main()
'''
    
    def _generate_fallback_analysis(self, prompt: str) -> str:
        """Generate basic analysis template when AI is unavailable."""
        return '''{
    "issues": ["AI service unavailable - manual review recommended"],
    "improvements": ["Add error handling", "Improve documentation", "Add type hints"],
    "risk_level": "medium",
    "priority": "medium"
}'''
    
    def stream_response(self, prompt: str, model_name: Optional[str] = None):
        """Stream response from the AI model."""
        if model_name:
            if not self.set_model(model_name):
                yield "Error: Model not found"
                return
        
        if not self.current_model:
            self.current_model = list(self.models.keys())[0]
        
        model_config = self.models[self.current_model]
        
        # Test connection first
        connection_status = self.test_ollama_connection()
        if connection_status["status"] != "connected":
            yield f"Error: Ollama not available - {connection_status['error']}"
            return
        
        try:
            payload = {
                "model": model_config.name,
                "prompt": prompt,
                "stream": True,
                "options": {
                    "temperature": model_config.temperature,
                    "num_predict": model_config.max_tokens
                }
            }
            
            response = self.session.post(
                f"{self.ollama_base_url}{model_config.endpoint}",
                json=payload,
                stream=True,
                timeout=60
            )
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line.decode('utf-8'))
                            if 'response' in data:
                                yield data['response']
                            if data.get('done', False):
                                break
                        except json.JSONDecodeError:
                            continue
            else:
                yield f"Error: API request failed with status {response.status_code}"
                
        except Exception as e:
            self.logger.error(f"Error streaming response: {e}")
            yield f"Error: {str(e)}"
    
    def download_model(self, model_name: str) -> bool:
        """Download a model to Ollama."""
        try:
            payload = {"name": model_name}
            response = self.session.post(
                f"{self.ollama_base_url}/api/pull",
                json=payload,
                timeout=300
            )
            
            if response.status_code == 200:
                self.logger.info(f"Successfully downloaded model: {model_name}")
                return True
            else:
                self.logger.error(f"Failed to download model {model_name}: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error downloading model {model_name}: {e}")
            return False

    def analyze_code(self, code_content: str, file_path: Optional[str] = None) -> Dict[str, Any]:
        """Analyze code for improvements using AI"""
        import json
        import re
        analysis_prompt = f"""
        Analyze this Python code for improvements. Focus on:
        1. Performance issues
        2. Bug potential  
        3. Code clarity
        4. Error handling
        
        Code to analyze:
        ```python
        {code_content[:1500]}
        ```
        
        Respond with JSON format:
        {{
            "issues": ["specific issue 1", "specific issue 2"],
            "improvements": ["specific improvement 1", "specific improvement 2"], 
            "risk_level": "low|medium|high",
            "priority": "low|medium|high"
        }}
        """
        response = self.generate_response(analysis_prompt)
        # Enhanced JSON parsing
        try:
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
                required_fields = ["issues", "improvements", "risk_level", "priority"]
                if all(field in analysis for field in required_fields):
                    return analysis
        except (json.JSONDecodeError, Exception):
            pass
        # Intelligent fallback parsing
        return self._parse_analysis_fallback(response)

    def _parse_analysis_fallback(self, response: str) -> Dict[str, Any]:
        """Fallback parsing when JSON extraction fails"""
        issues = []
        improvements = []
        risk_level = "medium"
        priority = "medium"
        lines = response.lower().split('\n')
        for line in lines:
            line = line.strip()
            if any(keyword in line for keyword in ['issue', 'problem', 'bug', 'error']):
                issues.append(line)
            elif any(keyword in line for keyword in ['improve', 'optimize', 'better', 'enhance']):
                improvements.append(line)
            elif 'high risk' in line or 'dangerous' in line:
                risk_level = "high"
            elif 'low risk' in line or 'safe' in line:
                risk_level = "low"
            elif 'critical' in line or 'urgent' in line:
                priority = "high"
        return {
            "issues": issues[:3] if issues else ["No specific issues identified"],
            "improvements": improvements[:3] if improvements else ["Add documentation"],
            "risk_level": risk_level,
            "priority": priority
        }

    def generate_code(self, specification: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate improved code based on specification"""
        import json
        prompt = f"""
        Generate improved Python code based on this specification:
        {specification}
        
        Context: {json.dumps(context) if context else 'None provided'}
        
        Requirements:
        - Keep existing functionality
        - Make minimal, safe changes only
        - Add proper error handling
        - Improve readability
        - Return ONLY the code, no explanations
        """
        response = self.generate_response(prompt)
        # Extract code from response
        if '```python' in response:
            start = response.find('```python') + 9
            end = response.find('```', start)
            if end > start:
                return response[start:end].strip()
        elif '```' in response:
            start = response.find('```') + 3
            end = response.find('```', start)
            if end > start:
                return response[start:end].strip()
        return response.strip() 