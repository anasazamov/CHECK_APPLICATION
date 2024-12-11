import json
from unittest.mock import patch, MagicMock
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now
from .tasks import manitor_server
from .models import Server, Application, Alert, DockerApplication, Domain, Company


class TestManitorServerTask(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username="testuser", password="password")

        self.company = Company.objects.create(name="Test Company", chanel_id="12345")
        self.company.user.add(self.user)

        self.server = Server.objects.create(
            name="Test Server",
            ipv4="127.0.0.1",
            username="linux",
            password="242000",
            ssh_port=22,
            company=self.company
        )
        self.application = Application.objects.create(
            server=self.server,
            name_run_on_server="nginx",
            port=80,
            company=self.company
        )
        self.alert = Alert.objects.create(application=self.application, time=now())

    @patch("check_server.check_functions.is_server_alive", return_value=False)
    @patch("check_server.send_telegram_notifacation.send_alert_with_file")
    def test_server_down_alert(self, mock_send_alert, mock_is_server_alive):

        manitor_server()

        alert = Alert.objects.filter(server=self.server).first()

        mock_send_alert.send_alert_with_file("127.0.0.1", "Server is Test Server")

    @patch("check_server.check_functions.is_server_alive", return_value=True)
    @patch("check_server.check_functions.is_port_open", return_value=False)
    @patch("check_server.connect_server.ssh_connect")
    @patch("check_server.get_log.get_logs", return_value="Sample logs")
    @patch("check_server.send_telegram_notifacation.send_alert_with_file")
    def test_application_down_alert(
        self,
        mock_send_alert,
        mock_get_logs,
        mock_ssh_connect,
        mock_is_port_open,
        mock_is_server_alive,
    ):

        ssh_mock = MagicMock()
        mock_ssh_connect.return_value = ssh_mock

        manitor_server()

        alert = Alert.objects.filter(application=self.application).first()
        self.assertIsNotNone(alert)

        mock_send_alert.send_alert_with_file("127.0.0.1", "nginx", "Sample logs", 80)

        mock_get_logs.get_logs(ssh_mock, "nginx")

        mock_ssh_connect.ssh_connect("127.0.0.1", "linux", "242000", 22)

    @patch("check_server.check_functions.is_server_alive", return_value=True)
    @patch("check_server.check_functions.is_port_open", return_value=True)
    def test_no_alerts_when_all_ok(self, mock_is_port_open, mock_is_server_alive):

        manitor_server()

        alerts = Alert.objects.filter(server=self.server)
        self.assertEqual(alerts.count(), 0)

    @patch("check_server.check_functions.is_port_open", return_value=False)
    @patch("check_server.get_log.get_logs", return_value="Sample logs")
    @patch("check_server.connect_server.ssh_connect")
    def test_get_logs_on_application_failure(
        self, mock_ssh_connect, mock_get_logs, mock_is_port_open
    ):

        ssh_mock = MagicMock()
        ssh_mock.exec_command.return_value = (
            MagicMock(),
            MagicMock(),
            MagicMock(),
        )  # stdin, stdout, stderr
        mock_ssh_connect.return_value = ssh_mock

        manitor_server()

        mock_get_logs.return_value = "Sample logs"

        alert = Alert.objects.filter(application=self.application).first()
        self.assertIsNotNone(alert)

    @patch("check_server.check_functions.is_server_alive", return_value=True)
    def test_alert_does_not_duplicate(self, mock_is_server_alive):

        Alert.objects.create(server=self.server, time=now())

        manitor_server()

        alerts = Alert.objects.filter(server=self.server)
        self.assertEqual(alerts.count(), 1)


class UpdateDeleteViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

        # Test uchun Company yaratamiz
        self.company = Company.objects.create(name="Test Company", chanel_id="12345")
        self.company.user.add(self.user)

        # Server obyektini yaratishda company maydonini beramiz
        self.server = Server.objects.create(
            name="Test Server",
            ssh_port=2222,
            ipv4="127.0.0.1",
            username="root",
            password="password",
            company=self.company  # Bu maydon majburiy
        )

        # Application, DockerApplication va Domain obyektlarini yaratamiz
        self.app = Application.objects.create(
            name_run_on_server="Test App",
            port=8080,
            server=self.server,
            company=self.company
        )

        self.docker_app = DockerApplication.objects.create(
            name_run_on_docker="Docker App",
            container_name="container",
            port=9000,
            server=self.server,
            company=self.company
        )

        self.domain = Domain.objects.create(
            domain="example.com",
            server=self.server,
            company=self.company
        )


    def test_get_server(self):
        url = reverse("get-server", args=[self.server.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Test Server")

    def test_update_server(self):
        url = reverse("update-server", args=[self.server.id])
        data = {
            "name": "Updated Server",
            "ssh_port": 2222,
            "ipv4": "192.168.1.1",
            "username": "admin"
        }
        response = self.client.put(url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.server.refresh_from_db()
        self.assertEqual(self.server.name, "Test Server")
        self.assertEqual(self.server.ssh_port, 2222)

    def test_delete_server(self):
        url = reverse("update-server", args=[self.server.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Server.objects.filter(id=self.server.id).exists())

    def test_get_app(self):
        url = reverse("get-applications-info", args=[self.app.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name_run_on_server"], "Test App")

    def test_update_app(self):
        url = reverse("update-application", args=[self.app.id])
        data = {
            "name_run_on_server": "Updated App",
            "port": 9090
        }
        response = self.client.put(url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.app.refresh_from_db()
        self.assertEqual(self.app.name_run_on_server, "Updated App")
        self.assertEqual(self.app.port, 9090)

    def test_delete_app(self):
        url = reverse("update-application", args=[self.app.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Application.objects.filter(id=self.app.id).exists())

    def test_get_docker_info(self):
        url = reverse("get-docker-info", args=[self.docker_app.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name_run_on_docker"], "Docker App")

    def test_update_docker_app(self):
        url = reverse("update-docker-app", args=[self.docker_app.id])
        data = {
            "name_run_on_docker": "Updated Docker App",
            "container_name": "updated_container",
            "port": 9091
        }
        response = self.client.put(url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.docker_app.refresh_from_db()
        self.assertEqual(self.docker_app.name_run_on_docker, "Updated Docker App")
        self.assertEqual(self.docker_app.container_name, "updated_container")

    def test_delete_docker_app(self):
        url = reverse("update-docker-app", args=[self.docker_app.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(DockerApplication.objects.filter(id=self.docker_app.id).exists())

    def test_get_domain_info(self):
        url = reverse("get-domain", args=[self.domain.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["domain"], "example.com")

    def test_update_domain(self):
        url = reverse("update-domain", args=[self.domain.id])
        data = {
            "domain": "updated-example.com"
        }
        response = self.client.put(url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.domain.refresh_from_db()
        self.assertEqual(self.domain.domain, "updated-example.com")

    def test_delete_domain(self):
        url = reverse("update-domain", args=[self.domain.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Domain.objects.filter(id=self.domain.id).exists())
