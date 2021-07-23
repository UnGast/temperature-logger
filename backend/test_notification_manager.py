from notification_manager import RiseAboveNotificationConfig, SystemStartNotificationConfig, NotificationManager

class MockEmailManager:
    def __init__(self, on_send):
        self.on_send = on_send

    def send_email(self, sender_address, receiver_address, subject, text):
        self.on_send()

class MockSensorManager:
    def __init__(self, sensor_values):
        self.sensor_values = sensor_values

    async def get_latest_values_filled_with_previous(self):
        return self.sensor_values

class MockGetTime:
    def __init__(self):
        self.time = 0

    def __call__(self):
        t = self.time
        self.time += 1
        return t

def test_rise_above_notification_config():
    config = RiseAboveNotificationConfig(
            get_time=MockGetTime(),
            sender_email='sender',
            receiver_email='receiver',
            message_subject='subject',
            message='message',
            check_interval=0,
            sensor_id=0,
            threshold=0,
            min_breach_duration=2
        )
    
    assert not config.check_signal({0: -1})
    assert not config.check_signal({0: -2})

    assert not config.check_signal({0: 0.01})
    assert config.check_signal({0: 0.01}) == True

    assert not config.check_signal({0: 1})
    assert not config.check_signal({0: -1})

    assert not config.check_signal({0: 1})
    assert config.check_signal({0: 1}) == True

def test_system_start_notification_config():
    config = SystemStartNotificationConfig(
            get_time=MockGetTime(),
            sender_email='sender',
            receiver_email='receiver',
            message_subject='subject',
            message='message',
            check_interval=1
        )

    assert config.check_signal({})
    assert not config.check_signal({})
    assert not config.check_signal({})

def test_notification_manager():
    configs = [
        RiseAboveNotificationConfig(
            get_time=MockGetTime(),
            sender_email='sender',
            receiver_email='receiver',
            message_subject='subject',
            message='message',
            check_interval=0,
            sensor_id=0,
            threshold=0,
            min_breach_duration=2
        ),
        SystemStartNotificationConfig(
            get_time=MockGetTime(),
            sender_email='sender',
            receiver_email='receiver',
            message_subject='subject',
            message='message',
            check_interval=1
        )
    ]

    emails_sent_count = 0

    mock_sensor_manager = MockSensorManager({0: -1})
    def on_send():
        nonlocal emails_sent_count
        emails_sent_count += 1
    mock_email_manager = MockEmailManager(on_send)
    notification_manager = NotificationManager(configs, mock_sensor_manager, mock_email_manager, MockGetTime())

    notification_manager.single_watch_step()
    assert emails_sent_count == 1

    notification_manager.single_watch_step()
    assert emails_sent_count == 1
    
    mock_sensor_manager.sensor_values = {0: 1}
    notification_manager.single_watch_step()
    assert emails_sent_count == 1

    notification_manager.single_watch_step()
    assert emails_sent_count == 2

    notification_manager.single_watch_step()
    assert emails_sent_count == 2

    notification_manager.single_watch_step()
    assert emails_sent_count == 2
