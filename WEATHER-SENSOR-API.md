# Weather Sensor API Documentation

## Overview

The Weather Sensor API provides endpoints for managing Bond Weather Sensors (model BWS-1000) in the Bond Bridge ecosystem. Weather Sensors detect environmental conditions (wind, rain, sun intensity) and can trigger automated actions on connected devices.

## Architecture

In the Bond architecture, Weather Sensors are considered a type of "Sidekick" - a Bond product capable of commanding devices through the Bridge. This is why Weather Sensor endpoints appear under the `/sidekicks/{ws_id}` path tree.

## Base URL

All Weather Sensor endpoints are located under:
```
/v2/sidekicks/{ws_id}
```

Where `{ws_id}` is the Weather Sensor ID (e.g., "WEAXX12345").

## API Endpoints

### 1. Weather Sensor Management

#### Create Weather Sensor
- **POST** `/v2/sidekicks`
- **Description**: Add a Weather Sensor to Bridge
- **Request Body**: WeatherSensor object with required `_id` field
- **Response**: 201 Created

#### Get Weather Sensor
- **GET** `/v2/sidekicks/{ws_id}`
- **Description**: Get information about a specific Weather Sensor
- **Response**: 200 OK with WeatherSensor object

#### Update Weather Sensor
- **PATCH** `/v2/sidekicks/{ws_id}`
- **Description**: Modify Weather Sensor metadata and event links
- **Request Body**: Partial WeatherSensor object
- **Response**: 200 OK

#### Delete Weather Sensor
- **DELETE** `/v2/sidekicks/{ws_id}`
- **Description**: Remove a Weather Sensor from the Bridge
- **Response**: 204 No Content

### 2. Properties Management

#### Get Properties
- **GET** `/v2/sidekicks/{ws_id}/properties`
- **Description**: Get current Weather Sensor configuration
- **Response**: 200 OK with Properties object

#### Update Properties
- **PATCH** `/v2/sidekicks/{ws_id}/properties`
- **Description**: Modify detection thresholds and enable/disable features
- **Response**: 200 OK with updated Properties object

### 3. State Monitoring

#### Get State
- **GET** `/v2/sidekicks/{ws_id}/state`
- **Description**: Get current sensor measurements and status
- **Response**: 200 OK with State object

### 4. Testing

#### Test Event
- **PUT** `/v2/sidekicks/{ws_id}/test`
- **Description**: Simulate weather events to trigger linked actions
- **Request Body**: Object with `event_name` ("wind", "rain", or "sun_high")
- **Response**: 200 OK

## Data Models

### WeatherSensor Object

| Field | Type | Description | Read/Write |
|-------|------|-------------|------------|
| `_id` | string | Weather Sensor ID (e.g., "WEAXX12345") | Write-only (POST) |
| `name` | string | Display name for the sensor | R/W |
| `location` | string | Physical location description | R/W |
| `event_links` | object | Maps event numbers to device actions | R/W |
| `signal` | integer | Signal quality (1-100) | Read-only |
| `battery` | integer | Battery percentage (1-100) | Read-only |
| `model` | string | Model number (e.g., "BWS-1000") | Read-only |
| `type` | string | Always "weather_sensor" | Read-only |

### Event Links

Event links map weather events to device actions:

| Event Number | Event Type | Trigger Condition |
|--------------|------------|-------------------|
| 1 | Wind | Wind speed reaches configured threshold |
| 2 | Rain | Rain detection begins |
| 3 | Sun | Sun intensity reaches configured level |

Each event maps to an array of action objects:
```json
{
  "1": [
    {
      "device": "xxyyzzww",
      "action": "TurnOn"
    }
  ],
  "2": [
    {
      "device": "aabbccdd",
      "action": "SetPosition",
      "argument": 75
    }
  ]
}
```

