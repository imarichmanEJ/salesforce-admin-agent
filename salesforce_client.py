import os
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv()

# Admin이 주로 다루는 핵심 객체 목록
# TODO: 실제 운영 시 동적 조회로 교체
CORE_OBJECTS = [
    "Account", "Contact", "Lead", "Opportunity", "Case",
    "Task", "Event", "Note", "EmailMessage",
    "Contract", "Order", "Product2", "Pricebook2",
    "ServiceAppointment", "WorkOrder", "Asset",
    "User", "UserRole", "CollaborationGroup",
    "Solution", "Entitlement", "ServiceContract",
    "ReturnOrder", "Shipment", "FulfillmentOrder",
]

# Salesforce XML 네임스페이스
SF_NS = "http://soap.sforce.com/2006/04/metadata"


class SalesforceClient:
    def __init__(self):
        self.instance_url = None
        self.access_token = None
        self._authenticate()

    def _authenticate(self):
        """Client Credentials Flow로 액세스 토큰 발급"""
        response = requests.post(
            f"https://{os.environ['SALESFORCE_DOMAIN']}.salesforce.com/services/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "client_id": os.environ["SALESFORCE_CLIENT_ID"],
                "client_secret": os.environ["SALESFORCE_CLIENT_SECRET"],
            }
        )
        response.raise_for_status()
        data = response.json()
        self.access_token = data["access_token"]
        self.instance_url = data["instance_url"]

    @property
    def headers(self):
        return {"Authorization": f"Bearer {self.access_token}"}

    def get_core_objects(self) -> list[dict]:
        """핵심 객체 이름 + 레이블 반환 (캐싱용)"""
        response = requests.get(
            f"{self.instance_url}/services/data/v59.0/sobjects/",
            headers=self.headers
        )
        response.raise_for_status()

        all_objects = {
            obj["name"]: obj["label"]
            for obj in response.json()["sobjects"]
        }

        return [
            {"name": name, "label": all_objects.get(name, name)}
            for name in CORE_OBJECTS
            if name in all_objects
        ]

    def describe_object(self, object_name: str) -> dict:
        """특정 객체의 필드 목록 조회"""
        response = requests.get(
            f"{self.instance_url}/services/data/v59.0/sobjects/{object_name}/describe/",
            headers=self.headers
        )
        response.raise_for_status()
        data = response.json()

        fields = [
            {
                "name": f["name"],
                "label": f["label"],
                "type": f["type"],
                "updateable": f["updateable"],
                "referenceTo": f.get("referenceTo", []),
            }
            for f in data.get("fields", [])
        ]

        return {
            "name": data["name"],
            "label": data["label"],
            "fields": fields,
        }

    def describe_objects(self, object_names: list[str]) -> list[dict]:
        """여러 객체 describe 한번에 처리"""
        return [self.describe_object(name) for name in object_names]

    def get_prompt_templates(self) -> list[dict]:
        """Salesforce CLI로 Custom Prompt Template 목록 조회

        1. CLI로 GenAiPromptTemplate 메타데이터 pull
        2. 로컬 XML 파일 파싱
        3. [{name, label, type, status, model}] 반환
        """
        sfdx_project_path = os.environ.get("SFDX_PROJECT_PATH", "")
        org_alias = os.environ.get("SFDX_ORG_ALIAS", "")

        if not sfdx_project_path or not org_alias:
            return []

        # CLI로 메타데이터 pull
        try:
            cmd = f"sf project retrieve start -m GenAiPromptTemplate -o {org_alias}"
            subprocess.run(
                cmd,
                cwd=sfdx_project_path,
                capture_output=True,
                shell=True,
                timeout=120,
                check=True
            )
        except subprocess.CalledProcessError:
            return []
        except subprocess.TimeoutExpired:
            return []

        # XML 파일 파싱
        templates_dir = Path(sfdx_project_path) / "force-app" / "main" / "default" / "genAiPromptTemplates"
        if not templates_dir.exists():
            return []

        templates = []
        for xml_file in templates_dir.glob("*.genAiPromptTemplate-meta.xml"):
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()

                def get_text(tag):
                    el = root.find(f"{{{SF_NS}}}{tag}")
                    return el.text.strip() if el is not None and el.text else ""

                # templateVersions 안에서 status, model 추출
                version = root.find(f"{{{SF_NS}}}templateVersions")
                status = ""
                model = ""
                if version is not None:
                    status_el = version.find(f"{{{SF_NS}}}status")
                    model_el = version.find(f"{{{SF_NS}}}primaryModel")
                    status = status_el.text.strip() if status_el is not None and status_el.text else ""
                    model = model_el.text.strip() if model_el is not None and model_el.text else ""

                templates.append({
                    "name": get_text("developerName"),
                    "label": get_text("masterLabel"),
                    "type": get_text("type"),
                    "status": status,
                    "model": model,
                    "category": "Custom",
                })
            except ET.ParseError:
                continue

        return templates