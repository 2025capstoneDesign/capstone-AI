import os
from dotenv import load_dotenv
from openai import OpenAI
import nltk
from datetime import datetime
from typing import List, Tuple
import json
from tqdm import tqdm

# .env 파일에서 환경 변수 로드
load_dotenv()

class Config:
    # 파일 경로 설정
    ASSETS_DIR = "assets"
    DATA_DIR = "text-preprocessing/data"
    
    # 문장 길이 설정
    MIN_SENTENCE_LENGTH = 5
    MAX_SENTENCE_LENGTH = 600
    
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
        """AI를 사용하여 문장을 정제합니다."""
        try:
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an AI assistant that refines lecture content. Remove unnecessary interjections and filler words while preserving the core educational content. Keep the lecture's main points and explanations intact."},
                    {"role": "user", "content": sentence}
                ],
                temperature=Config.OPENAI_TEMPERATURE,
                # max_tokens=Config.OPENAI_MAX_TOKENS
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

class FileManager:
    def __init__(self):
        self.data_dir = Config.DATA_DIR
        os.makedirs(self.data_dir, exist_ok=True)
    
    def save_processed_text(self, text: str, original_filename: str) -> str:
        """처리된 텍스트를 파일로 저장합니다."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{os.path.splitext(original_filename)[0]}_{timestamp}.txt"
        filepath = os.path.join(self.data_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        
        return filepath

class SentenceSplitter:
    def __init__(self):
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        self.MIN_SENTENCE_LENGTH = Config.MIN_SENTENCE_LENGTH
        self.MAX_SENTENCE_LENGTH = Config.MAX_SENTENCE_LENGTH

    def process_sentences(self, sentences: List[str]) -> List[str]:
        processed_sentences = []
        i = 0
        
        while i < len(sentences):
            current_sentence = sentences[i].strip()
            
            # 5자 미만 문장 삭제
            if len(current_sentence) < self.MIN_SENTENCE_LENGTH:
                i += 1
                continue
            
            # 문장 병합 시도
            while i + 1 < len(sentences):
                next_sentence = sentences[i + 1].strip()
                if len(current_sentence) + len(next_sentence) <= self.MAX_SENTENCE_LENGTH:
                    current_sentence = f"{current_sentence} {next_sentence}"
                    i += 1
                else:
                    break
            
            processed_sentences.append(current_sentence)
            i += 1
            
        return processed_sentences

    def split_sentences(self, text: str) -> List[str]:
        sentences = nltk.sent_tokenize(text)
        return self.process_sentences(sentences)

def process_file(file_path: str) -> List[str]:
    """파일을 읽어서 문장을 분리합니다."""
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    splitter = SentenceSplitter()
    return splitter.split_sentences(text)

def main():
    processor = TextProcessor()
    file_manager = FileManager()
    
    assets_dir = Config.ASSETS_DIR
    txt_files = [f for f in os.listdir(assets_dir) if f.endswith('.txt')]
    
    if not txt_files:
        print("assets 폴더에 txt 파일이 없습니다.")
        print(f"assets 폴더 경로: {assets_dir}")
        print("txt 파일을 assets 폴더에 넣어주세요.")
        return
    
    print("\n사용 가능한 파일 목록:")
    for i, file in enumerate(txt_files, 1):
        print(f"{i}. {file}")
    
    while True:
        try:
            file_idx = int(input("\n처리할 파일 번호를 입력하세요: ")) - 1
            if 0 <= file_idx < len(txt_files):
                break
            print("잘못된 번호입니다. 다시 입력해주세요.")
        except ValueError:
            print("숫자를 입력해주세요.")
    
    selected_file = txt_files[file_idx]
    file_path = os.path.join(assets_dir, selected_file)
    
    print("\n텍스트 처리 중...")
    sentences = process_file(file_path)
    
    if not sentences:
        print("문장 분리에 실패했습니다.")
        return
    
    print(f"\n총 {len(sentences)}개의 문장이 분리되었습니다.")
    
    while True:
        print("\n1. 문장 보기")
        print("2. 결과 txt 저장")
        print("3. AI 전처리")
        print("4. 종료")
        
        choice = input("\n선택하세요 (1-4): ")
        
        if choice == '1':
            print("\n=== 분리된 문장 ===")
            for i, sentence in enumerate(sentences, 1):
                print(f"\n{i}. {sentence}")
        
        elif choice == '2':
            final_text = "\n    ".join(sentences)
            saved_path = file_manager.save_processed_text(final_text, selected_file)
            print(f"\n파일이 저장되었습니다: {saved_path}")
        
        elif choice == '3':
            print("\nAI 전처리 중...")
            processed_sentences = []
            total_cost = 0
            
            for sentence in tqdm(sentences, desc="문장 처리 중"):
                processed_text, cost = processor.process_sentence(sentence)
                processed_sentences.append(processed_text)
                total_cost += cost
            
            print(f"\nAI 전처리 완료!")
            print(f"총 API 사용 비용: ${total_cost:.4f} (약 {int(total_cost * processor.EXCHANGE_RATE)}원)")
            
            while True:
                print("\n1. 처리된 문장 보기")
                print("2. 처리된 결과 저장")
                print("3. 이전 메뉴로")
                
                sub_choice = input("\n선택하세요 (1-3): ")
                
                if sub_choice == '1':
                    print("\n=== AI 처리된 문장 ===")
                    for i, sentence in enumerate(processed_sentences, 1):
                        print(f"\n{i}. {sentence}")
                
                elif sub_choice == '2':
                    final_text = "\n    ".join(processed_sentences)
                    saved_path = file_manager.save_processed_text(final_text, f"ai_processed_{selected_file}")
                    print(f"\n파일이 저장되었습니다: {saved_path}")
                
                elif sub_choice == '3':
                    break
                
                else:
                    print("잘못된 선택입니다. 다시 선택해주세요.")
        
        elif choice == '4':
            print("프로그램을 종료합니다.")
            break
        
        else:
            print("잘못된 선택입니다. 다시 선택해주세요.")

if __name__ == "__main__":
    main() 