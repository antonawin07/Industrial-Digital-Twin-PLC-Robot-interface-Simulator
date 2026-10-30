# Process Areas & Tag Database

## Overview

The Industrial PLC Simulator contains **295+ realistic industrial tags** organized across 12 major process areas, providing comprehensive coverage of a typical petrochemical or manufacturing plant.

## 🏭 Process Areas

### Area 100 - Reactor Systems
**35+ Tags | Primary Process Control**

Main production reactors with complete instrumentation packages:

#### Primary Reactor R-101
- **Temperature Control**: TIC-2101 with PV, SP, OUT, transmitter status
- **Jacket Temperature**: TIC-2102 for thermal management
- **Pressure Control**: PIC-2103 with high/high-high alarms
- **Level Control**: LIC-2104 with high/low alarms
- **Agitator System**: Speed control, torque, power, current monitoring
- **Process Analytics**: pH control, conductivity monitoring
- **Safety Systems**: PSV, rupture disc, emergency stops

#### Secondary Reactor R-102
- Complete secondary reactor instrumentation
- Independent control loops for temperature, pressure, level
- Agitator monitoring and control

**Sample Tags:**
- `R0101_TIC_2101_PV` - Reactor Temperature (°C)
- `R0101_PIC_2103_PV` - Reactor Pressure (psig)
- `R0101_LIC_2104_PV` - Reactor Level (%)
- `R0101_AGIT_SPEED_PV` - Agitator Speed (RPM)

### Area 200 - Pump Systems  
**40+ Tags | Rotating Equipment**

Complete pump monitoring with motor diagnostics:

#### Feed Pump P-201 (Centrifugal)
- **Motor Control**: Run commands, status, speed control
- **Electrical Monitoring**: 3-phase current, voltage, power, efficiency
- **VFD Integration**: Ready status, fault codes, warnings
- **Vibration Monitoring**: X, Y, Z axis measurements
- **Thermal Monitoring**: Drive/non-drive end bearing temperatures
- **Mechanical Systems**: Seal pressure, flow rate, pressures
- **Performance**: Pump efficiency, cavitation detection

#### Additional Pumps
- **P-202**: Positive displacement transfer pump
- **P-203**: Circulation pump with head monitoring

**Sample Tags:**
- `P0201_M_SPEED_ACTUAL` - Motor Speed (RPM)
- `P0201_M_CURRENT_A` - Motor Current Phase A (A)
- `P0201_VIBRATION_X` - Vibration X-axis (mm/s)
- `P0201_FLOW_RATE` - Pump Flow Rate (GPM)

### Area 300 - Valve Systems
**25+ Tags | Flow Control**

Comprehensive valve monitoring and control:

#### Control Valves
- **CV-301**: Feed control valve with positioner feedback
- **CV-302**: Product control valve
- Position commands, feedback, deviation monitoring
- Travel limit switches, actuator pressure
- Flow coefficient calculation

#### Emergency Shutdown Valves
- **ESD-301/302/303**: Safety shutdown valves
- Open/closed status, fault monitoring

#### Motor Operated Valves
- **MOV-301**: Block valve control
- Torque monitoring, motor current

**Sample Tags:**
- `CV0301_POSITION_FB` - Valve Position Feedback (%)
- `ESD_0301_OPEN_STATUS` - ESD Valve Status
- `MOV_0301_TORQUE_ACTUAL` - MOV Torque (%)

### Area 400 - Heat Exchanger Systems
**15+ Tags | Thermal Management**

Heat transfer equipment monitoring:

#### Shell & Tube Heat Exchanger HX-401
- Tube side: inlet/outlet temperatures, pressure, flow
- Shell side: inlet/outlet temperatures, pressure, flow
- Performance monitoring: fouling factor, overall U, LMTD, effectiveness

#### Air Cooler AC-402
- Process side: inlet/outlet temperatures
- Cooling system: dual fan operation, speeds
- Environmental: ambient temperature

**Sample Tags:**
- `HX0401_TUBE_INLET_TEMP` - HX Tube Inlet (°F)
- `AC0402_FAN_1_STATUS` - Air Cooler Fan Status

### Area 500 - Distillation Column Systems
**20+ Tags | Separation Processes**

Multi-tray distillation tower T-501:

#### Temperature Profile
- **Tray Temperatures**: 5 measurement points from top to bottom
- Temperature gradient monitoring

#### Pressure Control
- Top/bottom pressure monitoring
- Differential pressure calculation

#### Reflux System
- Flow control, ratio control, temperature
- Reflux drum level monitoring

#### Reboiler System
- Heat duty monitoring, temperature control
- Reboiler level monitoring

#### Product Streams
- Distillate and bottoms flow rates
- Feed stream monitoring

**Sample Tags:**
- `T0501_TRAY_01_TEMP` - Top Tray Temperature (°F)
- `T0501_REFLUX_RATIO` - Reflux Ratio
- `T0501_REBOILER_DUTY` - Heat Duty (kW)

### Area 600 - Analyzer Systems
**20+ Tags | Process Analytics**

Online process analyzers:

#### Gas Chromatograph GC-601
- **Multi-component Analysis**: H2, O2, N2, CO2, CH4, Ethane
- Sample validity, analysis time
- System status, calibration due flags
- Carrier gas pressure, column temperature

