import functools
from typing import Any

from allure import link, parent_suite, suite, title
from allure_commons._allure import StepContext, attach  # noqa: WPS436
from allure_commons.types import AttachmentType
from allure_commons.utils import func_parameters, represent


class CustomStepContext(StepContext):
    """Custom Allure шаг."""

    def __call__(self, func):
        """
        Call method.

        :param func: Function
        :return: Decorator
        """

        @functools.wraps(func)
        def impl(*args: Any, **kwargs: Any) -> Any:  # noqa: WPS430
            formatter_args = [represent(arg) for arg in args]
            formatter_params = func_parameters(func, *args, **kwargs)
            with StepContext(
                self.title.format(*formatter_args, **formatter_params),
                formatter_params,
            ):
                try:
                    return func(*args, **kwargs)  # noqa: WPS220
                except Exception as _ex:  # noqa: WPS122
                    page = args[0]  # noqa: WPS220
                    self._set_image(page.driver)  # noqa: WPS220
                    self._set_page_source(page.driver)  # noqa: WPS220
                    raise _ex  # noqa: WPS121, WPS220

        return impl

    def _set_image(self, driver: Any) -> None:
        """
        Attaching an image to an allure report.

        :param driver: browser driver
        """
        attach.file(
            source=driver.save_screenshot(),
            attachment_type=AttachmentType.PNG,
        )

    def _set_page_source(self, driver: Any) -> None:
        """
        Attaching the page source code to an allure report.

        :param driver: browser driver
        """
        attach(
            str(driver.driver.page_source),
            attachment_type=AttachmentType.HTML,
        )
        attach(
            str(driver.driver.page_source),
            attachment_type=AttachmentType.TEXT,
        )


def step(text: str) -> CustomStepContext:
    """
    Custom step Allure.

    :param text: Title
    :return: Instance of the step class
    """
    return CustomStepContext(text, {})


def allure_wrapper(
    allure_title: str,
    allure_suite: str,
    allure_parent_suite: str,
    test_case_id: int,
) -> Any:
    """
    Decorator for working with Allure.

    :param allure_title: Name of the test
    :param allure_suite: Folder name
    :param allure_parent_suite: Name of the parent folder
    :param test_case_id: Testcase id
    :return: Function
    """

    def decorator_function(func: Any) -> Any:  # noqa: WPS430
        @title(allure_title)
        @suite(allure_suite)
        @parent_suite(allure_parent_suite)
        @link(
            url="Link to the manual case",
            name="Link to the manual case",
        )
        def wrapper_func(*args: Any, **kwargs: Any) -> Any:  # noqa: WPS430
            return func(*args, **kwargs)

        return functools.update_wrapper(wrapper_func, func)

    return decorator_function
