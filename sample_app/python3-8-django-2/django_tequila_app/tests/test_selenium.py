import socket

from django.conf import settings
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


@override_settings(ALLOWED_HOSTS=['*'])  # Open ALLOW_HOSTS
@override_settings(DEBUG=True)
class SeleniumStaticLiveServerTestCase(StaticLiveServerTestCase):
    """
    Provides base test class which connects to the Docker
    container running Selenium.
    You can use a VNC client on localhost:5900 (password: secret)
    to get a view of the process
    """
    host = '0.0.0.0'  # Bind to 0.0.0.0 to allow external access

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set host to externally accessible web server address
        cls.host = socket.gethostbyname(socket.gethostname())

        cls.remote_selenium_address = getattr(settings, 'REMOTE_SELENIUM_SERVER', False)

        # Instantiate the remote WebDriver
        cls.selenium = webdriver.Remote(
            #  Set to: htttp://{selenium-container-name}:port/wd/hub
            #  In our example, the container is named `selenium`
            #  and runs on port 4444
            command_executor=cls.remote_selenium_address,
            # Set to CHROME since we are using the Chrome container
            desired_capabilities=DesiredCapabilities.CHROME,
        )
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        if cls.selenium:
            cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        """Open a new browser for each test."""
        super(SeleniumStaticLiveServerTestCase, self).setUp()

    def test_user_anonymous(self):
        self.selenium.get('%s%s' % (self.live_server_url,
                                    reverse('index')))

        self.assertTrue("AnonymousUser" in self.selenium.page_source, self.selenium.page_source)

    def test_user_allowed_to_access_a_protected_page(self):
        self.selenium.get('%s%s' % (self.live_server_url,
                                    reverse('unprotected')))

    def test_user_redirected_when_not_allowed(self):
        pass
        # TODO: set a mock for Tequila to test this part
        self.selenium.get('%s%s' % (self.live_server_url,
                                    reverse('protected')))

        WebDriverWait(self.selenium, 10).until(
            self.assertTrue("/login" in self.selenium.current_url)
        )
