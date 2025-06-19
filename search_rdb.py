# import os
# import re
# from collections import Counter, defaultdict
# from typing import List, Tuple
# from dotenv import load_dotenv
# import openai

# # 환경변수 로드
# load_dotenv()

# # LLM 초기화
# api_key = os.getenv("OPENAI_API_KEY")
# MODEL_NAME = os.getenv("MODEL_NAME")
# TEMPERATURE = float(os.getenv("TEMPERATURE"))

# client = openai.OpenAI(api_key=api_key)

# # 데이터베이스 스키마 및 메타데이터
# SCHEMA = """
# CREATE TABLE `project` (
#   `ID` text DEFAULT NULL,
#   `StartYear` double DEFAULT NULL,
#   `EndYear` double DEFAULT NULL,
#   `Project` text DEFAULT NULL,
#   `ProjectScale` double DEFAULT NULL,
#   `Roles` text DEFAULT NULL,
#   `SkillSet1` text DEFAULT NULL,
#   `SkillSet2` text DEFAULT NULL,
#   `SkillSet3` text DEFAULT NULL,
#   `SkillSet4` text DEFAULT NULL,
#   `Industry` text DEFAULT NULL,
#   `CareerImpact` double DEFAULT NULL
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
# """

# ROLES = """
# Mainframe, System, Administrator, Application, Arch., Architect, Back-End, CICD, Cloud, Cost, DB2, DBA,
# Dev., Eng., Engineer, Engineering, Front-End, MPA, Mgmt, Middleware, Monitoring, NW, Net., Networking,
# Operation, Ops, PL, PM, PMO, Process, QA, SM, SaaS, Security, Server, Service, Solution,
# TA, Tech., Technical, Web, architect, controller, 교육, 마스터, 모듈개발, 운영, 인터페이스
# """

# SKILLSETS = """
# Front-end Dev, Back-end Dev, Mobile Dev, Factory 기획/설계, 자동화 Eng, 지능화 Eng,
# ERP_FCM, ERP_SCM, ERP_HCM, ERP_T&E, Biz. Solution, System/Network Eng,
# Middleware/Database Eng, Data Center Eng, Cyber Security,
# Application Architect, Data Architect, Technical Architect,
# Infra PM, Application PM, Solution PM, PMO, Quality Eng, Offshoring Service Professional,
# AI/Data Dev, Generative AI Dev, Generative AI Model Dev,
# Sales, Domain Expert, ESG/SHE, ERP, SCM, CRM, AIX,
# Strategy Planning, New Biz. Dev, Financial Mgmt, Human Resource Mgmt,
# Stakeholder Mgmt, Governance & Public Mgmt,
# Infra PM -- 대형PM, Application PM -- 대형PM, Solution PM -- 대형PM
# """

# INDUSTRIES = """
# 물류, 제2금융, 제조, 공공, 미디어, 통신, 금융, 공통, Global, 
# 대외, 제1금융, 은행, 의료, 유통, 보험, SK그룹, 유통/서비스, 유통/물류/서비스
# """

# def expand_questions(user_question: str) -> List[str]:
#     """사용자 질문을 3개의 확장 질문으로 변환"""
#     prompt = f"""
#     당신은 데이터베이스 및 업무 도메인 전문가입니다.
#     아래 사용자 질문과 관련된 다양한 데이터를 찾을 수 있는 3개의 확장 질문을 만들어주세요.

#     중요한 규칙:
#     1. 원본 질문의 핵심 키워드를 포함하되, 다양한 각도에서 데이터를 조회할 수 있도록 확장
#     2. 데이터베이스 필터링 가능한 조건만 사용 (Roles, SkillSet1-4, Project, ProjectScale, Industry, CareerImpact, StartYear, EndYear 등)
#     3. 추상적이거나 감정적인 내용은 절대 포함하지 말 것

#     질문: "{user_question}"

#     아래 형식으로만 응답하세요:
#     - 질문 1
#     - 질문 2  
#     - 질문 3
#     """
    
#     intent_response = client.chat.completions.create(
#         model=MODEL_NAME,
#         messages=[
#             {"role": "system", "content": "당신은 자연어 이해 및 질문 확장 전문가입니다."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=TEMPERATURE
#     )

