# Agent Skill

## 역할
사용자가 자연어로 여러 작업을 처리할 수 있는 Agentforce Agent를 설계하고 구현한다.
Agent는 항상 다른 모든 기능(Flow, Prompt Template, Apex) 구현 완료 후 마지막에 구성한다.

---

## 0. Agent 사용 여부 판단

Use Agent when:
- 사용자와 대화형 인터랙션이 필요한 경우
- 여러 작업을 대화 흐름으로 묶어야 하는 경우
- 고객 문의를 자동으로 처리해야 하는 경우

Otherwise:
- 백그라운드 자동화만 필요 → Flow
- AI 텍스트 생성만 필요 → Prompt Template

**전제 조건:** Agentforce 활성화 (setup_skill.md 참조)

---

## 1. Agent 구성요소

| 구성요소 | 역할 |
|---------|------|
| Topic | 에이전트가 처리할 작업 카테고리 |
| Action | Topic 안에서 실제 실행되는 개별 작업 |
| Instructions | Topic별 행동 가이드라인 및 제약 |

Action이 호출할 수 있는 것:
- Autolaunched Flow
- Prompt Template (Flex 타입)
- Apex (@InvocableMethod)

---

## 2. Agent 타입 선택

| 타입 | 용도 |
|------|------|
| Agentforce Service Agent | 고객 서비스, Case 처리, 24/7 응답 |
| Agentforce Sales Agent | 영업 프로스펙팅, 리드 관리 |
| Agentforce (Default) | 내부 직원용 범용 에이전트 |
| Custom Agent | 특정 비즈니스 요구에 맞게 처음부터 구성 |

---

## 3. 구현 단계

**전제 조건:** 연결할 Flow / Prompt Template / Apex 먼저 생성 완료

### Step 1. Agent 생성
```
Setup → Quick Find: "Agents" → Agentforce Agents → New Agent
→ Agent 타입 선택
→ Agent 이름, 역할 설명, Run As 사용자 설정
```

### Step 2. Topic 및 Action 설정
```
Agent Builder → Topic 추가
→ Topic 이름 + Instructions 작성 (자연어로 행동 지침 명시)
→ Action 추가 → Flow / Prompt Template / Apex 선택 및 연결
```

※ Action 이름과 설명을 명확하게 작성해야 LLM이 올바른 Action을 선택함

### Step 3. 테스트
```
Agent Builder → Conversation Preview
→ 시나리오별 입력 테스트
→ Event Logs로 Topic/Action 선택 과정 확인
→ Instructions 보완
```

### Step 4. 배포
```
Agent Builder → Activate
→ 채널 선택 (Slack / Experience Site / CRM 등)
```

---

## 4. 주의사항

- Action 설명이 불명확하면 LLM이 잘못된 Action을 선택할 수 있음 → 설명을 구체적으로 작성
- Run As 사용자의 Permission Set이 필요한 데이터에 접근 가능한지 확인 필수
- Escalation Topic 설정 권장 (사람 상담원으로 전환)
- Agent Builder UI는 릴리즈마다 변경될 수 있음 → Trailhead 가이드와 실제 UI가 다를 수 있음

---

## 5. 출력
- Agent 타입 및 구성 이유
- Topic 목록 + 각 Topic의 Instructions
- Action 목록 + 연결된 Flow / Prompt Template / Apex
- Permission Set 확인 사항