#### Mass Spectrometer MS-602
- Molecular weight determination
- Product purity analysis
- Impurity level monitoring

#### pH Analyzer PH-603
- pH measurement with temperature compensation
- Auto-clean system status

#### Conductivity Analyzer COND-604
- Conductivity measurement with cell constant

**Sample Tags:**
- `GC0601_H2_PERCENT` - Hydrogen Concentration (%)
- `MS0602_PURITY_PERCENT` - Product Purity (%)
- `PH0603_VALUE` - pH Value

### Area 700 - Utility Systems
**30+ Tags | Plant Infrastructure**

Essential plant utilities:

#### Compressed Air System
- **Compressor 701**: Load, pressures, temperatures
- Motor monitoring, vibration, runtime hours
- Air header pressure, dryer dewpoint

#### Steam System
- Header pressure and temperature
- Flow rate monitoring
- Condensate return temperature
- Boiler load and efficiency

#### Cooling Water System
- Supply/return temperatures and pressures
- Flow rate monitoring
- Cooling tower fan operation
- Makeup water flow

#### Electrical System
- **3-Phase Monitoring**: Voltages, currents, frequency
- Power factor, kW/kVAR demand
- Total kWh consumption

**Sample Tags:**
- `AIR_COMP_701_DISCHARGE_PRESSURE` - Air Pressure (psig)
- `STEAM_HEADER_PRESSURE` - Steam Pressure (psig)
- `ELEC_KW_DEMAND` - Electrical Demand (kW)

### Area 800 - Safety Instrumented Systems
**15+ Tags | Process Safety**

Critical safety systems:

#### Emergency Shutdown System
- Reactor trip, high pressure/temperature trips
- Gas detection trip, fire detection trip
- System health monitoring, bypass status

#### Gas Detection System
- **Multi-gas Monitoring**: H2S, LEL, O2, CO
- Detection limits and alarm levels

#### Fire Detection System
- Zone-based fire detection
- Fire suppression system ready status

**Sample Tags:**
- `SIS_SYSTEM_HEALTHY` - SIS Health Status
- `GAS_DETECT_H2S_PPM` - H2S Detection (ppm)
- `FIRE_DETECT_ZONE_1` - Fire Zone 1 Status

### Area 900 - Production & Batch Systems
**25+ Tags | Manufacturing Execution**

Production tracking and batch control:

#### Batch Control (ISA-88 Compliant)
- Batch number, recipe name/version
- Batch state, phase, step tracking
- Target vs actual quantities
- Batch completion percentage

#### Production Metrics
- Hourly/daily/monthly production rates
- Process yield calculations

#### Quality Control
- Sample tracking, laboratory results
- Moisture, density, viscosity, color
- Product release status

#### Overall Equipment Effectiveness (OEE)
- Availability, performance, quality rates
- Overall OEE calculation

**Sample Tags:**
- `PROD_BATCH_NUMBER` - Current Batch
- `PROD_HOURLY_RATE` - Production Rate (kg/hr)
- `OEE_OVERALL` - Overall OEE (%)

### Area 1000 - Alarm & Status Systems
**15+ Tags | System Monitoring**

Plant-wide monitoring:

#### Alarm Management
- Alarm counts by priority level
- Acknowledged vs unacknowledged alarms
- Total active alarms

#### System Status
- Operator counts, HMI connections
- Historian and backup system status
- UPS system monitoring

**Sample Tags:**
- `ALARM_COUNT_TOTAL` - Total Active Alarms
- `SYSTEM_UPS_BATTERY_PERCENT` - UPS Battery (%)

### Area 1100 - Environmental Monitoring
**10+ Tags | Environmental Compliance**

Environmental and weather monitoring:

#### Weather Station
- Temperature, humidity, barometric pressure
- Wind speed/direction, rainfall

#### Environmental Monitoring
- Noise levels, dust levels
- Emissions monitoring (SO2, NOx, CO)

**Sample Tags:**
- `WEATHER_TEMP_AMBIENT` - Ambient Temperature (°F)
- `ENV_NOISE_LEVEL` - Noise Level (dB)

### Area 1200 - SCADA & Communication Systems
**10+ Tags | Information Systems**

Plant information systems:

#### SCADA System
- System online status, communication health
- User sessions, data rates
- Network latency monitoring

#### Communication Infrastructure
- Ethernet, serial port status
- Wireless signal strength

**Sample Tags:**
- `SCADA_SYSTEM_STATUS` - SCADA Online Status
- `COMM_ETHERNET_STATUS` - Network Status

## Legacy Compatibility

**Additional Tags** - For backward compatibility:
- `TEMPERATURE`, `PRESSURE`, `STATUS` - Basic legacy tags
- `SCADA[0-9]` - Legacy SCADA array elements

## Dynamic Simulation

All tags feature realistic dynamic behavior:
- **Temperature cycling** with first-order responses
- **Pump ramp-up** with acceleration curves  
- **Flow calculations** based on pump speed and valve positions
- **Batch progress** with time-based advancement
- **Equipment health** monitoring with realistic variations
- **Process interactions** between related tags

This comprehensive tag database provides an ultra-realistic testing environment for industrial automation applications, SCADA systems, and PLC communication tools.