#     expanded_text = intent_response.choices[0].message.content.strip()
#     questions = [
#         line.lstrip("- ").strip()
#         for line in expanded_text.splitlines()
#         if line.startswith("- ")
#     ]
#     return questions

# def generate_sql_queries(questions: List[str]) -> List[str]:
#     """확장된 질문들을 SQL 쿼리로 변환"""
#     questions_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])
    
#     # prompt = f"""
#     # 아래는 데이터베이스 스키마입니다:
#     # {SCHEMA}

#     # Roles 목록: {ROLES}
#     # Skill Set 목록: {SKILLSETS}
#     # Industry 목록: {INDUSTRIES}

#     # 다음 질문들에 각각 적합한 SQL 쿼리를 작성해 주세요.
    
#     # SQL 작성 가이드라인:
#     # 1. 항상 'ID' 컬럼을 포함하여 조회
#     # 2. OR 조건을 적극 활용하여 많은 관련 데이터 수집
#     # 3. 목록에 있는 값 위주로 사용
    
#     # 각 질문에 대해 다음 형식으로 응답:
#     # 질문 1에 대한 SQL:
#     # ```sql
#     # [SQL 쿼리]
#     # ```
    
#     # 질문들:
#     # {questions_text}
#     # """
#     prompt = f"""
#         아래는 데이터베이스 스키마입니다:
#         {SCHEMA}

#         Roles 목록: {ROLES}
#         Skill Set 목록: {SKILLSETS}
#         Industry 목록: {INDUSTRIES}

#         위 내용을 참고하여, 아래 질문들에 적합한 SQL 쿼리를 작성해 주세요.
#         항상 'ID' 컬럼을 포함하여 조회하는 쿼리를 작성해 주세요.
#         반듯시 OR 조건을 적극 활용하여 많은 관련 데이터 수집해주세요

#         질문들:
#         {questions_text}
#         """
    
#     sql_response = client.chat.completions.create(
#         model=MODEL_NAME,
#         messages=[
#             {"role": "system", "content": "당신은 SQL 전문가입니다."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=TEMPERATURE
#     )

#     response_text = sql_response.choices[0].message.content.strip()
    
#     # SQL 블록 추출
#     sql_blocks = re.findall(r'```sql\s*(.*?)\s*```', response_text, re.DOTALL)
#     sql_queries = []
    
#     for sql_block in sql_blocks:
#         cleaned_sql = ' '.join(sql_block.strip().split())
#         sql_queries.append(cleaned_sql)
    
#     return sql_queries

# def execute_sql_queries(sql_queries: List[str], execute_sql_func) -> List[str]:
#     """SQL 쿼리들을 실행하고 ID들을 수집"""
#     all_ids = []
    
#     for i, sql in enumerate(sql_queries, 1):
#         try:
#             result = execute_sql_func(sql)
#             if isinstance(result, tuple):
#                 columns, rows = result
                
#                 # ID 컬럼 찾기
#                 try:
#                     id_index = list(columns).index('ID')
#                     ids = [row[id_index] for row in rows if row[id_index] is not None]
#                     all_ids.extend(ids)
#                 except ValueError:
#                     print("❌ 'ID' 컬럼이 결과에 없습니다.")
#             else:
#                 print(f"✅ Affected rows: {result}")
#         except Exception as e:
#             print(f"❌ Error executing SQL {i}: {e}")
    
#     return all_ids

# def get_top_career_profiles(all_ids: List[str], execute_sql_func, top_n: int = 3):
#     """상위 N개 ID 프로필 조회 - 간단한 ChromaDB 스타일 출력"""
#     counter = Counter(all_ids)
#     most_common_ids = counter.most_common(top_n)
    
#     if not most_common_ids:
#         return {}
    
#     # 상위 ID들 조회
#     top_ids = [id_val for id_val, _ in most_common_ids]
#     in_clause = ", ".join(f"'{id_val}'" for id_val in top_ids)
#     query = f"SELECT * FROM project WHERE ID IN ({in_clause});"
    
#     result = execute_sql_func(query)
#     columns, rows = result
    
#     # ID별 그룹화
#     person_projects = defaultdict(list)
#     for row in rows:
#         row_dict = dict(zip(columns, row))
#         person_projects[row_dict['ID']].append(row_dict)
    
