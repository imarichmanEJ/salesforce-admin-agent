# Apex Skill

## 역할
Flow로 구현하기 어려운 로직을 Apex로 구현한다.
Apex는 데이터 처리 및 계산 로직을 담당한다.

---

## 0. Apex 사용 조건

Use Apex when:
- 2개 이상의 Object 데이터를 조합해야 하는 경우
- 데이터 변환/가공/집계 필요
- Loop 또는 반복 처리 필요
- 조건 분기가 복잡한 경우
- 외부 API 호출 필요

Otherwise → Flow 사용

---

## 1. Apex 구조 (중요)

Apex는 반드시 2계층 구조로 작성한다:

1. Invocable Class (인터페이스)
2. Service Class (비즈니스 로직)

---

## 2. Apex 패턴

### 2-1. Invocable Class (Flow / Agent에서 호출)

- Flow 또는 Agent Action에서 호출되는 진입점
- 실제 로직은 Service Class에 위임

```java
public class {ClassName}Invoker {

    @InvocableMethod(label='{Label}')
    public static List<Output> execute(List<Input> inputs) {
        return {ServiceClass}.process(inputs);
    }

    public class Input {
        @InvocableVariable(required=true)
        public Id recordId;
    }

    public class Output {
        @InvocableVariable
        public String result;
    }
}
```

---

### 2-2. Service Class (핵심 로직)

- 실제 데이터 처리 수행
- 재사용 가능하도록 설계

```java
public class {ServiceClass} {

    public static List<{InvokerClass}.Output> process(List<{InvokerClass}.Input> inputs) {

        List<{InvokerClass}.Output> results = new List<{InvokerClass}.Output>();

        Set<Id> ids = new Set<Id>();
        for ({InvokerClass}.Input inp : inputs) {
            ids.add(inp.recordId);
        }

        List<{SObject}> records = [
            SELECT Id, {fields}
            FROM {SObject}
            WHERE Id IN :ids
        ];

        for ({SObject} rec : records) {
            {InvokerClass}.Output out = new {InvokerClass}.Output();
            out.result = {값};
            results.add(out);
        }

        return results;
    }
}
```

---

## 3. External API Callout

- 반드시 @InvocableMethod(callout=true)

```java
@InvocableMethod(label='{Label}' callout=true)
```

---

## 4. Governor Limits 핵심 규칙

- SOQL은 Loop 밖에서 1회
- DML은 List로 모아서 1회
- Bulk-safe 구조 유지

---

## 5. 금지 사항

- Trigger 생성 금지 (Flow로 대체)
- Loop 안에 SOQL/DML 금지
- 단일 레코드 처리 금지
- Hardcoding 금지

---

## 6. 연결 방식

### Flow에서 연결
- Flow Builder → Action → Apex 선택
- InvocableMethod 선택 후 Input/Output 매핑

### Agent에서 연결
- Agent Builder → Actions → Apex 선택
- InvocableMethod 선택

---

## 7. 출력
use case를 분석해서 아래를 출력한다:
- Invoker Class 완전한 코드 (Input/Output 포함)
- Service Class 완전한 코드
- Flow/Agent 연결 방법
- Governor Limits 주의사항 (해당 코드 기준)