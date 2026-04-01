# Flex Prompt Template

## 구현 순서

### Step 1. Prompte Template 생성
경로: Setup > Prompt Builder > New Prompt Template 

### Step 2. 세부 사항 입력
- Prompt Template Type: Flex
- Prompt Template Name: 템플릿 이름
- Template Description: 템플릿 설명
- Input (Optional - 5 data sources) : 사용할 리소스
- Input : Name / API Name/ Source Type(Object, Free Text, Data Model Object)
    - Source Type:
        - Object: Salesforce 내 표준/커스텀 Object 데이터
        - Free Text: 사용자가 직접 입력하는 커스텀 텍스트
        - Data Model Object: Data Cloud 데이터 사용 시

### Step 3. 프롬프트 작성 with Resource
- 목적에 맞게 프롬프트를 작성한다.
- Resource가 필요한 경우, 아래 목적에 맞게 Resource 사용이 가능하다.
    - Input 리소스 필요 → Merge Field 사용 ({!$Input:Account.Name})
    - 관계된 Object 데이터 전체 필요 → Related List 사용 ({!$RelatedList:Account.Orders.Records})
    - 날짜 필터 등 조건부 데이터 조회 필요 → Flow 사용 ({!$Flow:FlowAPIName.Prompt})
    - 외부 API 또는 복잡한 로직 필요 → Apex 사용

### Step 4. Save and Activation