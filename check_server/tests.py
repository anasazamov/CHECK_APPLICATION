from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.utils.timezone import now
from .tasks import manitor_server
from .models import Server, Application, Alert


class TestManitorServerTask(TestCase):
    def setUp(self):

        self.server = Server.objects.create(
            name="Test Server",
            ipv4="127.0.0.1",
            username="linux",
            password="242000",
            ssh_port=22,
        )
        self.application = Application.objects.create(
            server=self.server,
            name_run_on_server="nginx",
            port=80,
        )
        self.alert = Alert.objects.create(
            application=self.application,
            time=now()
        )

    @patch("check_server.check_functions.is_server_alive", return_value=False)
    @patch("check_server.send_telegram_notifacation.send_alert_with_file")
    def test_server_down_alert(self, mock_send_alert, mock_is_server_alive):

        manitor_server()

        alert = Alert.objects.filter(server=self.server).first()


        mock_send_alert.send_alert_with_file(
            "127.0.0.1", "Server is Test Server"
        )

    @patch("check_server.check_functions.is_server_alive", return_value=True)
    @patch("check_server.check_functions.is_port_open", return_value=False)
    @patch("check_server.connect_server.ssh_connect")
    @patch("check_server.get_log.get_logs", return_value="Sample logs")
    @patch("check_server.send_telegram_notifacation.send_alert_with_file")
    def test_application_down_alert(
        self, mock_send_alert, mock_get_logs, mock_ssh_connect, mock_is_port_open, mock_is_server_alive
    ):

        ssh_mock = MagicMock()
        mock_ssh_connect.return_value = ssh_mock

        manitor_server()

        alert = Alert.objects.filter(application=self.application).first()
        self.assertIsNotNone(alert)

        mock_send_alert.send_alert_with_file(
            "127.0.0.1", "nginx", "Sample logs", 80
        )

        print(f"get_logs chaqiruvlari: {mock_get_logs.call_args}")
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
        ssh_mock.exec_command.return_value = (MagicMock(), MagicMock(), MagicMock())  # stdin, stdout, stderr
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
