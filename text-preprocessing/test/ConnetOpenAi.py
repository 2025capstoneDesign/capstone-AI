import os
from dotenv import load_dotenv
from openai import OpenAI
import nltk

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url="https://api.openai.com/v1"
)

nltk.download('punkt')

def get_ai_response(user_input):
    try:
        # API 호출
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 도움이 되는 AI 어시스턴트입니다."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        # 응답 반환
        return response.choices[0].message.content
    except Exception as e:
        return f"오류가 발생했습니다: {str(e)}"

def main():
    print("AI 챗봇에 오신 것을 환영합니다! (종료하려면 'quit' 또는 'exit'를 입력하세요)")
    
    while True:
        user_input = input("\n사용자: ")
        
        if user_input.lower() in ['quit', 'exit']:
            print("대화를 종료합니다.")
            break
            
        response = get_ai_response(user_input)
        print("\nAI:", response)

if __name__ == "__main__":
    main() 