import os
import random
import shutil

record_dir = "sample_records"
if os.path.exists(record_dir):
    shutil.rmtree(record_dir)
os.makedirs(record_dir, exist_ok=True)

# 공통 연결 허브 기관 (모든 시대/유형을 관통하여 그래프를 이어주는 역할)
common_orgs = ["행정안전부", "기획재정부", "보건복지부", "외교부", "국토교통부"]

# Type A: 1988 Olympics (50 records)
a_agents = ["김조직", "이체육", "박행사", "최외교", "정안전"]
a_orgs = ["서울올림픽조직위원회", "체육부"] + common_orgs
a_activities = ["경기장 건설 관리", "자원봉사자 모집", "선수단 보안/경호", "개막식/폐막식 기획", "외신 기자단 지원"]
a_laws = ["올림픽대회지원법", "올림픽시설물 설치 특별법", "국제경기대회 체육진흥기금법"]
a_years = ["1986", "1987", "1988"]

# Type B: NCIS Construction (100 records)
b_agents = ["전산국장", "홍비트", "박서버", "김보안", "이네트워크"]
b_orgs = [f"참여부처_{i}호" for i in range(1, 15)] + common_orgs  # 14 mock + 5 common
b_activities = ["통합이전 마스터플랜 수립", "물리적 서버 이전", "공동망 네트워크 구축", "통합보안관제 체계 수립", "소프트웨어 라이선스 통합"]
b_laws = ["전자정부법", "정보통신기반 보호법", "공공기관 정보자원 통합기준"]
b_years = ["2005", "2006", "2007", "2008"]

# Type C: COVID-19 Response (100 records)
c_agents = ["정은경", "역학조사관A", "백신담당팀장", "임상지원담당관", "마스크수급관"]
c_orgs = ["질병관리청", "식품의약품안전처", "전국지방자치단체연합"] + common_orgs
c_activities = ["마스크 수급 5부제 기획", "백신 콜드체인 유통망 확충", "확진자 동선 역학조사", "해외입국자 자가격리 관리", "의료기관 손실보상금 지급"]
c_laws = ["감염병의 예방 및 관리에 관한 법률", "재난 및 안전관리 기본법", "검역법"]
c_years = ["2020", "2021", "2022", "2023"]

def gen_doc(idx, type_prefix, agents, activities, orgs, laws, years):
    doc_id = f"{type_prefix}-{idx:03d}"
    agent = random.choice(agents)
    activity = random.choice(activities)
    org = random.choice(orgs)
    law = random.choice(laws)
    year = random.choice(years)
    
    content = f"""결재문서번호: {doc_id}
작성자: {agent} (기록관리부)
소속 기관(Organization): '{org}'
수신처: 부서 전체
제목: {activity} 관련 전략 이행 결과보고서
내용:
이 문서는 {type_prefix} 프로젝트 중 {activity}에 대한 세부 절차와 진행 결과를 요약한 핵심 기록물입니다.

진행 업무(Activity): '{activity}'
관련 법령(Mandate): '{law}'
생산년도(Date): '{year}'
"""
    with open(os.path.join(record_dir, f"document_{doc_id}.txt"), "w", encoding="utf-8") as f:
        f.write(content)

counter = 1
for i in range(50):
    gen_doc(counter, "OLYMPIC", a_agents, a_activities, a_orgs, a_laws, a_years)
    counter += 1

for i in range(100):
    gen_doc(counter, "NCIS", b_agents, b_activities, b_orgs, b_laws, b_years)
    counter += 1

for i in range(100):
    gen_doc(counter, "COVID19", c_agents, c_activities, c_orgs, c_laws, c_years)
    counter += 1

print(f"Generated {counter-1} complex virtual documents.")
