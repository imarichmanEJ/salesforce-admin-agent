# Prompt Builder Skill

## 구현 순서

### 1. Template Type 선택

Field Generation:
- 단일 Object 필드에 결과 저장
- 예: Case 요약 → Case.Summary__c

Sales Email:
- 이메일 생성 (Recipient 존재)

Flex:
- 두 개 이상의 Object 필요
- 또는 Flow / Apex / 외부 데이터 필요


---

### 2. 선택한 Template Type 에 맞춰 가이드 생성

Field Genration → prompt_type/field_generation.md 참고
Sales Email → prompt_type/sales_email.md 참고
Flex → prompt_type/flex.md 참고


---

### 3. 기존 템플릿 확인
- 기존 템플릿 중에 목적에 맞는 템플렛이 있는지 검토한다.

##### Standard 템플릿 (Salesforce 기본 제공)

| Name | Template Type | Category | Description |
|------|--------------|----------|-------------|
| Account Summary | Record Summary | Standard | Account 레코드의 리치 텍스트 요약 생성 |
| Generate Case Description - Messaging Transcript | Case Details | Standard-Overridable | 채팅 트랜스크립트 기반 케이스 설명 생성 |
| Anomaly Details | Anomaly Analysis | Standard | 보안 이상 징후 분석 |
| Revenue Reconciliation Analysis | Global Standard | Standard | 총계정원장과 Opportunity 비교해 불일치 식별 |
| Executive Brief | Record Summary | Standard | 임원 브리핑용 Account 정보 요약 |
| Generate Case Subject - Messaging Transcript | Case Details | Standard-Overridable | 채팅 트랜스크립트 기반 케이스 제목 생성 |
| Investigation - Investigate User | User Investigation | Standard | 사용자 프로필/활동/권한 종합 조사 |
| Slack Channel Summary | Slack Channel Summarizer | Standard | Slack 채널 콘텐츠 요약 |
| Refine Text | Write with AI | Standard | 텍스트를 더 전문적이고 명확하게 다듬기 |
| Identify Anomalies | Anomaly Detection | Standard | 보안 경고 데이터 분석으로 이상 징후 식별 |
| Answer Questions with Knowledge | Knowledge Answers | Standard-Overridable | Knowledge 베이스로 사용자 질의 응답 |
| Expand Text | Write with AI | Standard | 텍스트에 세부 정보와 맥락 추가 |
| Classify Security Risk | Security Risk Analysis | Standard | Salesforce 보안 데이터 분석해 위험 분류 |
| Summarize Messaging Session | Record Summary | Standard | MessagingSession 객체 기반 요약 생성 |
| Summarize Text | Write with AI | Standard | 텍스트를 핵심 포인트로 요약 |
| Create Executive Briefing for Account Review Meeting | Global Standard | Standard | Account 검토 회의용 임원 브리핑 생성 |

※ Standard-Overridable: 커스터마이즈 가능
※ Standard: 수정 불가, 재활용만 가능

##### Custom 템플릿 (Org에 직접 만들어진 것)

Salesforce CLI로 조회:
```bash
sf project retrieve start -m GenAiPromptTemplate -o {org_alias}
# 결과: force-app/main/default/genAiPromptTemplates/*.genAiPromptTemplate-meta.xml
```


---

### 4. Prompt Builder 최종 가이드 작성

Step 1. 사전 조건 확인
- Einstein 활성화: `Setup → Einstein Setup → Turn on Einstein`
- Agentforce 활성화: `Setup → Salesforce Go → Agentforce(Default) → Turn on`
- Sales Email 유형인 경우, `Setup → Einstein for Sales > Turn on Sales Emails`

Step 2. Prompt Template 생성 가이드
- 앞서 생성한 가이드 출력
- 관련된 기존 템플릿이 있는 경우, 해당 템플릿도 있으니 검토하라고 언급

Step 3. 관련된 기존 템플릿이 있는 경우,
- 해당 템플릿도 있으니 검토하라고 언급
- 없는 경우 무시