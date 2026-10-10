import allure
import pytest

from src.main.api.fixtures.api_fixture import *
from src.main.api.fixtures.object_fixture import *
from src.main.api.fixtures.user_fixture import *
from src.main.api.fixtures.db_fixture import *
from src.main.ui.fixstures.data_fixture import *
from src.main.ui.fixstures.login_fixture import *


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"report_{report.when}", report)

@pytest.fixture(autouse=True)
def screenshot(request, page):
    yield
    report = getattr(request.node, "report_call", None)
    if report and report.failed:
        allure.attach(
            page.screenshot(full_page=True),
            name = "screenshot_on_failure",
            attachment_type=allure.attachment_type.PNG,
        )