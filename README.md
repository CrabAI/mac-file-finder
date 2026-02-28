# mac-file-finder

macOS Spotlight 기반 로컬 파일 검색 CLI 도구. 자연어 질의로 파일을 찾고, Finder에서 위치를 열거나 기본 앱으로 바로 실행할 수 있습니다.

## Features

- **자연어 검색:** `mdfind`를 사용해 파일명·내용·메타데이터를 동시에 검색
- **범위 제한 검색:** `-onlyin` 옵션으로 특정 디렉토리만 탐색해 속도·정확도 향상
- **메타데이터 표시:** 파일명 / 종류(Kind) / 최종 수정일 출력
- **인터랙티브 액션:**
  - `[r]` Finder에서 파일 위치 표시 (선택 상태로 열림)
  - `[o]` 기본 앱으로 파일 바로 열기

## Requirements

- macOS (Spotlight 사용 필수)
- Python 3.9+

## Installation

### 1. 저장소 클론

```bash
git clone https://github.com/crabai/mac-file-finder.git
cd mac-file-finder
```

### 2. 가상환경 생성 (선택)

```bash
python -m venv venv
source venv/bin/activate
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. 설정 파일 생성

```bash
cp config.example.py config.py
```

`config.py`를 열어 본인의 검색 경로를 지정합니다:

```python
# config.py
SEARCH_ROOTS = [
    "~/Documents",
    "~/Desktop",
    # "~/Downloads",  # 필요 시 추가
]

TOP_N = 10  # 최대 결과 수
```

> **주의:** `config.py`는 개인 경로가 포함되므로 `.gitignore`에 의해 커밋에서 제외됩니다.

## Usage

```bash
python run.py
```

### 실행 예시

```
macOS 로컬 파일 찾기 에이전트 (Spotlight 기반)
검색 범위: ~/Documents, ~/Desktop

찾고 싶은 파일을 자연어로 입력하세요 (종료: q): 여름 휴가 사진

📁 후보 파일:
1. 여름휴가2024.jpg | JPEG image | 2024-08-15 14:32:00 +0000
   /Users/yourname/Desktop/여름휴가2024.jpg
2. vacation_summary.pdf | PDF Document | 2024-08-20 09:10:00 +0000
   /Users/yourname/Documents/vacation_summary.pdf

정밀 파일 검색이 완료되었습니다.

동작 선택: [r] Finder에서 위치 표시 / [o] 파일 열기 / [Enter] 건너뜀: r
번호 입력 (1~2): 1
```

### 검색 팁

| 상황 | 입력 예시 |
|------|-----------|
| 파일명 키워드 | `휴가 보고서` |
| 파일 형식 | `invoice pdf` |
| 내용 키워드 | `API key configuration` |
| 날짜 범위 | `2024 계약서` |

> 문장이 길면 핵심 키워드만 입력하는 것이 더 정확합니다.

## Project Structure

```
mac-file-finder/
├── run.py              # 메인 실행 파일 (검색 루프 + 액션)
├── config.example.py   # 설정 템플릿 (커밋 포함)
├── config.py           # 실제 설정 파일 (커밋 제외 - .gitignore)
├── requirements.txt    # Python 의존성
└── README.md
```

## Configuration

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `SEARCH_ROOTS` | `["~/Documents", "~/Desktop"]` | Spotlight 검색 대상 디렉토리 목록 |
| `TOP_N` | `10` | 검색 결과 최대 출력 개수 |

## How It Works

```
사용자 입력 (자연어)
       │
       ▼
  mdfind -onlyin <root> <query>     ← macOS Spotlight 인덱스 검색
       │
       ▼
  결과 중복 제거 + 상위 TOP_N 선택
       │
       ▼
  mdls -name kMDItemDisplayName
       -name kMDItemKind
       -name kMDItemFSContentChangeDate   ← 메타데이터 조회
       │
       ▼
  결과 출력 → 사용자 액션 선택
       │
  ┌────┴────┐
  │ [r]     │ [o]
  ▼         ▼
open -R   open
(Finder)  (기본 앱)
```

## Troubleshooting

### 검색 결과가 없을 때

- Spotlight 인덱싱이 완료됐는지 확인: **시스템 설정 → Siri 및 Spotlight**
- `SEARCH_ROOTS` 경로가 올바른지 확인
- 더 짧은 키워드로 재시도

### `mdfind` 명령어를 찾을 수 없을 때

- macOS 전용 도구입니다. Linux/Windows에서는 동작하지 않습니다.

### `config.py` 파일이 없다는 오류

```bash
cp config.example.py config.py
```

## License

MIT