#     # 간단한 포맷팅
#     career_profiles = {}
#     for person_id, projects in person_projects.items():
#         profile = f"=== 선택된 사원 ===\n사번: {person_id}\n총 경력 수: {len(projects)}개\n\n경력 상세:\n"
        
#         for j, p in enumerate(projects, 1):
#             years = f"{int(p.get('StartYear', 0))}~{int(p.get('EndYear', 0))}년차"
#             skills = ', '.join([str(p.get(f'SkillSet{i}', '')) for i in range(1,5) if p.get(f'SkillSet{i}')])
            
#             profile += f"  경력 {j}: {years} - {p.get('Roles', '')}\n"
#             profile += f"    스킬셋: {skills}\n"
#             profile += f"    도메인: {p.get('Industry', '')}\n"
#             profile += f"    요약: {p.get('Project', '')}\n\n"
        
#         career_profiles[person_id] = profile
#         print(profile)
    
#     return career_profiles

# def analyze_career_question(user_question: str, execute_sql_func):
#     """전체 커리어 분석 프로세스 실행 - ChromaDB 형식 반환"""
#     print(f"사용자 질문: {user_question}\n")
    
#     # 1. 질문 확장
#     expanded_questions = expand_questions(user_question)
    
#     # 2. SQL 생성
#     sql_queries = generate_sql_queries(expanded_questions)
#     print(f"\n생성된 SQL 쿼리 {len(sql_queries)}개:")
#     for i, sql in enumerate(sql_queries, 1):
#         print(f"{i}. {sql}")
    
#     # 3. SQL 실행 및 ID 수집
#     all_ids = execute_sql_queries(sql_queries, execute_sql_func)
    
#     # 4. 상위 커리어 프로필 조회 및 반환 (ChromaDB 형식)
#     career_profiles = get_top_career_profiles(all_ids, execute_sql_func)
    
#     return career_profiles

# # 사용 예시
# if __name__ == "__main__":
#     # execute_sql 함수는 실제 데이터베이스 연결 함수로 교체 필요
#     def dummy_execute_sql(sql):
#         print(f"SQL 실행: {sql}")
#         return ("columns", [])  # 더미 응답
    
#     user_question = "반도체 설비관리 및 설비제어, SHE 통합시스템 구축 프로젝트에서 PL 및 PM 역할을 수행한 5년차 경력으로써, 비슷한 경력과 경험을 가진 다른 전문가들이 경력 발전을 위해 어떤 경로를 선택했는지 알려주세요."
#     analyze_career_question(user_question, dummy_execute_sql)
#     print(expand_questions(user_question))


import os
import re
import pymysql  # 추가된 부분
from collections import Counter, defaultdict
from typing import List, Tuple
from dotenv import load_dotenv
import openai

# 환경변수 로드
load_dotenv()

# LLM 초기화
api_key = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
TEMPERATURE = float(os.getenv("TEMPERATURE"))

client = openai.OpenAI(api_key=api_key)

# 실제 DB 연결 함수 
def execute_sql(sql):
    """MariaDB 연결해서 SQL 실행"""
    connection = pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"), 
        password=os.getenv("DB_PASSWORD", "1234"),
        database=os.getenv("DB_NAME", "nav7"),
        charset='utf8mb4'
    )
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            if sql.strip().upper().startswith('SELECT'):
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                return columns, rows
            else:
                connection.commit()
                return cursor.rowcount
    finally:
        connection.close()

