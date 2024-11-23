from typing import Optional
import openai
from app.core.ai_config import ai_settings
import logging

logger = logging.getLogger(__name__)

# 配置OpenAI
openai.api_key = ai_settings.OPENAI_API_KEY
openai.api_base = ai_settings.OPENAI_API_BASE

async def generate_divination_answer(
    divination_type: str,
    question: str,
    user_context: Optional[dict] = None
) -> str:
    """
    使用OpenAI生成占卜答案
    """
    try:
        # 根据占卜类型构建提示词
        if divination_type == "answer_book":
            prompt = f"""
            作为一位专业的占卜师，请针对以下问题提供一个简短而有见地的回答：
            问题：{question}
            请从命运的角度给出建议，包含具体的指导。
            """
        
        elif divination_type == "tarot":
            prompt = f"""
            作为一位专业的塔罗牌占卜师，请为以下问题进行塔罗牌解读：
            问题：{question}
            请抽取一张塔罗牌，并详细解释其含义和对问题的启示。
            解读应包含：
            1. 抽到的牌及其正逆位
            2. 该牌的基本含义
            3. 对当前问题的具体指导
            4. 未来的发展建议
            """
        
        elif divination_type == "yijing":
            prompt = f"""
            作为一位专业的易经占卜师，请为以下问题进行六爻卦象解读：
            问题：{question}
            请生成一个卦象，并详细解释其含义和对问题的启示。
            解读应包含：
            1. 所得卦象
            2. 卦象的基本含义
            3. 对当前问题的具体指导
            4. 吉凶判断和建议
            """
        
        else:
            return "暂不支持该占卜类型"

        # 调用OpenAI API
        response = await openai.ChatCompletion.acreate(
            model=ai_settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "你是一位专业的占卜师，精通各种占卜方式，包括答案之书、塔罗牌和易经。"},
                {"role": "user", "content": prompt}
            ],
            temperature=ai_settings.OPENAI_TEMPERATURE,
            max_tokens=ai_settings.OPENAI_MAX_TOKENS
        )

        # 提取生成的答案
        answer = response.choices[0].message.content.strip()
        return answer

    except Exception as e:
        logger.error(f"AI生成答案失败: {str(e)}")
        return "抱歉，占卜服务暂时无法使用，请稍后再试。" 