### Properties Object

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `feature_wind` | boolean | Enable wind detection | true |
| `feature_rain` | boolean | Enable rain detection | true |
| `feature_sun` | boolean | Enable sun detection | true |
| `feature_wind_push` | boolean | Enable wind threshold push notifications | true |
| `wind_threshold_dms` | integer | Wind threshold in decimeters/second | - |
| `sun_threshold_level` | integer | Sun intensity threshold (1-8) | - |
| `wind_ignore` | boolean | Temporarily ignore wind detections | false |
| `wind_ignore_expiration` | integer | Seconds to ignore wind detections | - |

### State Object

#### Status Values
- `idle` - No active weather events
- `triggered_wind` - Wind threshold exceeded
- `triggered_rain` - Rain detected
- `triggered_sun_high` - Sun intensity threshold exceeded
- `triggered_wind_manual` - Manual wind trigger

#### Measurement Data

| Field | Type | Description | Units |
|-------|------|-------------|-------|
| `data_wind_speed_dms` | integer | Last wind speed measurement | decimeters/second |
| `data_rain_mmh` | integer | Rain rate | millimeters/hour |
| `data_sun_level` | integer | Sun intensity level | 1-8 scale |
| `data_temperature_dc` | integer | Temperature | deci-Celsius |
| `data_humidity_percent` | integer | Humidity | percentage (0-100) |
| `data_unixtime` | integer | Timestamp of last measurement | Unix timestamp |
| `is_raining` | boolean | Current rain status | - |

#### Battery Status

| Field | Type | Description |
|-------|------|-------------|
| `battery` | integer | Solar battery percentage (1-100) |
| `battery_2` | integer | Backup battery percentage (1-100) |
| `battery_voltage_dV` | integer | Solar battery voltage (decivolts) |
| `battery_2_voltage_dV` | integer | Backup battery voltage (decivolts) |

#### Status Flags

| Flag | Description |
|------|-------------|
| `status_flag_unstable` | Data rate lower than expected |
| `status_flag_no_data` | No data for >30 minutes |
| `status_flag_battery_low` | Solar battery low |
| `status_flag_battery_2_low` | Backup battery (AA) low |
| `status_flag_low_temperature` | Low temperature - external 12V supply recommended |

## Example Usage

### Adding a Weather Sensor

```bash
POST /v2/sidekicks
Content-Type: application/json

{
  "_id": "WEA001234",
  "name": "Garden Weather Station",
  "location": "Back Garden",
  "event_links": {
    "1": [
      {
        "device": "awning123",
        "action": "Close"
      }
    ],
    "2": [
      {
        "device": "window456",
        "action": "SetPosition",
        "argument": 0
      }
    ]
  }
}
```

### Configuring Detection Thresholds

```bash
PATCH /v2/sidekicks/WEA001234/properties
Content-Type: application/json

{
  "wind_threshold_dms": 100,
  "sun_threshold_level": 6,
  "feature_wind_push": true
}
```

### Getting Current Measurements

```bash
GET /v2/sidekicks/WEA001234/state

Response:
{
  "status": "idle",
  "data_wind_speed_dms": 45,
  "data_rain_mmh": 0,
  "data_sun_level": 4,
  "data_temperature_dc": 225,
  "data_humidity_percent": 72,
  "is_raining": false,
  "battery": 85,
  "battery_2": 90
}
```

### Testing Wind Event

```bash
PUT /v2/sidekicks/WEA001234/test
Content-Type: application/json

{
  "event_name": "wind"
}
```

## Integration Notes

1. **Event Links**: When configuring event links, ensure referenced devices exist on the Bridge
2. **Signal Quality**: Signal strength updates don't trigger hash changes - poll explicitly if needed
3. **Battery Monitoring**: Monitor both solar and backup battery levels for reliability
4. **Temperature Considerations**: Low temperatures may require external 12V power supply
5. **Threshold Units**: 
   - Wind: decimeters/second (10 dm/s = 1 m/s)
   - Rain: millimeters/hour
   - Temperature: deci-Celsius (225 = 22.5°C)

## Error Responses

All endpoints follow standard HTTP status codes:
- **400** Bad Request - Invalid request parameters
- **401** Unauthorized - Authentication required
- **404** Not Found - Weather Sensor not found
- **500** Internal Server Error - Server-side error