# 데이터베이스 스키마 및 메타데이터
SCHEMA = """
CREATE TABLE `project` (
  `ID` text DEFAULT NULL,
  `StartYear` double DEFAULT NULL,
  `EndYear` double DEFAULT NULL,
  `Project` text DEFAULT NULL,
  `ProjectScale` double DEFAULT NULL,
  `Roles` text DEFAULT NULL,
  `SkillSet1` text DEFAULT NULL,
  `SkillSet2` text DEFAULT NULL,
  `SkillSet3` text DEFAULT NULL,
  `SkillSet4` text DEFAULT NULL,
  `Industry` text DEFAULT NULL,
  `CareerImpact` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

ROLES = """
Mainframe, System, Administrator, Application, Arch., Architect, Back-End, CICD, Cloud, Cost, DB2, DBA,
Dev., Eng., Engineer, Engineering, Front-End, MPA, Mgmt, Middleware, Monitoring, NW, Net., Networking,
Operation, Ops, PL, PM, PMO, Process, QA, SM, SaaS, Security, Server, Service, Solution,
TA, Tech., Technical, Web, architect, controller, 교육, 마스터, 모듈개발, 운영, 인터페이스
"""

SKILLSETS = """
Front-end Dev, Back-end Dev, Mobile Dev, Factory 기획/설계, 자동화 Eng, 지능화 Eng,
ERP_FCM, ERP_SCM, ERP_HCM, ERP_T&E, Biz. Solution, System/Network Eng,
Middleware/Database Eng, Data Center Eng, Cyber Security,
Application Architect, Data Architect, Technical Architect,
Infra PM, Application PM, Solution PM, PMO, Quality Eng, Offshoring Service Professional,
AI/Data Dev, Generative AI Dev, Generative AI Model Dev,
Sales, Domain Expert, ESG/SHE, ERP, SCM, CRM, AIX,
Strategy Planning, New Biz. Dev, Financial Mgmt, Human Resource Mgmt,
Stakeholder Mgmt, Governance & Public Mgmt,
Infra PM -- 대형PM, Application PM -- 대형PM, Solution PM -- 대형PM
"""

INDUSTRIES = """
물류, 제2금융, 제조, 공공, 미디어, 통신, 금융, 공통, Global, 
대외, 제1금융, 은행, 의료, 유통, 보험, SK그룹, 유통/서비스, 유통/물류/서비스
"""

def expand_questions(user_question: str) -> List[str]:
    """사용자 질문을 3개의 확장 질문으로 변환"""
    prompt = f"""
    당신은 데이터베이스 및 업무 도메인 전문가입니다.
    아래 사용자 질문과 관련된 다양한 데이터를 찾을 수 있는 3개의 확장 질문을 만들어주세요.

    중요한 규칙:
    1. 원본 질문의 핵심 키워드를 포함하되, 다양한 각도에서 데이터를 조회할 수 있도록 확장
    2. 데이터베이스 필터링 가능한 조건만 사용 (Roles, SkillSet1-4, Project, ProjectScale, Industry, CareerImpact, StartYear, EndYear 등)
    3. 추상적이거나 감정적인 내용은 절대 포함하지 말 것

    질문: "{user_question}"

    아래 형식으로만 응답하세요:
    - 질문 1
    - 질문 2  
    - 질문 3
    """
    
    intent_response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "당신은 자연어 이해 및 질문 확장 전문가입니다."},
            {"role": "user", "content": prompt}
        ],
        temperature=TEMPERATURE
    )

    expanded_text = intent_response.choices[0].message.content.strip()
    questions = [
        line.lstrip("- ").strip()
        for line in expanded_text.splitlines()
        if line.startswith("- ")
    ]
    print("확장된 질문: ", questions)
    return questions

def generate_sql_queries(questions: List[str]) -> List[str]:
    """확장된 질문들을 SQL 쿼리로 변환 - 개선된 프롬프트"""
    questions_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])
    
    prompt = f"""
    아래는 데이터베이스 스키마입니다:
    {SCHEMA}

    Roles 목록: {ROLES}
    Skill Set 목록: {SKILLSETS}
    Industry 목록: {INDUSTRIES}

    다음 질문들에 각각 적합한 SQL 쿼리를 작성해 주세요.
    
    SQL 작성 가이드라인:
    1. 항상 'ID' 컬럼을 포함하여 조회
    2. LIKE '%키워드%' 사용하여 부분 매칭
    3. OR 조건을 적극 활용하여 많은 관련 데이터 수집
    
    각 질문에 대해 다음 형식으로 응답:
    질문 1에 대한 SQL:
    ```sql
    SELECT ID * FROM project WHERE ...
    ```
    
    질문들:
    {questions_text}
    """
    
    sql_response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "당신은 SQL 전문가입니다."},
            {"role": "user", "content": prompt}
        ],
        temperature=TEMPERATURE
    )

    response_text = sql_response.choices[0].message.content.strip()
    
    # SQL 블록 추출
    sql_blocks = re.findall(r'```sql\s*(.*?)\s*```', response_text, re.DOTALL)
    sql_queries = []
    
    for sql_block in sql_blocks:
        cleaned_sql = ' '.join(sql_block.strip().split())
        sql_queries.append(cleaned_sql)
    
    return sql_queries

def execute_sql_queries(sql_queries: List[str], execute_sql_func) -> List[str]:
    """SQL 쿼리들을 실행하고 ID들을 수집"""
    all_ids = []
    
    for i, sql in enumerate(sql_queries, 1):
        try:
            result = execute_sql_func(sql)
            if isinstance(result, tuple):
                columns, rows = result
                
                # ID 컬럼 찾기
                try:
                    id_index = list(columns).index('ID')
                    ids = [row[id_index] for row in rows if row[id_index] is not None]
                    all_ids.extend(ids)
                except ValueError:
                    print("❌ 'ID' 컬럼이 결과에 없습니다.")
            else:
                print(f"✅ Affected rows: {result}")
        except Exception as e:
            print(f"❌ Error executing SQL {i}: {e}")
    
    return all_ids

def get_top_career_profiles(all_ids: List[str], execute_sql_func, top_n: int = 3):
    """상위 N개 ID 프로필 조회 - ChromaDB 스타일과 같도록 출력"""
    counter = Counter(all_ids)
    most_common_ids = counter.most_common(top_n)
    
    if not most_common_ids:
        return {}
    
    # 상위 ID들 조회
    top_ids = [id_val for id_val, _ in most_common_ids]
    in_clause = ", ".join(f"'{id_val}'" for id_val in top_ids)
    query = f"SELECT * FROM project WHERE ID IN ({in_clause});"
    
    result = execute_sql_func(query)
    columns, rows = result
    
    # ID별 그룹화
    person_projects = defaultdict(list)
    for row in rows:
        row_dict = dict(zip(columns, row))
        person_projects[row_dict['ID']].append(row_dict)
    
    # 간단한 포맷팅
    career_profiles = {}
    for person_id, projects in person_projects.items():
        profile = f"=== 선택된 사원 ===\n사번: {person_id}\n총 경력 수: {len(projects)}개\n\n경력 상세:\n"
        
        for j, p in enumerate(projects, 1):
            years = f"{int(p.get('StartYear', 0))}~{int(p.get('EndYear', 0))}년차"
            skills = ', '.join([str(p.get(f'SkillSet{i}', '')) for i in range(1,5) if p.get(f'SkillSet{i}')])
            
            profile += f"  경력 {j}: {years} - {p.get('Roles', '')}\n"
            profile += f"    스킬셋: {skills}\n"
            profile += f"    도메인: {p.get('Industry', '')}\n"
            profile += f"    프로젝트규모: {p.get('ProjectScale', '')}\n"
            profile += f"    커리어임팩트: {p.get('CareerImpact', '')} - {p.get('CareerImpactDesc', '')}\n"
            profile += f"    요약: {p.get('Project', '')}\n\n"
        
        career_profiles[person_id] = profile
        print(profile)
    
    return career_profiles

def analyze_career_question(user_question: str, execute_sql_func):
    """전체 커리어 분석 프로세스 실행 - ChromaDB 형식 반환"""
    print(f"사용자 질문: {user_question}\n")
    
    # 1. 질문 확장
    expanded_questions = expand_questions(user_question)
    
    # 2. SQL 생성
    sql_queries = generate_sql_queries(expanded_questions)
    print(f"\n생성된 SQL 쿼리 {len(sql_queries)}개:")
    for i, sql in enumerate(sql_queries, 1):
        print(f"{i}. {sql}")
    
    # 3. SQL 실행 및 ID 수집
    all_ids = execute_sql_queries(sql_queries, execute_sql_func)
    
    # 4. 상위 커리어 프로필 조회 및 반환 (ChromaDB 형식)
    career_profiles = get_top_career_profiles(all_ids, execute_sql_func)
    
    return career_profiles

# 사용 예시
if __name__ == "__main__":
    user_question = "반도체 설비관리 및 설비제어, SHE 통합시스템 구축 프로젝트에서 PL 및 PM 역할을 수행한 5년차 경력으로써, 비슷한 경력과 경험을 가진 다른 전문가들이 경력 발전을 위해 어떤 경로를 선택했는지 알려주세요."
    analyze_career_question(user_question, execute_sql)