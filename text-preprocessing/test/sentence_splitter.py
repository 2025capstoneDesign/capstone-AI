import nltk
from nltk.tokenize import sent_tokenize
import os

class SentenceSplitter:
    def __init__(self):
        # NLTK 데이터 다운로드 (처음 실행시에만 필요)
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        self.MIN_SENTENCE_LENGTH = 5  # 최소 문장 길이 (불충족시 삭제)
        self.MAX_SHORT_SENTENCE_LENGTH = 100  # 짧은 문장으로 간주할 최대 길이 (30글자 이하 문장 병합)
        self.MAX_SENTENCE_LENGTH = 400  # 문장 병합 시 최대 길이 제한

    def process_sentences(self, sentences):
        """문장들을 처리하여 짧은 문장을 처리"""
        processed_sentences = []
        i = 0
        
        while i < len(sentences):
            current_sentence = sentences[i].strip()
            
            # 1. MIN_SENTENCE_LENGTH 미만인 문장은 무조건 삭제
            if len(current_sentence) < self.MIN_SENTENCE_LENGTH:
                i += 1
                continue
            
            # 2. MAX_SHORT_SENTENCE_LENGTH 이하인 문장은 무조건 병합 시도
            if len(current_sentence) <= self.MAX_SHORT_SENTENCE_LENGTH:
                merged = False
                
                # 다음 문장이 있는 경우
                if i + 1 < len(sentences):
                    next_sentence = sentences[i + 1].strip()
                    # 다음 문장과 병합 시도
                    if len(current_sentence) + len(next_sentence) <= self.MAX_SENTENCE_LENGTH:
                        current_sentence = f"{current_sentence} {next_sentence}"
                        i += 2
                        merged = True
                
                # 이전 문장이 있는 경우
                if not merged and i > 0 and processed_sentences:
                    prev_sentence = processed_sentences[-1]
                    # 이전 문장과 병합 시도
                    if len(prev_sentence) + len(current_sentence) <= self.MAX_SENTENCE_LENGTH:
                        processed_sentences[-1] = f"{prev_sentence} {current_sentence}"
                        i += 1
                        merged = True
                
                # 병합이 성공했다면, 병합된 문장이 여전히 짧은지 확인하고 계속 처리
                if merged:
                    # 병합된 문장이 여전히 짧다면 다시 처리
                    if len(current_sentence) <= self.MAX_SHORT_SENTENCE_LENGTH:
                        i -= 1  # 현재 문장을 다시 처리하기 위해 인덱스 조정
                        continue
            
            # 3. 일반 문장 처리
            processed_sentences.append(current_sentence)
            i += 1
            
        return processed_sentences

    def split_sentences(self, text):
        """텍스트를 문장 단위로 분리하고 처리"""
        sentences = sent_tokenize(text)
        return self.process_sentences(sentences)

    def process_file(self, input_file):
        """파일을 읽어서 문장 단위로 분리"""
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        return self.split_sentences(text)

def main():
    splitter = SentenceSplitter()
    
    # assets 폴더 생성
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../assets')
    os.makedirs(assets_dir, exist_ok=True)
    
    txt_files = [f for f in os.listdir(assets_dir) if f.endswith('.txt')]
    
    if not txt_files:
        print("assets 폴더에 txt 파일이 없습니다.")
        print(f"assets 폴더 경로: {assets_dir}")
        print("txt 파일을 assets 폴더에 넣어주세요.")
        return
    
    print("\n사용 가능한 파일 목록:")
    for i, file in enumerate(txt_files, 1):
        print(f"{i}. {file}")
    
    # 파일 선택
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
    
    # 문장 분리
    sentences = splitter.process_file(file_path)
    
    print(f"\n총 {len(sentences)}개의 문장이 분리되었습니다.")
    
    while True:
        print("\n1. 특정 문장 보기")
        print("2. 전체 문장 보기")
        print("3. 종료")
        
        choice = input("\n선택하세요 (1-3): ")
        
        if choice == '1':
            while True:
                try:
                    sentence_num = int(input(f"보고 싶은 문장 번호를 입력하세요 (1-{len(sentences)}): "))
                    if 1 <= sentence_num <= len(sentences):
                        print(f"\n문장 {sentence_num}:")
                        print(sentences[sentence_num-1])
                        break
                    print("잘못된 번호입니다. 다시 입력해주세요.")
                except ValueError:
                    print("숫자를 입력해주세요.")
        
        elif choice == '2':
            print("\n=== 전체 문장 ===")
            for i, sentence in enumerate(sentences, 1):
                print(f"\n문장 {i}:")
                print(sentence)
        
        elif choice == '3':
            print("프로그램을 종료합니다.")
            break
        
        else:
            print("잘못된 선택입니다. 다시 선택해주세요.")

if __name__ == "__main__":
    main() 