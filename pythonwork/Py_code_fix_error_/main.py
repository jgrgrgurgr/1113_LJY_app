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

    # '연도' 열이 있는지 확인하고 필터링
    if '연도' in df.columns:
        df = df[(df['연도'] == 2017) | (df['연도'] == 2022)]
    else:
        return "연도 열이 존재하지 않습니다."

    # 도로 종류별로 그룹화하여 합계 계산
    grouped_df = df.groupby(['도로종류', '연도']).sum().reset_index()

    # 연도 기준으로 오름차순 정렬
    grouped_df.sort_values(by=['도로종류', '연도'], ascending=True, inplace=True)

    # 도로종류별로 2개씩 묶기
    grouped_df['도로종류'] = grouped_df['도로종류'].astype(str)

    # 새로운 데이터프레임 생성
    combined_rows = []
    for road_type in grouped_df['도로종류'].unique():
        road_data = grouped_df[grouped_df['도로종류'] == road_type]
        if len(road_data) == 2:
            combined_rows.append(road_data)

    combined_df = pd.concat(combined_rows).reset_index(drop=True)

    # HTML 테이블 생성
    html_table = combined_df.to_html(index=False, escape=False, justify="center", border=0)

    styled_html_table = f"""
    <style>
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 15px;
            text-align: center;
            border: 1px solid #ddd;
        }}
        th {{
            background-color: #2193b0;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        tr:hover {{
            background-color: #f1f1f1;
        }}
    </style>
    {html_table}
    """
    
    return styled_html_table

@app.get("/", response_class=HTMLResponse)
async def drowsy_driving():
    # CSV 파일을 가공하여 HTML로 변환
    table_html = process_csv_to_html(file_path)

    # HTML 페이지 생성
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>졸음운전 예방 캠페인 by 1113 이주영</title>
        <style>
            body {{
                background-color: #f2f2f2;
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 20px;
                overflow-y: auto;
                height: 100vh;
            }}
            header {{
                text-align: center;
                margin-bottom: 20px;
            }}
            h1 {{
                font-size: 2.5em;
                color: #4a4a4a;
                text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
            }}
            .tip-card {{
                background: white;
                border-radius: 5px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
                padding: 20px;
                margin: 10px auto;
                width: 80%;
            }}
            h2 {{
                color: #333; 
            }}
            ul {{
                list-style-position: inside;
            }}
            button {{
                background: linear-gradient(135deg, #6dd5ed, #2193b0);
                border: none; 
                border-radius: 0;
                color: white;
                padding: 15px 30px;
                font-size: 1.2em;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3); 
                cursor: pointer;
                width: 100%;
            }}
            footer {{
                text-align: center;
                margin-top: 20px;
                font-size: 0.8em;
            }}
            a {{
                color: #2193b0;
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>졸음운전, 이렇게 알고 예방하자.</h1>
            <p>졸음운전이 왜 위험한지, 그리고 어떻게 하면 대처할 수 있는지에 대해 알아봅시다.</p>
        </header>

        <main>
            <div class="tip-card">
                <h2>졸음운전의 정의.</h2>
                    <p>도로교통법 제45조에 따르면, (과로한 때 등의 운전 금지) 자동차등의 운전자는 제44조에 따른 술에 취한 상태 외에 과로, 질병 또는 약물(마약, 대마 및 향정신성의약품과 그 밖에 행정자치부령으로 정하는 것이라 합니다.</p>
                <h3>졸음운전 관련 매체.</h3>
                    <p><a href="https://www.korea.kr/multi/visualNewsView.do?newsId=148846669" target="_blank">졸음운전 예방법</a></p>
                    <p><a href="https://www.youtube.com/watch?v=SVfls3GBPhY" target="_blank">졸음운전의 위험성(동영상)</a></p>
            </div>

            <div class="tip-card">
                <h2>졸음운전 교통사고 현황.</h2>
                    {table_html}
            </div>

            <div class="tip-card">
                <h2>졸음운전을 예방하는 법.</h2>
                <button onclick="alert('충분한 수면과 휴식을 취하거나, 동승자와의 대화, 창문 개방과 같은 방법으로 예방할 수 있다.')">정답 공개</button>
            </div>

            <div class="tip-card">
                <h2>관련 자료 참조</h2>
                <p><a href="https://www.police.go.kr/index.do" target="_blank">경찰청</a></p>
            </div>
        </main>

        <footer>
            <a href="#top">맨 위로 가기</a>
        </footer>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)