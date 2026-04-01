# Sales Email Template

## 구현 순서

### Step 1. Sales Email prompt template type 활성화
경로: Setup > Einstein for Sales > Turn on Sales Emails

### Step 2. Prompte Template 생성
경로: Setup > Prompt Builder > New Prompt Template 

### Step 3. 세부 사항 입력
- Prompt Template Type: Sales Email
- Prompt Template Name: 템플릿 이름
- Template Description: 템플릿 설명
- recipient : 수신인 정보가 있는 Object (e.g Contact, Lead, Person Account)
- Related Object: 1개만 선택 가능
  ※ 2개 이상 Object가 필요하면 Flex 타입 사용

### Step 4. 프롬프트 작성 with Resource
- 목적에 맞게 프롬프트를 작성한다.
- Resource가 필요한 경우, 아래 목적에 맞게 Resource 사용이 가능하다.
    - Input 리소스 필요 → Merge Field 사용 ({!$Input:Account.Name})
    - 관계된 Object 데이터 전체 필요 → Related List 사용 ({!$RelatedList:Account.Orders.Records})
    - 날짜 필터 등 조건부 데이터 조회 필요 → Flow 사용 ({!$Flow:FlowAPIName.Prompt})
    - 외부 API 또는 복잡한 로직 필요 → Apex 사용

### Step 5. Save and Activation