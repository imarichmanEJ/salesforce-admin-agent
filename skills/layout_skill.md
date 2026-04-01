# Layout Skill

## 역할
Salesforce Object의 필드(Field)를 생성하고, 레코드 페이지에 배치하여 Flow, Prompt Template, Agent에서 사용할 수 있도록 한다.

---

## 1. 필드 필요 여부 판단

### 규칙
- 기존 필드로 해결 가능한지 먼저 확인
- 기존 필드가 있으면 반드시 재사용
- 새로운 필드는 필요한 경우에만 생성

### 필드 생성이 필요한 경우
- AI 생성 결과를 저장해야 할 때
- 기존 Object에 없는 데이터가 필요한 경우
- Object 간 관계가 필요한 경우 (Lookup)

---

## 2. 필드 Naming 규칙

### 규칙
- API Name: PascalCase + `__c`
- 공백은 `_`로 변환
- 의미가 명확해야 함

### 예시
- Quick Summary → `Quick_Summary__c`
- Translated Description → `Translated_Description__c`
- Customer Sentiment → `Customer_Sentiment__c`

---

## 3. 필드 타입 선택 기준

| Use Case | Field Type |
|---------|-----------|
| 요약 / 번역 / 생성 텍스트 | Long Text Area |
| 짧은 텍스트 | Text |
| 상태 / 분류 | Picklist |
| 날짜 | Date / DateTime |
| 숫자 | Number |
| Object 참조 | Lookup |

---

## 4. 필드 생성

### 경로
Setup → Object Manager → 대상 Object → Fields & Relationships → New

### 작업
1. Field Type 선택
2. Label 입력
3. API Name 확인
4. Field-Level Security 설정

---

### Lookup Field 생성 (관계 연결)

#### 조건
- 두 개 이상의 Object를 연결해야 하는 경우

#### 작업
1. Field Type → Lookup 선택
2. 연결할 Object 선택
3. 저장

---

## 5. Layout 구성

### 5.1 Page Layout

#### 역할
- 필드를 레코드 페이지에 표시
- Related List, 버튼, 액션 관리

#### 경로
Setup → Object Manager → Object → Page Layouts

---

### 5.2 Lightning App Builder

#### 역할
- 페이지 구조 및 컴포넌트 배치

#### 경로
레코드 페이지 → 설정 아이콘 → Edit Page

---

### 5.3 Dynamic Forms (권장)

#### 역할
- 필드를 개별 단위로 배치
- 조건부 표시 가능

#### 활성화
Lightning App Builder → Record Detail → Upgrade Now

---

## 6. Prompt Template 연결

### Field Generation 타입일 경우

#### 경로
App Launcher → Object → 레코드 → 설정 아이콘 → Edit Page

#### 작업
- 생성한 Field에 Prompt Template 연결
- 자세한 설정은 `field_generation.md Step 4-A` 참조

---

## 7. 실행 순서 규칙

- 필드 생성은 반드시 다른 기능보다 먼저 수행
- Prompt Template 생성보다 먼저 수행
- Dynamic Forms 연결은 Prompt Template 이후 수행 가능

---

## 8. 출력

- 생성 또는 재사용된 Field 목록
- Field API Name
- Field Type
- Layout 적용 방법