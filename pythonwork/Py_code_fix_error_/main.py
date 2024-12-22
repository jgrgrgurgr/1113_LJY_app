import pandas as pd
import chardet
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# CSV 파일 경로
file_path = '/Users/harold0812/Desktop/1113 이주영 프그 수행/pythonwork/경찰청_졸음운전 교통사고 현황_20221231.csv'

# 파일의 인코딩 감지
with open(file_path, 'rb') as f:
    result = chardet.detect(f.read())
    encoding = result['encoding']

def process_csv_to_html(file_path):
    # CSV 파일 읽기
    df = pd.read_csv(file_path, encoding=encoding)

    # 데이터 가공 (예: 필요한 열만 선택)
    df.fillna(0, inplace=True)  # 결측치를 0으로 대체

    # HTML 테이블 생성
    html_table = df.to_html(index=False, escape=False, justify="center", border=1)

    return html_table

@app.get("/", response_class=HTMLResponse)
async def show_weather():
    # CSV 파일을 가공하여 HTML로 변환
    table_html = process_csv_to_html(file_path)

    # HTML 페이지 생성
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8"> <!-- 문자 인코딩 설정 -->
        <meta name="viewport" content="width=device-width, initial-scale=1.0"> <!-- 반응형 웹 디자인 설정 -->
        <title>졸음운전 방지</title> <!-- 페이지 제목 -->
        <style>
            body {{
                background-color: #f2f2f2; /* 부드러운 배경 색상 */
                font-family: 'Arial', sans-serif; /* 기본 폰트 설정 */
                margin: 0; /* 기본 여백 제거 */
                padding: 20px; /* 패딩 추가 */
            }}
            header {{
                text-align: center; /* 중앙 정렬 */
                margin-bottom: 20px; /* 아래 여백 설정 */
            }}
            h1 {{
                font-size: 2.5em; /* 제목 크기 설정 */
                color: #4a4a4a; /* 제목 색상 */
                text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3); /* 텍스트 그림자 효과 */
            }}
            .tip-card {{
                background: white; /* 카드 배경 색상 */
                border-radius: 15px; /* 둥근 모서리 */
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2); /* 카드 그림자 */
                padding: 20px; /* 패딩 추가 */
                margin: 10px auto; /* 중앙 정렬을 위한 마진 */
                width: 90%; /* 카드 너비 설정 */
                max-width: 600px; /* 카드 최대 너비 설정 */
            }}
            h2 {{
                color: #333; /* 부제목 색상 */
            }}
            ul {{
                list-style-position: inside; /* 리스트 아이템 내부 정렬 */
            }}
            button {{
                background: linear-gradient(135deg, #6dd5ed, #2193b0); /* 그라데이션 버튼 배경 */
                border: none; /* 테두리 제거 */
                border-radius: 25px; /* 둥근 모서리 */
                color: white; /* 글자 색상 */
                padding: 15px 30px; /* 패딩 추가 */
                font-size: 1.2em; /* 폰트 크기 설정 */
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3); /* 버튼 그림자 */
                cursor: pointer; /* 마우스 커서 포인터로 변경 */
            }}
            footer {{
                text-align: center; /* 중앙 정렬 */
                margin-top: 20px; /* 위 여백 설정 */
                font-size: 0.8em; /* 글자 크기 설정 */
            }}
            a {{
                color: #2193b0; /* 링크 색상 설정 */
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>졸음운전, 조심하세요!</h1> <!-- 주요 제목 -->
            <p>졸음운전 예방의 중요성에 대해 알아보세요.</p> <!-- 설명 -->
        </header>

        <main>
            <div class="tip-card">
                <h2>졸음운전 방지를 위한 팁</h2>
                <ul>
                    <li>정기적으로 휴식을 취하세요.</li>
                    <li>커피나 카페인 음료를 드세요.</li>
                    <li>늦은 시간에 운전하지 마세요.</li>
                </ul>
            </div>

            <div class="tip-card">
                <h2>졸음 체크하기</h2>
                <button onclick="alert('경고: 졸음이 느껴지면 즉시 정차하세요!')">알림 상태 확인</button> <!-- 행동 버튼 -->
            </div>

            <div class="tip-card">
                <h2>자원 링크</h2>
                <p><a href="https://www.nhtsa.gov/" target="_blank">국립 교통 안전국</a></p>
            </div>
        </main>

        <footer>
            <p>&copy; 2023 졸음운전 방지 웹 사이트</p> <!-- 저작권 정보 -->
            <a href="#top">맨 위로 가기</a> <!-- 위로 이동 링크 -->
        </footer>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)