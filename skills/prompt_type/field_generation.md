# Field Generation Prompt Template

## 구현 순서

### Step 1. 사전 확인
- AI가 채울 필드가 어느 Object에 있는지 확인한다.
- 해당 Object에 채울 필드가 없으면 Step2 부터, 있으면 Step3 부터 시작한다.

### Step 2. 필드 생성 (신규 필드 필요 시)
layout_skill.md에서 New Field 부분 참고해서 필드를 생성한다.

### Step 3. Prompt Template 생성
경로 : Setup > Prompt Builder > New Prompt Template

### Step 4. 세부 사항 입력
- Prompt Template Type: Field Generation
- Prompt Template Name: 템플릿 이름
- Template Description: 템플릿 설명
- Object: AI가 채울 필드가 있는 Object
- Object Field: AI가 채울 필드 선택

### Step 5. 프롬프트 작성 with Resource
- 목적에 맞게 프롬프트를 작성한다.
- Resource가 필요한 경우, 아래 목적에 맞게 Resource 사용이 가능하다.
    - Primary Object 필드값 필요 → Merge Field 사용 ({!$Input:Account.Name})
    - 관계된 Object 데이터 전체 필요 → Related List 사용 ({!$RelatedList:Account.Orders.Records})
    - 날짜 필터 등 조건부 데이터 조회 필요 → Flow 사용 ({!$Flow:FlowAPIName.Prompt})
    - 외부 API 또는 복잡한 로직 필요 → Apex 사용

### Step 6. Save and Activation