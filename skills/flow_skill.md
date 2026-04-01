# Flow Skill

## 역할
Use case에 맞는 Flow 솔루션을 선택하고, 재사용 또는 신규 생성 여부를 판단하여 구현 가이드를 제공한다.

---

## 0. Flow 사용 여부 판단 (중요)

Use Flow when:
- 레코드 생성/수정 기반 자동화가 필요할 때
- 단순 조건 분기 및 데이터 업데이트
- Prompt Template 호출 및 오케스트레이션

Use Apex instead when:
- 2개 이상의 Object를 복잡하게 조합해야 하는 경우
- 반복(loop), 집계, 조건 분기가 복잡한 경우
- 외부 API 호출이 필요한 경우
- 데이터 가공/변환 로직이 복잡한 경우

※ 위 조건에 해당하면 Flow 대신 Apex 사용 (apex_skill.md 참조)

---

## 1. 기존 Template Flow 재활용 (최우선)

아래 목록에서 목적에 맞는 Template이 있으면 반드시 재사용한다.

| Template | Flow Type | 설명 |
|---------|-----------|------|
| Route Conversations to Agentforce Service Agents | Omni-Channel Flow | 조건 기반 Agentforce 라우팅 |
| Find Contact Associated with Messaging Session | Autolaunched Flow | Messaging → Contact 연결 |
| Create Work Order from Case | Record-Triggered Flow | Case 기반 Work Order 생성 |
| Check Service Plan Eligibility | Autolaunched Flow | 서비스 플랜 자격 검증 |
| Check Service Plan Eligibility for MessagingSession | Autolaunched Flow | MessagingSession 기준 검증 |
| Chats Routed to Agents and Queues | Omni-Channel Flow | 채팅 라우팅 |
| Voice Calls Routed to Agents and Queues | Omni-Channel Flow | 음성 라우팅 |
| Messages Routed to Agents and Queues | Omni-Channel Flow | 메시지 라우팅 |
| Close Case | Autolaunched Flow | Case 종료 처리 |
| Create a Case | Autolaunched Flow | Case 생성 |

### Rule
- 유사한 Template이 존재하면 반드시 재사용
- 신규 생성은 Template로 해결 불가능한 경우에만 진행

---

## 2. Flow Type 선택 (단순화)

| Use Case | Flow Type |
|---------|-----------|
| 레코드 생성/수정 시 자동 실행 | Record-Triggered Flow |
| 다른 기능에서 호출 (Prompt Template / Agent) | Autolaunched Flow |
| Prompt Template에 데이터 주입 | Template-Triggered Prompt Flow |
| Agentforce 라우팅 | Omni-Channel Flow |

### 제한
- Screen Flow는 명시적으로 요구되지 않는 한 사용 금지
- Schedule Flow는 특수한 경우에만 사용

---

## 3. 신규 Flow 생성 (표준 패턴 기반)

### 3-1. Record-Triggered Flow

1. Setup → Flow → New Flow
2. Record-Triggered Flow 선택
3. Object: {object_name}
4. Trigger:
   - Record Created
   - 또는 Record Created or Updated

5. (Optional) Entry Condition 설정

6. Action:
   - Prompt Template 호출
   또는
   - Update Records (필드 업데이트)

7. Save → Activate

---

### 3-2. Autolaunched Flow

1. Setup → Flow → New Flow
2. Autolaunched Flow 선택

3. (Optional) Get Records 추가
4. (Optional) Assignment / Decision 추가
5. Output 변수 설정 (필요 시)

6. Save → Activate

---

### 3-3. Template-Triggered Prompt Flow

1. Setup → Flow → New Flow
2. Template-Triggered Prompt Flow 선택

3. Input 변수 정의 (Prompt Template에서 전달)
4. 필요한 데이터 조회 (Get Records)
5. Output 구성 (Prompt Template에서 사용)

6. Save → Activate

---

### 3-4. Omni-Channel Flow

1. Setup → Omni-Channel Flow
2. New Flow 생성
3. 조건 설정
4. Queue 또는 Agent로 라우팅 설정
5. Save → Activate

---

## 4. Flow 설계 원칙 (중요)

- Flow는 “단순 orchestration” 용도로만 사용
- 복잡한 로직 구현 금지
- Object 간 관계 처리 최소화
- 1~2개의 핵심 Action만 포함

---

## 5. Apex 전환 기준 (강제 규칙)

아래 조건 중 하나라도 해당하면 Flow 대신 Apex 사용:

- 2개 이상의 Object 데이터 조합 필요
- Loop / Aggregation 필요
- 조건 분기가 2단계 이상
- 외부 API 호출 필요
- 데이터 가공/변환 로직 존재

→ apex_skill.md 참조

---

## 6. 최종 출력

- 선택된 Flow 유형
- Template 재사용 여부
- 또는 신규 Flow 생성 가이드
- (필요 시) Apex 전환 안내