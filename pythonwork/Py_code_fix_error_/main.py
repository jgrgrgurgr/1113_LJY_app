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
    <html>
        <head>
            <title>경찰청 졸음운전 교통사고 현황</title>
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; }}
                table {{ margin: 0 auto; border-collapse: collapse; width: 80%; }}
                th, td {{ padding: 10px; border: 1px solid #ddd; text-align: center; }}
                th {{ background-color: #f4f4f4; }}
            </style>
        </head>
        <body>
            <h1>경찰청 졸음운전 교통사고 현황</h1>
            {table_html}
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)