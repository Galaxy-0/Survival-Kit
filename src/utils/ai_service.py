"""
AI服务工具模块
"""
import os
from typing import Dict, Any, Optional
import requests
from .logger import setup_logger
from .config_loader import load_config
from datetime import datetime

logger = setup_logger('ai_service')

class AIService:
    def __init__(self):
        """初始化AI服务"""
        config = load_config()
        self.provider = config.get('ai_provider', 'deepseek')
        self.api_key = config.get('ai_api_key')
        self.api_base = config.get('ai_api_base')
        
        if not self.api_key:
            raise ValueError("未设置AI API密钥")
            
    def analyze_text(self, text: str, max_tokens: int = 1000) -> Optional[str]:
        """
        分析文本内容
        
        Args:
            text: 要分析的文本
            max_tokens: 最大token数
            
        Returns:
            str: 分析结果
        """
        try:
            if self.provider == 'deepseek':
                return self._call_deepseek_api(text, max_tokens)
            elif self.provider == 'openai':
                return self._call_openai_api(text, max_tokens)
            else:
                raise ValueError(f"不支持的AI提供商: {self.provider}")
        except Exception as e:
            logger.error(f"AI分析失败: {str(e)}")
            return None
            
    def _call_deepseek_api(self, text: str, max_tokens: int) -> str:
        """调用Deepseek API"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'deepseek-chat',
            'messages': [
                {
                    'role': 'user',
                    'content': text
                }
            ],
            'max_tokens': max_tokens
        }
        
        response = requests.post(
            f"{self.api_base}/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            raise Exception(f"Deepseek API调用失败: {response.text}")
            
    def _call_openai_api(self, text: str, max_tokens: int) -> str:
        """调用OpenAI API"""
        import openai
        openai.api_key = self.api_key
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": text}
            ],
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
        
    def analyze_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析项目数据
        
        Args:
            project_data: 项目相关数据
            
        Returns:
            Dict[str, Any]: 分析结果
        """
        # 构建分析提示
        prompt = f"""
        请分析以下GitHub项目的商业价值：
        
        项目名称：{project_data.get('name')}
        描述：{project_data.get('description')}
        星标数：{project_data.get('stars')}
        分叉数：{project_data.get('forks')}
        主要语言：{project_data.get('language')}
        许可证：{project_data.get('license')}
        
        请从以下几个方面进行分析：
        1. 技术价值
        2. 市场潜力
        3. 变现可能性
        4. 开发难度
        5. 具体建议
        """
        
        result = self.analyze_text(prompt)
        if not result:
            return {}
            
        # 这里可以添加结果解析逻辑
        return {
            'analysis': result,
            'timestamp': datetime.now().isoformat()
        } 