import nltk
from nltk.tokenize import sent_tokenize
import os

class SentenceSplitter:
    def split_sentences(self, text):
        """텍스트를 문장 단위로 분리"""
        return sent_tokenize(text)

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