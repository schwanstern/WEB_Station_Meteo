from django.conf import settings
from influxdb_client import InfluxDBClient
import logging
import datetime

logger = logging.getLogger(__name__)

def get_client():
    """Returns an authenticated InfluxDB client."""
    try:
        # Check for missing settings
        if not settings.INFLUXDB_URL:
            logger.error("INFLUXDB_URL is not set.")
        if not settings.INFLUXDB_TOKEN:
            logger.error("INFLUXDB_TOKEN is not set.")
        if not settings.INFLUXDB_ORG:
            logger.error("INFLUXDB_ORG is not set.")
            
        return InfluxDBClient(
            url=settings.INFLUXDB_URL,
            token=settings.INFLUXDB_TOKEN,
            org=settings.INFLUXDB_ORG
        )
    except Exception as e:
        logger.error(f"Failed to initialize InfluxDBClient: {e}")
        # Log values (be careful with token in prod, but needed for debug now)
        logger.error(f"Config: URL={settings.INFLUXDB_URL}, ORG={settings.INFLUXDB_ORG}, TOKEN={'*' * 5 if settings.INFLUXDB_TOKEN else 'None'}")
        raise e


def check_connection():
    """Simple ping to check InfluxDB connection."""
    try:
        client = get_client()
        return client.ping()
    except:
        return False

def query_measurements(measurement="ttn_uplink_student", duration="1h"):
    """
    Query metrics for a specific duration from ttn_uplink_student.
    duration examples: '1h', '24h', '7d'.
    """
    client = get_client()
    query_api = client.query_api()
    bucket = settings.INFLUXDB_BUCKET
    
    # Map duration to valid Flux duration if needed, or pass directly if format matches
    # InfluxQL '7d' works in Flux too.
    
    query = f'''
    from(bucket: "{bucket}")
      |> range(start: -{duration})
      |> filter(fn: (r) => r["_measurement"] == "{measurement}")
      |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
      |> drop(columns: ["_start", "_stop"])
    '''
    
    try:
        # query_data_frame might be easier if pandas is available, but let's return dict list to match old behavior
        result = query_api.query(query)
        points = []
        for table in result:
            for record in table.records:
                # Convert record to dict compatible with old get_points()
                # Old format: {'time': '...', 'temperature': 12, ...}
                point = record.values
                # Rename _time to time
                point['time'] = point.pop('_time')
                # Remove internal flux columns if they persist
                for k in list(point.keys()):
                    if k.startswith('_') or k in ['result', 'table']:
                         pass # actually pivot removes _measurement field usage usually, but let's keep clean
                
                # record.values contains all columns after pivot
                # We need to make sure we return a clean dict
                clean_point = {k: v for k, v in point.items() if k not in ['result', 'table', '_start', '_stop', '_measurement']}
                # Ensure time is string ISO format if expected by consumer, or keep datetime
                # The consumer `core/services.py` does: dt_str = p.get('time', '') ... datetime.strptime(..., "%Y-%m-%dT%H:%M:%SZ")
                # Flux returns datetime object. We might need to convert back to string OR fix consumer.
                # Adapting consumer is better but let's try to maintain contract first.
                if isinstance(clean_point.get('time'), datetime.datetime):
                    clean_point['time'] = clean_point['time'].strftime("%Y-%m-%dT%H:%M:%SZ")
                
                points.append(clean_point)
                
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
    query_api = client.query_api()
    bucket = settings.INFLUXDB_BUCKET
    
    query = f'''
    from(bucket: "{bucket}")
      |> range(start: -1y)
      |> filter(fn: (r) => r["_measurement"] == "ttn_uplink_student")
      |> last()
      |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    '''
    
    try:
        result = query_api.query(query)
        points = []
        for table in result:
            for record in table.records:
                 point = record.values
                 point['time'] = point.pop('_time')
                 clean_point = {k: v for k, v in point.items() if k not in ['result', 'table', '_start', '_stop', '_measurement']}
                 if isinstance(clean_point.get('time'), datetime.datetime):
                    clean_point['time'] = clean_point['time'].strftime("%Y-%m-%dT%H:%M:%SZ")
                 points.append(clean_point)
        
        if points:
            return points[0]
        return None
    except Exception as e:
        logger.error(f"Error fetching latest data: {e}")
        return None
