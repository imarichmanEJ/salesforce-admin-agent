# Setup Skill

## 역할
use case 구현에 필요한 Salesforce 기능만 선택적으로 활성화하고, 필수 권한을 설정한다.  
항상 다른 모든 작업보다 먼저 수행한다.

---

## 0. Setup 실행 원칙 (매우 중요)

모든 설정은 "필요한 경우에만" 수행한다.

### 조건부 활성화 규칙

- Prompt Template 포함 → Einstein 활성화
- Agent 포함 → Agentforce 활성화
- Sales Email 포함 → Einstein for Sales 활성화
- Agent 사용 → Permission Set 설정
- 외부 API / OAuth 필요 → Connected App 설정

불필요한 기능은 절대 활성화하지 않는다.

---

## 1. Einstein 활성화 (조건부)

### 언제 필요한가
- Prompt Template (Field Generation / Flex / Sales Email) 사용 시

### 경로
Setup → Quick Find: "Einstein Setup" → Einstein Setup

### 작업
- Turn on Einstein 토글 활성화

---

## 2. Agentforce 활성화 (조건부)

### 언제 필요한가
- Agent Step이 포함된 경우

### 전제 조건
- Einstein 활성화 완료

### 경로
Setup → Quick Find: "Agents" → Agentforce

### 작업
- Enable Agentforce 토글 활성화

---

## 3. Einstein for Sales 활성화 (조건부)

### 언제 필요한가
- Sales Email Prompt Template 사용 시

### 전제 조건
- Einstein 활성화 완료

### 경로
Setup → Quick Find: "Einstein for Sales"

### 작업
- Enable Einstein for Sales 클릭

### 주의사항
- 별도 라이선스 필요할 수 있음

---

## 4. Permission Set 설정 (조건부)

### 언제 필요한가
- Agent 사용 시 (필수)
- Prompt Template / Flow 실행 권한 필요 시

### 생성 경로
Setup → Quick Find: "Permission Sets" → New

### 주요 권한

| 기능 | 필요 권한 |
|------|---------|
| Prompt Template | Use Prompt Builder, Access Einstein Generative AI |
| Agentforce Admin | Customize Application |
| Agentforce 사용자 | Agent Access |

### Agent 권한 설정
Permission Set → Agent Access → 사용할 Agent 선택 → 사용자에게 할당

---

## 5. Connected App 설정 (Optional)

### 언제 필요한가
- 외부 API 호출
- OAuth 인증 필요

### 경로
Setup → App Manager → New Connected App

### 작업
- OAuth 활성화
- Callback URL 설정
- OAuth Scope 설정 (api, refresh_token 등)

---

## 6. 출력 규칙

각 항목은 아래 형식으로 작성:

### [설정 항목 이름]

- 필요 여부: Yes / No
- 실행 경로:
- 설정 작업:
- 주의사항: (필요 시)

---

## 7. 출력 예시

### Einstein 활성화
- 필요 여부: Yes
- 실행 경로: Setup → Einstein Setup
- 설정 작업: Turn on Einstein 활성화

### Agentforce 활성화
- 필요 여부: No