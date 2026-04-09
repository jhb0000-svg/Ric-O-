import os

record_dir = "sample_records"
os.makedirs(record_dir, exist_ok=True)

docs = [
    {
        "id": "JEON-001",
        "agent": "전형배",
        "dept": "의료정책과",
        "org": "보건복지부",
        "activity": "의료민영화 정책 영향 평가",
        "law": "의료법",
        "year": "2008",
        "type": "보건정책"
    },
    {
        "id": "JEON-002",
        "agent": "전형배",
        "dept": "건강보험팀",
        "org": "보건복지부",
        "activity": "국민건강보험 시스템 개편 실무",
        "law": "국민건강보험법",
        "year": "2008",
        "type": "보건정책"
    },
    {
        "id": "JEON-003",
        "agent": "전형배",
        "dept": "수자원정책국",
        "org": "국토교통부",
        "activity": "4대강 살리기 사업 후속 조치 검토",
        "law": "하천법",
        "year": "2011",
        "type": "국토부특파"
    },
    {
        "id": "JEON-004",
        "agent": "전형배",
        "dept": "공공기관이전추진단",
        "org": "국토교통부",
        "activity": "지방 혁신도시 건설 추진 현황 모니터링",
        "law": "국토기본법",
        "year": "2012",
        "type": "국토부특파"
    }
]

for d in docs:
    content = f"""결재문서번호: {d['id']}
작성자: {d['agent']} ({d['dept']})
소속 기관(Organization): '{d['org']}'
수신처: 장관실
제목: {d['activity']} 관련 대외비 보고서
내용:
이 문서는 {d['year']}년 당시 {d['agent']} 주무관이 {d['org']} 재직 시절 작성한 {d['type']} 기획의 일환입니다. 전출 전후의 히스토리를 파악하는 핵심 자료입니다.

진행 업무(Activity): '{d['activity']}'
관련 법령(Mandate): '{d['law']}'
생산년도(Date): '{d['year']}'
"""
    with open(os.path.join(record_dir, f"document_{d['id']}.txt"), "w", encoding="utf-8") as f:
        f.write(content)

print("전형배 담당자의 특수 시나리오 기록물 4건이 생성되었습니다.")
