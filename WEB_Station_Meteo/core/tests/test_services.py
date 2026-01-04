from django.test import TestCase
from core import services

class ServiceTests(TestCase):
    def test_get_sensor_data(self):
        data = services.get_sensor_data()
        self.assertIn("vent_vitesse", data)
        self.assertEqual(data["vent_vitesse"], 25)
        self.assertEqual(data["vent_dir"], "S")

    def test_get_alerts_logic_normal(self):
        # By default simulated wind is 25, which is > 15, so DANGER
        # We might need to mock get_sensor_data if we want to test other branches
        # primarily testing that it runs for now
        alerts = services.get_alerts_logic()
        self.assertTrue(len(alerts) > 0)
        self.assertEqual(alerts[0]["type"], "danger")

    def test_system_update(self):
        initial_state = services.get_system_state()
        initial_update = initial_state["update_available"]
        
        # Perform update
        services.update_system()
        
        new_state = services.get_system_state()
        self.assertFalse(new_state["update_available"])
        self.assertNotEqual(new_state["last_update"], "Jamais")
