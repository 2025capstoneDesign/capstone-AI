# 음성 텍스트 전처리 도구

이 도구는 강의 음성 텍스트를 전처리하여 더 나은 품질의 데이터를 생성하는 데 사용됩니다.

## 기능

- assets 폴더 내의 txt 파일을 불러와서 선택적으로 처리
- 문장 분리 및 병합
- AI를 통한 문장 정제
- 처리된 결과 저장

## 실행 방법

1. 프로젝트 루트 디렉토리의 `assets` 폴더에 처리할 강의 교안 텍스트 파일(.txt)을 추가합니다.
2. `text-preprocessing` 폴더로 이동하여 `main.py`를 실행합니다:
   ```bash
   cd text-preprocessing
   python main.py
   ```
3. 메뉴에서 처리할 파일을 선택하고 원하는 작업을 수행합니다.

## 설정

### Config 변수 설명

```python
# 파일 경로 설정
ASSETS_DIR = "assets"  # 원본 텍스트 파일이 있는 디렉토리
DATA_DIR = "text-preprocessing/data"  # 처리된 결과가 저장되는 디렉토리

# 문장 길이 설정
MIN_SENTENCE_LENGTH = 5  # 5자 미만의 문장은 삭제
MAX_SENTENCE_LENGTH = 600  # 문장 병합 시 최대 길이

# OpenAI API 설정
OPENAI_MODEL = "gpt-3.5-turbo"  # 사용할 OpenAI 모델
OPENAI_TEMPERATURE = 0.3  # AI 응답의 창의성 정도
OPENAI_MAX_TOKENS = 500  # AI 응답의 최대 토큰 수

# 토큰 비용 설정 (1M 토큰당)
TOKEN_COSTS = {
    "gpt-3.5-turbo": {
        "input": 0.50,
        "output": 1.50
    }
}

# 환율 설정
EXCHANGE_RATE = 1468.30  # USD to KRW
```

### .env 파일 구성

프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 다음 내용을 추가하세요:

```
OPENAI_API_KEY=your_api_key_here
```

## 데이터 저장

처리된 데이터는 `text-preprocessing/data` 디렉토리에 저장됩니다.
파일명 형식: `{원본파일명}_{날짜}_{시간}.txt`
예시: `lecture_20240315_143022.txt`

## 성능 및 권장사항

- 문장 개수는 API 비용에 직접적인 영향을 미칩니다. 따라서 전처리 후 문장 개수가 50개 이하로 유지하는 것을 권장합니다.
- 현재 `main.py`의 설정은 테스트 결과 가장 적절한 것으로 확인하였습니다. (MAX_SENTENCE_LENGTH = 600)

## 테스트

### 단일 문장 테스트

`test_preprocessing.py`를 사용하여 개별 문장에 대한 전처리를 테스트할 수 있습니다.

### 다중 문장 테스트

`testData`를 사용하여 여러 문장에 대한 테스트가 가능합니다.
이 테스트는 실제 문방 분리 작업을 수행하지 않으며, AI 전처리 작업만 수행합니다.
