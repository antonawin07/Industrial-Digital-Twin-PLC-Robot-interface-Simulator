 Industrial PLC Simulator

A professional-grade HTTP-based PLC simulator with **295+ realistic industrial tags** for testing industrial automation applications, SCADA systems, and PLC monitoring tools.

 Features

- **HTTP REST API** for easy integration
- **295+ Realistic Industrial Tags** across 12 process areas
- **Industry-standard naming conventions** (ISA-88, Allen-Bradley)
- **Complete data type support** (SINT, INT, DINT, REAL, BOOL, SSTRING, STRING)
- **Dynamic process simulation** with realistic behaviors
- **Cross-platform** - runs on Windows, Linux, macOS
- **Zero Dependencies** - uses only Python standard library
- **CORS Support** for web applications

 Quick Start

### Installation

```bash
git clone https://github.com/Digital-Energy/industrial-plc-simulator.git
cd industrial-plc-simulator
python industrial_plc_simulator.py
```

The server will start on `http://localhost:8001`

Basic Usage

```bash
# Start the simulator
python industrial_plc_simulator.py

# Get all available tags (295+)
curl http://localhost:8001/tags

# Read reactor system tags
curl "http://localhost:8001/read?tags=R0101_TIC_2101_PV,R0101_PIC_2103_PV,R0101_LIC_2104_PV"

# Get tags organized by plant areas
curl http://localhost:8001/areas

# Monitor alarms
curl http://localhost:8001/alarms
```

## 📊 Process Areas & Tags

| Area | Prefix | Tag Count | Description |
|------|--------|-----------|-------------|
| **Area 100** | R01xx | 35+ | Reactor Systems (Primary & Secondary) |
| **Area 200** | P02xx | 40+ | Pump Systems (Centrifugal, PD, Circulation) |
| **Area 300** | CV03xx, ESD, MOV | 25+ | Valve Systems (Control, Emergency, Motor) |
| **Area 400** | HX04xx, AC04xx | 15+ | Heat Exchanger Systems |
| **Area 500** | T05xx | 20+ | Distillation Column Systems |
| **Area 600** | GC06xx, MS06xx, PH06xx | 20+ | Analyzer Systems |
| **Area 700** | AIR, STEAM, CW, ELEC | 30+ | Utility Systems |
| **Area 800** | SIS, GAS_DETECT, FIRE | 15+ | Safety Instrumented Systems |
| **Area 900** | PROD, QC, OEE | 25+ | Production & Batch Systems |
| **Area 1000** | ALARM, SYSTEM | 15+ | Alarm & Status Systems |
| **Area 1100** | WEATHER, ENV | 10+ | Environmental Monitoring |
| **Area 1200** | SCADA, COMM | 10+ | SCADA & Communication |

**Total: 295+ Industrial Tags**

 API Endpoints

 GET /tags
Returns all available PLC tags with their data types and current values.

**Response:**
```json
{
  "tags": [
    {
      "name": "R0101_TIC_2101_PV",
      "type": "REAL",
      "value": 348.5
    },
    {
      "name": "P0201_M_SPEED_ACTUAL",
      "type": "REAL", 
      "value": 1750.0
    }
  ],
  "total_tags": 295,
  "status": "Success"
}
```

 GET /read?tags=TAG1,TAG2,TAG3
Read current values for specified tags.

**Example:**
```bash
curl "http://localhost:8001/read?tags=R0101_TIC_2101_PV,P0201_M_SPEED_ACTUAL,CV0301_POSITION_FB"
```

**Response:**
```json
{
  "values": {
    "R0101_TIC_2101_PV": {
      "value": 348.5,
      "type": "REAL",
      "quality": "GOOD",
      "timestamp": "2025-07-30T21:30:00.000000"
    }
  },
  "status": "Success"
}
```

 GET /areas
Returns tags organized by plant areas.

 GET /alarms
Returns current alarm status and alarm summary.

POST /write
Write tag values (JSON body):
```json
{
  "R0101_TIC_2101_SP": 355.0,
  "CV0301_POSITION_CMD": 60.0
}
```
 Industrial Process Simulation

### Advanced Features
- **Dynamic Tag Values**: Real-time simulation with process dynamics
- **Temperature Cycling**: Realistic first-order temperature responses
- **Flow Calculations**: Based on pump speed and valve positions
- **Batch Progress**: Time-based production simulation
- **Equipment Health**: Vibration and temperature monitoring
- **Process Interactions**: Tags that influence each other realistically

 Equipment Coverage

 Reactor Systems (Area 100)
- Primary Reactor R-101 with full instrumentation
- Temperature, Pressure, Level, Flow control loops
- Agitator systems with VFD control
- pH and Conductivity monitoring
- Safety systems (PSV, Rupture Discs, E-Stop)

 Pump Systems (Area 200)
- Centrifugal Feed Pump P-201 with full diagnostics
- Motor parameters (Current, Voltage, Power, Torque)
- VFD status and fault codes
- Vibration monitoring (X, Y, Z axes)
- Bearing temperature monitoring
- Cavitation detection

 Valve Systems (Area 300)
- Control Valves with position feedback
- Emergency Shutdown Valves (ESD)
- Motor Operated Valves (MOV)
- Pneumatic actuator pressure
- Travel limit switches

 Safety Systems (Area 800)
- Safety Instrumented System (SIS)
- Gas Detection (H2S, LEL, O2, CO)
- Fire Detection and Suppression
- Emergency trip systems

 Production Systems (Area 900)
- Batch control with ISA-88 states
- Recipe management with versions
- Production rates and totals
- Quality control parameters
- Overall Equipment Effectiveness (OEE)

 Integration Examples

Python Integration
```python
import requests

# Get all tags
response = requests.get('http://localhost:8001/tags')
tags = response.json()['tags']

# Read specific values
response = requests.get('http://localhost:8001/read?tags=R0101_TIC_2101_PV,P0201_M_SPEED_ACTUAL')
values = response.json()['values']
print(f"Reactor Temperature: {values['R0101_TIC_2101_PV']['value']}°C")
```

 JavaScript/Web Integration
```javascript
// Fetch all tags
fetch('http://localhost:8001/tags')
  .then(response => response.json())
  .then(data => console.log('Available tags:', data.total_tags));

// Read tag values
fetch('http://localhost:8001/read?tags=R0101_TIC_2101_PV,P0201_M_SPEED_ACTUAL')
  .then(response => response.json())
  .then(data => console.log('Tag values:', data.values));
```

 Use Cases

- **Development & Testing** - Test PLC applications without hardware
- **CI/CD Pipelines** - Automated testing of industrial software
- **Training & Education** - Learn PLC communication protocols
- **Rapid Prototyping** - Quick development of HMI/SCADA applications
- **Demo Environments** - Showcase industrial automation solutions
- **Integration Testing** - Validate communication with PLC monitoring tools

 Requirements

- **Python 3.6+**
- **No additional dependencies** - uses only Python standard library

 Integration Partners

Designed to work seamlessly with:
- **SCADA Systems** - Industrial HMI/SCADA applications
- **PLC Monitoring Tools** - SignalTap, FactoryTalk, etc.
- **Allen-Bradley Communication Libraries** - pylogix and other bindings
- **OPC Clients** - through HTTP REST interface
- **Custom Automation Tools** - via simple HTTP API
- **Web Applications** - with CORS support

 License

MIT License - See [LICENSE](LICENSE) file for details.

 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


⚠️ **Note**: This is a simulation tool for development and testing purposes. Do not use in production environments with real industrial equipment.

**Digital Energy Services** | www.digitalenergyservices.ca | **Industrial Automation Testing Platform**
