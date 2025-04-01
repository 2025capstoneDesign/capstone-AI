import os
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
from typing import Tuple

# .env 파일에서 환경 변수 로드
load_dotenv()

class Config:
    # OpenAI API 설정
    OPENAI_MODEL = "gpt-3.5-turbo"
    OPENAI_TEMPERATURE = 0.3
    OPENAI_MAX_TOKENS = 500
    
    # 토큰 비용 설정 (1M 토큰당)
    TOKEN_COSTS = {
        "gpt-3.5-turbo": {
            "input": 0.50,
            "output": 1.50
        }
    }
    
    # 환율 설정
    EXCHANGE_RATE = 1468.30

class TextProcessor:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            base_url="https://api.openai.com/v1"
        )
        self.token_costs = Config.TOKEN_COSTS
        self.total_tokens = {"input": 0, "output": 0}
        self.EXCHANGE_RATE = Config.EXCHANGE_RATE
        
    def process_sentence(self, sentence: str) -> Tuple[str, float]:
        """단일 문장을 처리하고 비용을 계산합니다."""
        try:
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an AI assistant that refines lecture content. Remove unnecessary interjections and filler words while preserving the core educational content. Keep the lecture's main points and explanations intact."},
                    {"role": "user", "content": sentence}
                ],
                temperature=Config.OPENAI_TEMPERATURE,
                max_tokens=Config.OPENAI_MAX_TOKENS
            )
            
            # 토큰 사용량 계산
            self.total_tokens["input"] += response.usage.prompt_tokens
            self.total_tokens["output"] += response.usage.completion_tokens
            
            return response.choices[0].message.content.strip(), self.calculate_cost()
            
        except Exception as e:
            return f"오류가 발생했습니다: {str(e)}", 0.0
    
    def calculate_cost(self) -> float:
        """토큰 사용량에 따른 비용을 계산합니다."""
        model = Config.OPENAI_MODEL
        input_cost = (self.total_tokens["input"] / 1_000_000) * self.token_costs[model]["input"]
        output_cost = (self.total_tokens["output"] / 1_000_000) * self.token_costs[model]["output"]
        return input_cost + output_cost

def process_batch_text(processor: TextProcessor):
    """testData.txt 파일의 전체 내용을 한 번에 처리합니다."""
    try:
        # 현재 스크립트 파일의 디렉토리 경로를 기준으로 testData.txt 파일 경로 설정
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'testData.txt')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        
        if not text:
            print("파일이 비어있습니다.")
            return
            
        print("\n=== 전체 텍스트 처리 결과 ===")
        print("원본 텍스트:")
        print(text)
        print("\n처리 중...")
        
        processed_text, cost = processor.process_sentence(text)
        
        print("\n처리된 텍스트:")
        print(processed_text)
        print(f"\n총 API 사용 비용: ${cost:.4f} (약 {int(cost * processor.EXCHANGE_RATE)}원)")
        
    except FileNotFoundError:
        print(f"testData.txt 파일을 찾을 수 없습니다. (경로: {file_path})")
    except Exception as e:
        print(f"파일 처리 중 오류가 발생했습니다: {str(e)}")

def process_single_input(processor: TextProcessor):
    """사용자 입력을 받아 단일 문장을 처리합니다."""
    print("\n테스트할 문장을 입력하세요:")
    sentence = input().strip()
    
    if not sentence:
        print("문장이 입력되지 않았습니다.")
        return
    
    print("\n문장 처리 중...")
    processed_text, cost = processor.process_sentence(sentence)
    
    print("\n=== 처리 결과 ===")
    print(f"원본 문장: {sentence}\n")
    print(f"처리된 문장: {processed_text}")
    print(f"\n총 API 사용 비용: ${cost:.4f} (약 {int(cost * processor.EXCHANGE_RATE)}원)")

def main():
    processor = TextProcessor()
    
    while True:
        print("\n=== 메뉴 ===")
        print("1. 직접 입력")
        print("2. testData.txt 전체 텍스트 처리")
        print("3. 종료")
        
        choice = input("\n선택하세요 (1-3): ").strip()
        
        if choice == "1":
            process_single_input(processor)
        elif choice == "2":
            process_batch_text(processor)
        elif choice == "3":
            print("\n프로그램을 종료합니다.")
            break
        else:
            print("\n잘못된 선택입니다. 다시 선택해주세요.")

if __name__ == "__main__":
    main() 