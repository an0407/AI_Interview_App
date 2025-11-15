from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.schemas.pydantic.qs_gen_llm_pydantic import LLMResponse
from app.config.settings import settings
import json




class LLMService:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=0.2,
            api_key=settings.OPENAI_API_KEY
        )

    async def generate_questions(self, role: str, difficulty: str, count: int, skill_focus: str = "", tech_stack: list = []):
        template = ChatPromptTemplate.from_template(
            """
            You are an AI Interview Question Generator.

            ROLE: {role}
            DIFFICULTY: {difficulty}
            COUNT: {count}
            SKILL FOCUS: {skill_focus}
            TECH STACK: {tech_stack}

            You should generate interview questions based on the provided details.
            You must respond in the following JSON format.
            You need to include all the fields mentioned in the prompt.
            Generate interview questions in JSON ONLY:
            {{
                "questions": [
                    {{
                        "question": "...",
                        "difficulty": "...",
                        "category": "...",
                        "expected_answer": "..."
                    }}
                ],
                "metadata": {{
                    "role": "{role}",
                    "difficulty": "{difficulty}",
                    "total": {count},
                    "skill_focus": "{skill_focus}",
                    "tech_stack": {tech_stack}
                }}
            }}
            """
        )

        parser = JsonOutputParser(pydantic_object=LLMResponse)

        chain = template | self.llm | parser

        try:
            result = await chain.ainvoke({
                "role": role,
                "difficulty": difficulty,
                "count": count,
                "skill_focus": skill_focus,
                "tech_stack": json.dumps(tech_stack)
            })
            return result
        except Exception as e:
            raise Exception(f"LLM Error: {str(e)}")
