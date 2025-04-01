import re
import torch
import numpy as np
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity

# 강의 녹음본 텍스트와 PPT 텍스트를 문장 단위로 분리
def preprocess_text(text):
    text = re.sub(r'[^A-Za-z0-9.,;?!\s]', '', text)
    sentences = text.split('.')  # 문장 단위로 분리
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences

# 파일에서 텍스트 읽기
def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()  # 파일 내용 전체 읽기
    return text

# 파일 경로 설정
lecture_file_path = './assets/lecture_text.txt'  # 강의 녹음본 텍스트 파일 경로
ppt_file_path = './assets/ppt_text.txt'  # PPT 텍스트 파일 경로

# 파일에서 텍스트 읽기
lecture_text =  read_text_from_file(lecture_file_path)
ppt_text =  read_text_from_file(ppt_file_path)

# 녹음본과 PPT 텍스트 전처리
lecture_sentences = preprocess_text(lecture_text)
ppt_sentences = preprocess_text(ppt_text)

# BERT 모델 및 토크나이저 로딩
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# BERT 모델을 사용하여 텍스트를 임베딩으로 변환
def get_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    # [CLS] 토큰 벡터를 반환 (문장 임베딩)
    return outputs.last_hidden_state[:, 0, :].numpy()  # (1, hidden_size)

# 강의 녹음본과 PPT 슬라이드 임베딩
lecture_embeddings = np.array([get_embedding(sentence) for sentence in lecture_sentences])
ppt_embeddings = np.array([get_embedding(sentence) for sentence in ppt_sentences])

# 유사도 계산 (2D 배열로 변환 후 처리)
def calculate_similarity(lecture_embeddings, ppt_embeddings):
    similarities = []
    # 2D 배열로 유사도 계산
    for lec_emb in lecture_embeddings:
        similarity = cosine_similarity(lec_emb.reshape(1, -1), ppt_embeddings.reshape(len(ppt_embeddings), -1))
        similarities.append(similarity)
    return similarities

# 강의 녹음본과 PPT 간의 유사도 계산
similarity_scores = calculate_similarity(lecture_embeddings, ppt_embeddings)

# 슬라이드 구간 매핑
def map_to_slide(similarity_scores, threshold=0.8):
    slide_mapping = []
    slide_idx = 0
    for i, scores in enumerate(similarity_scores):
        # 가장 높은 유사도 값 인덱스를 선택하고 threshold로 구분
        max_similarity = np.max(scores)
        if max_similarity < threshold:  # 유사도가 threshold 이하일 경우 새 슬라이드
            slide_idx += 1
        slide_mapping.append(slide_idx)
    return slide_mapping

# 슬라이드 매핑 결과
slide_mapping = map_to_slide(similarity_scores)
print("Slide Mapping: ", slide_mapping)

# 슬라이드별 텍스트 배치
def group_sentences_by_slide(lecture_sentences, slide_mapping):
    slide_texts = {}
    for idx, slide in enumerate(slide_mapping):
        if slide not in slide_texts:
            slide_texts[slide] = []
        slide_texts[slide].append(lecture_sentences[idx])
    return slide_texts

# 슬라이드 별 텍스트 배치
slide_texts = group_sentences_by_slide(lecture_sentences, slide_mapping)
for slide, text in slide_texts.items():
    print(f"Slide {slide+1}:")
    print(" ".join(text))
    print("\n")
