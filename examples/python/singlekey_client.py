"""
SingleKey API Python Client

A complete Python client for the SingleKey Screening API.

Installation:
    pip install requests

Usage:
    from singlekey_client import SingleKeyClient

    client = SingleKeyClient("your_api_token")
    result = client.create_screening(landlord, tenant)
"""

import requests
import time
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class Environment(Enum):
    PRODUCTION = "https://platform.singlekey.com"
    SANDBOX = "https://sandbox.singlekey.com"


@dataclass
class Landlord:
    """Landlord information for screening request."""
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    external_id: Optional[str] = None


@dataclass
class TenantDOB:
    """Tenant date of birth."""
    year: int
    month: int
    day: int


@dataclass
class Tenant:
    """Tenant information for screening request."""
    first_name: str
    last_name: str
    email: str
    phone: str
    dob: TenantDOB
    address: str
    sin: str  # SIN for Canada, SSN for USA
    external_id: Optional[str] = None
    middle_name: Optional[str] = None
    employer: Optional[str] = None
    job_title: Optional[str] = None
    annual_income: Optional[int] = None


@dataclass
class Property:
    """Property information for screening."""
    address: str
    rent: Optional[int] = None
    unit: Optional[str] = None


class SingleKeyError(Exception):
    """Base exception for SingleKey API errors."""
    def __init__(self, message: str, errors: List[str] = None):
        super().__init__(message)
        self.errors = errors or []


class AuthenticationError(SingleKeyError):
    """Raised when authentication fails."""
    pass


class ValidationError(SingleKeyError):
    """Raised when request validation fails."""
    pass


class NotFoundError(SingleKeyError):
    """Raised when resource is not found."""
    pass


