import os
import random

agents = ["김철수", "이영희", "박지민", "최동훈", "정수진"]
activities = ["기록물 평가 폐기처분", "차세대 시스템 아키텍처 개선", "개인정보 보안 진단 평가", "2026 정기 감사 대응", "하반기 예산안 편성 사전조사"]
departments = ["기록관리부", "IT기획부", "정보보안팀", "감사실", "재무팀"]
laws = ["공공기록물 관리에 관한 법률", "개인정보 보호법", "정보통신망법", "정부조직법", "회계관계직원 등의 책임에 관한 법률"]
years = ["2023", "2024", "2025", "2026"]
orgs = ["행정안전부", "국가기록원", "과학기술정보통신부", "방송통신위원회", "기획재정부"]

record_dir = "sample_records"
os.makedirs(record_dir, exist_ok=True)

for i in range(1, 31):
    idx = str(i).zfill(3)
    doc_id = f"2026-X-{idx}"
    agent = random.choice(agents)
    activity = random.choice(activities)
    dept = random.choice(departments)
    law = random.choice(laws)
    year = random.choice(years)
    org = random.choice(orgs)
    
    content = f"""결재문서번호: {doc_id}
작성자: {agent} ({dept})
소속 기관(Organization): '{org}'
수신처: 부서 전체
제목: {activity} 관련 세부 진행 보고서 {idx}
내용:
이 문서는 {activity} 업무 수행 과정에서 발생한 제반 사항을 기록한 보고서입니다.
위 업무는 철저한 대외비 및 공개 원칙을 따르며, 주요 데이터베이스 적재 과정을 수반합니다.
진행 업무(Activity): '{activity}'.
관련 법령(Mandate): '{law}'.
생산년도(Date): '{year}'.
담당 관리자는 {agent}입니다.
문서 고유 코드는 {doc_id}입니다.
"""
    with open(os.path.join(record_dir, f"document_{idx}.txt"), "w", encoding="utf-8") as f:
        f.write(content)

print("Generated exactly 30 enriched sample documents.")
