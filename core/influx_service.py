from django.conf import settings
from influxdb_client import InfluxDBClient
import logging
import datetime

logger = logging.getLogger(__name__)

def get_client():
    """Returns an authenticated InfluxDB client."""
    return InfluxDBClient(
        host=settings.INFLUXDB_HOST,
        port=settings.INFLUXDB_PORT,
        username=settings.INFLUXDB_USER,
        password=settings.INFLUXDB_PASSWORD,
        database=settings.INFLUXDB_DB
    )

def query_measurements(measurement="ttn_uplink_student", duration="1h"):
    """
    Query metrics for a specific duration from ttn_uplink_student.
    duration examples: '1h', '24h', '7d'.
    """
    client = get_client()
    # InfluxQL for history
    query = f"SELECT * FROM \"{measurement}\" WHERE time > now() - {duration}"
    
    try:
        result = client.query(query)
        points = list(result.get_points())
        return points
    except Exception as e:
        logger.error(f"Error querying InfluxDB: {e}")
        return []

def get_latest_data():
    """
    Fetch the most recent data point.
    Measurement: ttn_uplink_student
    Fields: humidite, luminosite, pression, speed, temperature, dir
    """
    client = get_client()
    query = "SELECT * FROM \"ttn_uplink_student\" ORDER BY time DESC LIMIT 1"
    
    try:
        result = client.query(query)
        points = list(result.get_points())
        if points:
            return points[0]
        return None
    except Exception as e:
        logger.error(f"Error fetching latest data: {e}")
        return None