class SingleKeyClient:
    """
    SingleKey API client for tenant screening.

    Example:
        client = SingleKeyClient("your_api_token")

        # Create a screening
        result = client.create_screening(
            landlord=Landlord(
                first_name="John",
                last_name="Smith",
                email="john@example.com"
            ),
            tenant=Tenant(
                first_name="Jane",
                last_name="Doe",
                email="jane@example.com",
                phone="5551234567",
                dob=TenantDOB(year=1990, month=6, day=15),
                address="123 Main St, Toronto, ON, Canada, M5V 1A1",
                sin="123456789"
            )
        )

        # Get report
        report = client.get_report(result["purchase_token"])
    """

    def __init__(
        self,
        api_token: str,
        environment: Environment = Environment.PRODUCTION,
        timeout: int = 30
    ):
        """
        Initialize the SingleKey client.

        Args:
            api_token: Your SingleKey API token
            environment: PRODUCTION or SANDBOX
            timeout: Request timeout in seconds
        """
        self.api_token = api_token
        self.base_url = environment.value
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Token {api_token}",
            "Content-Type": "application/json"
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Dict = None,
        params: Dict = None
    ) -> Dict[str, Any]:
        """Make an API request."""
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.timeout
            )

            # Handle different status codes
            if response.status_code == 401:
                raise AuthenticationError("Invalid API token")

            if response.status_code == 404:
                raise NotFoundError("Resource not found")

            result = response.json()

            # Check for API-level errors
            if not result.get("success", True) and result.get("errors"):
                raise ValidationError(
                    result.get("detail", "Validation failed"),
                    result.get("errors", [])
                )

            return result

        except requests.exceptions.Timeout:
            raise SingleKeyError("Request timed out")
        except requests.exceptions.ConnectionError:
            raise SingleKeyError("Connection failed")

    def create_screening(
        self,
        landlord: Landlord,
        tenant: Tenant,
        property_info: Property = None,
        run_now: bool = True,
        tenant_pays: bool = False,
        callback_url: str = None,
        external_deal_id: str = None
    ) -> Dict[str, Any]:
        """
        Create a new screening request.

        Args:
            landlord: Landlord information
            tenant: Tenant information
            property_info: Property details (optional)
            run_now: Process immediately (default True)
            tenant_pays: Tenant provides payment (default False)
            callback_url: Webhook URL for notifications
            external_deal_id: Your CRM deal ID

        Returns:
            Dict with purchase_token and status
        """
        payload = {
            "external_customer_id": landlord.external_id or f"ll-{landlord.email}",
            "external_tenant_id": tenant.external_id or f"tn-{tenant.email}",
            "run_now": run_now,
            "tenant_pays": tenant_pays,

            # Landlord info
            "ll_first_name": landlord.first_name,
            "ll_last_name": landlord.last_name,
            "ll_email": landlord.email,

            # Tenant info
            "ten_first_name": tenant.first_name,
            "ten_last_name": tenant.last_name,
            "ten_email": tenant.email,
            "ten_tel": tenant.phone,
            "ten_dob_year": tenant.dob.year,
            "ten_dob_month": tenant.dob.month,
            "ten_dob_day": tenant.dob.day,
            "ten_address": tenant.address,
            "ten_sin": tenant.sin,
        }

        # Optional fields
        if landlord.phone:
            payload["ll_tel"] = landlord.phone

        if tenant.middle_name:
            payload["ten_middle_name"] = tenant.middle_name

        if tenant.employer:
            payload["ten_employer"] = tenant.employer

        if tenant.job_title:
            payload["ten_job_title"] = tenant.job_title

        if tenant.annual_income:
            payload["ten_annual_income"] = tenant.annual_income

        if property_info:
            payload["purchase_address"] = property_info.address
            if property_info.rent:
                payload["purchase_rent"] = property_info.rent
            if property_info.unit:
                payload["purchase_unit"] = property_info.unit

        if callback_url:
            payload["callback_url"] = callback_url

        if external_deal_id:
            payload["external_deal_id"] = external_deal_id

        return self._request("POST", "/api/request", data=payload)

    def create_form_request(
        self,
        landlord: Landlord,
        tenant_email: str,
        tenant_first_name: str = None,
        tenant_last_name: str = None,
        property_address: str = None,
        tenant_form: bool = False,
        callback_url: str = None
    ) -> Dict[str, Any]:
        """
        Create a form-based screening request.

        Args:
            landlord: Landlord information
            tenant_email: Tenant's email address
            tenant_first_name: Tenant's first name (optional)
            tenant_last_name: Tenant's last name (optional)
            property_address: Property address (required for tenant_form)
            tenant_form: Use direct tenant form (default False)
            callback_url: Webhook URL for notifications

        Returns:
            Dict with purchase_token and form_url
        """
        payload = {
            "external_customer_id": landlord.external_id or f"ll-{landlord.email}",
            "external_tenant_id": f"tn-{tenant_email}",

            # Landlord info
            "ll_first_name": landlord.first_name,
            "ll_last_name": landlord.last_name,
            "ll_email": landlord.email,

            # Tenant info
            "ten_email": tenant_email,
        }

        if landlord.phone:
            payload["ll_tel"] = landlord.phone

        if tenant_first_name:
            payload["ten_first_name"] = tenant_first_name

        if tenant_last_name:
            payload["ten_last_name"] = tenant_last_name

        if tenant_form:
            payload["tenant_form"] = True
            if property_address:
                payload["purchase_address"] = property_address

        if callback_url:
            payload["callback_url"] = callback_url

        return self._request("POST", "/api/request", data=payload)

    def get_report(self, purchase_token: str) -> Dict[str, Any]:
        """
        Get screening report.

        Args:
            purchase_token: Token from create_screening

        Returns:
            Dict with report data or status
        """
        return self._request("GET", f"/api/report/{purchase_token}")

    def get_applicant(
        self,
        purchase_token: str,
        detailed: bool = False,
        show_credit_score: bool = False
    ) -> Dict[str, Any]:
        """
        Get applicant information.

        Args:
            purchase_token: Token from create_screening
            detailed: Include detailed information
            show_credit_score: Include credit score

        Returns:
            Dict with applicant data
        """
        params = {}
        if detailed:
            params["detailed"] = "true"
        if show_credit_score:
            params["show_credit_score"] = "true"

        return self._request(
            "GET",
            f"/api/applicant/{purchase_token}",
            params=params
        )

    def validate_screening(self, screening_id: str) -> Dict[str, Any]:
        """
        Validate screening data for errors.

        Args:
            screening_id: The screening ID to validate

        Returns:
            Dict with validation status and any errors
        """
        return self._request("POST", f"/api/purchase_errors/{screening_id}")

    def download_pdf(self, purchase_token: str, output_path: str) -> bool:
        """
        Download screening report as PDF.

        Args:
            purchase_token: Token from create_screening
            output_path: File path to save the PDF

        Returns:
            True if successful
        """
        url = f"{self.base_url}/api/report_pdf/{purchase_token}"

        response = self.session.get(url, stream=True, timeout=self.timeout)

        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True

        if response.status_code == 404:
            raise NotFoundError("Report not found")

        raise SingleKeyError(f"Failed to download PDF: {response.status_code}")

    def wait_for_report(
        self,
        purchase_token: str,
        timeout: int = 300,
        poll_interval: int = 10
    ) -> Dict[str, Any]:
        """
        Poll until report is ready.

        Args:
            purchase_token: Token from create_screening
            timeout: Maximum seconds to wait
            poll_interval: Seconds between checks

        Returns:
            Completed report data
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            report = self.get_report(purchase_token)

            if report.get("success") and report.get("singlekey_score"):
                return report

            logger.info(f"Status: {report.get('detail', 'Processing...')}")
            time.sleep(poll_interval)

        raise SingleKeyError("Timeout waiting for report")


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Initialize client
    client = SingleKeyClient(
        api_token="your_api_token",
        environment=Environment.SANDBOX
    )

    try:
        # Create screening
        result = client.create_screening(
            landlord=Landlord(
                external_id="landlord-123",
                first_name="John",
                last_name="Smith",
                email="john@example.com",
                phone="5551234567"
            ),
            tenant=Tenant(
                external_id="tenant-456",
                first_name="Jane",
                last_name="Doe",
                email="jane@example.com",
                phone="5559876543",
                dob=TenantDOB(year=1990, month=6, day=15),
                address="456 Oak Ave, Toronto, ON, Canada, M5V 2B3",
                sin="123456789"
            ),
            property_info=Property(
                address="123 Main St, Toronto, ON, Canada, M5V 1A1",
                rent=2000
            ),
            callback_url="https://yoursite.com/webhooks/singlekey"
        )

        print(f"Screening created: {result['purchase_token']}")

        # Wait for report
        report = client.wait_for_report(result['purchase_token'])

        print(f"SingleKey Score: {report['singlekey_score']}")
        print(f"Report URL: {report['report_url']}")

        # Download PDF
        client.download_pdf(result['purchase_token'], "screening_report.pdf")
        print("PDF saved to screening_report.pdf")

    except ValidationError as e:
        print(f"Validation failed: {e}")
        for error in e.errors:
            print(f"  - {error}")

    except SingleKeyError as e:
        print(f"API error: {e}")
