from dependency_injector import containers, providers

from services.chrome_headless import ChromeHeadlessService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    chrome_headless_service = providers.Factory(
        ChromeHeadlessService
    )
