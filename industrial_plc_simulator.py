#!/usr/bin/env python3
"""
Industrial PLC Simulator

A comprehensive HTTP-based PLC simulator for industrial automation testing.
Provides realistic industrial-grade tag simulation with proper naming conventions,
comprehensive data types, and industrial process control scenarios.

Features:
- 295+ realistic industrial tags across 12 process areas
- Industry-standard tag naming conventions (ISA-88, Allen-Bradley)
- Complete data type support (SINT, INT, DINT, REAL, BOOL, SSTRING, STRING)
- Realistic industrial process simulation with dynamics
- Multiple plant areas: Reactors, Pumps, Valves, Heat Exchangers, Distillation
- Temperature cycling and process dynamics
- Comprehensive alarm and status monitoring
- Production metrics, batch control, and quality systems
- Safety Instrumented Systems (SIS)
- Environmental monitoring and utilities

Author: Digital Energy Services
Website: www.digitalenergyservices.ca
License: MIT
"""

import socket
import threading
import struct
import json
import time
import math
import random
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class IndustrialPLCSimulator:
    """
    Comprehensive Industrial PLC Simulator with extensive tag simulation
    Based on real-world petrochemical, pharmaceutical, and manufacturing plants
    """
    
    def __init__(self, host='localhost', port=8001):
        self.host = host
        self.port = port
        self.running = False
        self.start_time = time.time()
        
        # Initialize comprehensive industrial tag database (295+ tags)
        self.tags = self._initialize_industrial_tags()
        
        # Tag metadata for descriptions and engineering units
        self.tag_metadata = self._initialize_tag_metadata()
        
        # Process simulation parameters
        self.process_params = {
            'reactor_temp_setpoint': 350.0,
            'pump_speed_setpoint': 1750.0,
            'process_pressure_setpoint': 45.0,
            'distillation_reflux_ratio': 3.5,
            'batch_progress': 0.0,
            'production_rate': 2500.0  # kg/hr
        }
        
        # Alarm counters
        self.alarm_counts = {
            'critical': 0,
            'high': 2,
            'medium': 5,
            'low': 12
        }
    
    def _initialize_industrial_tags(self):
        """Initialize comprehensive industrial tag database with 295+ realistic values"""
        tags = {}
        
        # =====================================================
        # AREA 100 - REACTOR SYSTEMS (Main Process)
        # =====================================================
        
        # Primary Reactor R-101
        tags.update({
            # Temperature Control Loops
            'R0101_TIC_2101_PV': 348.5,      # Reactor Temperature PV (°C)
            'R0101_TIC_2101_SP': 350.0,      # Temperature Setpoint
            'R0101_TIC_2101_OUT': 65.2,      # Controller Output %
            'R0101_TIC_2101_MODE': 'AUTO',   # Control Mode
            'R0101_TT_2101_EU': 348.5,       # Temperature Transmitter EU
            'R0101_TT_2101_RAW': 27384,      # Raw ADC value (4-20mA)
            'R0101_TT_2101_STATUS': True,    # Transmitter OK
            'R0101_TT_2101_FAULT': False,    # Transmitter Fault
            
            # Jacket Temperature Control
            'R0101_TIC_2102_PV': 285.2,      # Jacket Temperature PV
            'R0101_TIC_2102_SP': 290.0,      # Jacket Temperature SP
            'R0101_TIC_2102_OUT': 42.8,      # Jacket Controller Output
            
            # Pressure Control
            'R0101_PIC_2103_PV': 44.8,       # Reactor Pressure PV (psig)
            'R0101_PIC_2103_SP': 45.0,       # Pressure Setpoint
            'R0101_PIC_2103_OUT': 52.1,      # Pressure Controller Output
            'R0101_PT_2103_EU': 44.8,        # Pressure Transmitter EU
            'R0101_PT_2103_HIGH_ALARM': False, # High Pressure Alarm
            'R0101_PT_2103_HIHI_ALARM': False, # High-High Pressure
            
            # Level Control
            'R0101_LIC_2104_PV': 78.5,       # Reactor Level PV (%)
            'R0101_LIC_2104_SP': 80.0,       # Level Setpoint
            'R0101_LIC_2104_OUT': 45.2,      # Level Controller Output
            'R0101_LT_2104_HIGH_ALARM': False, # High Level Alarm
            'R0101_LT_2104_LOW_ALARM': False,  # Low Level Alarm
            
            # Agitator System
            'R0101_AGIT_SPEED_PV': 125.5,    # Agitator Speed (RPM)
            'R0101_AGIT_SPEED_SP': 130.0,    # Speed Setpoint
            'R0101_AGIT_TORQUE': 78.2,       # Agitator Torque (%)
            'R0101_AGIT_POWER': 45.8,        # Motor Power (kW)
            'R0101_AGIT_CURRENT': 89.5,      # Motor Current (A)
            'R0101_AGIT_RUN_STATUS': True,   # Agitator Running
            'R0101_AGIT_FAULT': False,       # Agitator Fault
            
            # pH Control
            'R0101_PH_PV': 7.25,             # pH Value
            'R0101_PH_SP': 7.5,              # pH Setpoint
            'R0101_PH_OUT': 35.2,            # pH Controller Output
            
            # Conductivity
            'R0101_COND_PV': 485.2,          # Conductivity (µS/cm)
            
            # Safety Systems
            'R0101_PSV_2105_OPEN': False,    # Pressure Safety Valve
            'R0101_RUPTURE_DISC_OK': True,   # Rupture Disc Status
            'R0101_EMERGENCY_STOP': False,   # Emergency Stop
        })
        
        # Secondary Reactor R-102
        tags.update({
            'R0102_TIC_2201_PV': 298.7,      # R-102 Temperature
            'R0102_TIC_2201_SP': 300.0,
            'R0102_TIC_2201_OUT': 58.9,
            'R0102_PIC_2202_PV': 25.4,       # R-102 Pressure
            'R0102_PIC_2202_SP': 25.0,
            'R0102_LIC_2203_PV': 65.8,       # R-102 Level
            'R0102_LIC_2203_SP': 70.0,
            'R0102_AGIT_SPEED_PV': 98.5,     # R-102 Agitator
            'R0102_AGIT_RUN_STATUS': True,
        })
        
        # =====================================================
        # AREA 200 - PUMP SYSTEMS
        # =====================================================
        
        # Feed Pump P-201 (Centrifugal)
        tags.update({
            'P0201_M_RUN_CMD': False,        # Motor Run Command
            'P0201_M_RUN_STATUS': False,     # Motor Running Status
            'P0201_M_SPEED_ACTUAL': 1750.0,  # Actual Motor Speed (RPM)
            'P0201_M_SPEED_SETPOINT': 1750.0, # Speed Setpoint
            'P0201_M_CURRENT_A': 45.2,       # Motor Current Phase A
            'P0201_M_CURRENT_B': 46.1,       # Motor Current Phase B
            'P0201_M_CURRENT_C': 44.8,       # Motor Current Phase C
            'P0201_M_VOLTAGE_AB': 478.5,     # Line Voltage AB
            'P0201_M_VOLTAGE_BC': 479.2,     # Line Voltage BC
            'P0201_M_VOLTAGE_CA': 478.9,     # Line Voltage CA
            'P0201_M_POWER': 37.5,           # Motor Power (kW)
            'P0201_M_TORQUE': 78.5,          # Motor Torque (%)
            'P0201_M_EFFICIENCY': 94.2,      # Motor Efficiency (%)
            'P0201_VFD_READY': True,         # VFD Ready Status
            'P0201_VFD_FAULT_CODE': 0,       # VFD Fault Code
            'P0201_VFD_WARNING_CODE': 0,     # VFD Warning Code
            'P0201_VIBRATION_X': 2.1,        # Vibration X-axis (mm/s)
            'P0201_VIBRATION_Y': 1.8,        # Vibration Y-axis
            'P0201_VIBRATION_Z': 2.3,        # Vibration Z-axis
            'P0201_BEARING_TEMP_DE': 65.2,   # Drive End Bearing Temp
            'P0201_BEARING_TEMP_NDE': 62.8,  # Non-Drive End Bearing
            'P0201_SEAL_PRESSURE': 15.2,     # Mechanical Seal Pressure
            'P0201_FLOW_RATE': 245.8,        # Pump Flow Rate (GPM)
            'P0201_DISCHARGE_PRESSURE': 85.2, # Discharge Pressure (psig)
            'P0201_SUCTION_PRESSURE': 5.2,   # Suction Pressure (psig)
            'P0201_DIFFERENTIAL_PRESSURE': 80.0, # Differential Pressure
            'P0201_EFFICIENCY': 76.5,        # Pump Efficiency (%)
            'P0201_CAVITATION_ALARM': False, # Cavitation Detected
        })
        
        # Transfer Pump P-202 (Positive Displacement)
        tags.update({
            'P0202_M_RUN_STATUS': True,      # P-202 Running
            'P0202_M_SPEED_ACTUAL': 850.0,   # P-202 Speed
            'P0202_M_CURRENT': 28.5,         # P-202 Current
            'P0202_FLOW_RATE': 125.4,        # P-202 Flow Rate
            'P0202_DISCHARGE_PRESSURE': 125.8, # P-202 Discharge Pressure
            'P0202_PULSATION_DAMPENER_PRESSURE': 120.5, # Pulsation Dampener
        })
        
        # Circulation Pump P-203
        tags.update({
            'P0203_M_RUN_STATUS': True,
            'P0203_M_SPEED_ACTUAL': 1450.0,
            'P0203_FLOW_RATE': 850.2,
            'P0203_HEAD': 45.2,              # Pump Head (ft)
        })
        
        # =====================================================
        # AREA 300 - VALVE SYSTEMS
        # =====================================================
        
        # Control Valve CV-301 (Feed Control)
        tags.update({
            'CV0301_POSITION_CMD': 50.0,     # Valve Position Command (%)
            'CV0301_POSITION_FB': 49.8,      # Position Feedback
            'CV0301_POSITION_DEVIATION': 0.2, # Position Deviation
            'CV0301_OPEN_STATUS': False,     # Fully Open Status
            'CV0301_CLOSED_STATUS': False,   # Fully Closed Status
            'CV0301_TRAVEL_LIMIT_SWITCH_OPEN': False, # Travel Limit Open
            'CV0301_TRAVEL_LIMIT_SWITCH_CLOSED': False, # Travel Limit Closed
            'CV0301_ACTUATOR_PRESSURE': 18.5, # Pneumatic Actuator Pressure
            'CV0301_POSITIONER_SETPOINT': 50.0, # Valve Positioner SP
            'CV0301_POSITIONER_FEEDBACK': 49.8, # Positioner Feedback
            'CV0301_FLOW_COEFFICIENT': 125.8, # Cv Flow Coefficient
        })
        
        # Control Valve CV-302 (Product Control)
        tags.update({
            'CV0302_POSITION_CMD': 35.2,
            'CV0302_POSITION_FB': 35.0,
            'CV0302_ACTUATOR_PRESSURE': 15.8,
            'CV0302_FLOW_COEFFICIENT': 89.5,
        })
        
        # Emergency Shutdown Valves
        tags.update({
            'ESD_0301_CLOSE_CMD': False,     # ESD Close Command
            'ESD_0301_OPEN_STATUS': True,    # ESD Valve Open
            'ESD_0301_CLOSED_STATUS': False, # ESD Valve Closed
            'ESD_0301_FAULT_STATUS': False,  # ESD Valve Fault
            'ESD_0302_OPEN_STATUS': True,    # ESD-302 Open
            'ESD_0303_OPEN_STATUS': True,    # ESD-303 Open
        })
        
        # Block Valves (Motor Operated)
        tags.update({
            'MOV_0301_OPEN_CMD': False,      # Motor Operated Valve Open Cmd
            'MOV_0301_CLOSE_CMD': False,     # MOV Close Command
            'MOV_0301_OPEN_STATUS': True,    # MOV Open Status
            'MOV_0301_CLOSED_STATUS': False, # MOV Closed Status
            'MOV_0301_TORQUE_ACTUAL': 45.8,  # MOV Torque (%)
            'MOV_0301_MOTOR_CURRENT': 12.5,  # MOV Motor Current
        })
        
        # =====================================================
        # AREA 400 - HEAT EXCHANGER SYSTEMS
        # =====================================================
        
        # Shell & Tube Heat Exchanger HX-401
        tags.update({
            'HX0401_TUBE_INLET_TEMP': 185.2,     # Tube Side Inlet Temperature
            'HX0401_TUBE_OUTLET_TEMP': 145.8,    # Tube Side Outlet Temperature
            'HX0401_SHELL_INLET_TEMP': 125.5,    # Shell Side Inlet Temperature
            'HX0401_SHELL_OUTLET_TEMP': 165.2,   # Shell Side Outlet Temperature
            'HX0401_TUBE_PRESSURE': 125.8,       # Tube Side Pressure
            'HX0401_SHELL_PRESSURE': 45.2,       # Shell Side Pressure
            'HX0401_TUBE_FLOW_RATE': 450.8,      # Tube Side Flow Rate
            'HX0401_SHELL_FLOW_RATE': 285.5,     # Shell Side Flow Rate
            'HX0401_FOULING_FACTOR': 0.0002,     # Fouling Factor
            'HX0401_OVERALL_U': 125.8,           # Overall Heat Transfer Coefficient
            'HX0401_LMTD': 28.5,                 # Log Mean Temperature Difference
            'HX0401_EFFECTIVENESS': 78.5,        # Heat Exchanger Effectiveness
        })
        
        # Air Cooler AC-402
        tags.update({
            'AC0402_INLET_TEMP': 125.8,          # Air Cooler Inlet Temperature
            'AC0402_OUTLET_TEMP': 85.2,          # Air Cooler Outlet Temperature
            'AC0402_FAN_1_STATUS': True,         # Fan 1 Running
            'AC0402_FAN_2_STATUS': True,         # Fan 2 Running
            'AC0402_FAN_1_SPEED': 850.0,         # Fan 1 Speed (RPM)
            'AC0402_FAN_2_SPEED': 845.0,         # Fan 2 Speed (RPM)
            'AC0402_AMBIENT_TEMP': 75.2,         # Ambient Temperature
        })
        
        # =====================================================
        # AREA 500 - DISTILLATION COLUMN SYSTEMS
        # =====================================================
        
        # Distillation Tower T-501
        tags.update({
            # Column Temperatures (Multiple Trays)
            'T0501_TRAY_01_TEMP': 185.5,        # Top Tray Temperature
            'T0501_TRAY_05_TEMP': 195.8,        # Tray 5 Temperature
            'T0501_TRAY_10_TEMP': 215.2,        # Tray 10 Temperature
            'T0501_TRAY_15_TEMP': 235.8,        # Tray 15 Temperature
            'T0501_TRAY_20_TEMP': 255.5,        # Bottom Tray Temperature
            
            # Column Pressures
            'T0501_TOP_PRESSURE': 15.2,         # Top Pressure (psig)
            'T0501_BOTTOM_PRESSURE': 18.5,      # Bottom Pressure (psig)
            'T0501_DIFFERENTIAL_PRESSURE': 3.3, # Differential Pressure
            
            # Reflux System
            'T0501_REFLUX_FLOW': 125.8,         # Reflux Flow Rate
            'T0501_REFLUX_RATIO': 3.5,          # Reflux Ratio
            'T0501_REFLUX_TEMP': 145.2,         # Reflux Temperature
            'T0501_REFLUX_DRUM_LEVEL': 65.8,    # Reflux Drum Level (%)
            
            # Reboiler System
            'T0501_REBOILER_DUTY': 2850.5,      # Reboiler Heat Duty (kW)
            'T0501_REBOILER_TEMP': 285.8,       # Reboiler Temperature
            'T0501_REBOILER_LEVEL': 55.2,       # Reboiler Level (%)
            
            # Product Streams
            'T0501_DISTILLATE_FLOW': 85.5,      # Distillate Flow Rate
            'T0501_BOTTOMS_FLOW': 165.8,        # Bottoms Flow Rate
            'T0501_FEED_FLOW': 250.0,           # Feed Flow Rate
            'T0501_FEED_TEMP': 185.5,           # Feed Temperature
        })
        
        # =====================================================
        # AREA 600 - ANALYZER SYSTEMS
        # =====================================================
        
        # Gas Chromatograph GC-601
        tags.update({
            'GC0601_H2_PERCENT': 2.45,          # Hydrogen Concentration (%)
            'GC0601_O2_PERCENT': 18.52,         # Oxygen Concentration
            'GC0601_N2_PERCENT': 75.28,         # Nitrogen Concentration
            'GC0601_CO2_PERCENT': 3.12,         # CO2 Concentration
            'GC0601_CH4_PERCENT': 0.58,         # Methane Concentration
            'GC0601_ETHANE_PERCENT': 0.05,      # Ethane Concentration
            'GC0601_SAMPLE_VALID': True,        # Sample Valid Flag
            'GC0601_ANALYSIS_TIME': 8.5,        # Analysis Time (minutes)
            'GC0601_STATUS': 'ANALYZING',       # Analyzer Status
            'GC0601_CALIBRATION_DUE': False,    # Calibration Due
            'GC0601_CARRIER_GAS_PRESSURE': 25.8, # Carrier Gas Pressure
            'GC0601_COLUMN_TEMP': 85.2,         # Column Temperature
        })
        
        # Mass Spectrometer MS-602
        tags.update({
            'MS0602_MOLECULAR_WEIGHT': 28.5,    # Average Molecular Weight
            'MS0602_PURITY_PERCENT': 99.85,     # Product Purity
            'MS0602_IMPURITY_PPM': 1500,        # Impurity Level (ppm)
            'MS0602_STATUS': 'ONLINE',          # MS Status
        })
        
        # pH Analyzer PH-603
        tags.update({
            'PH0603_VALUE': 7.23,               # pH Value
            'PH0603_TEMPERATURE': 25.5,         # Sample Temperature
            'PH0603_AUTO_CLEAN_STATUS': False,  # Auto Clean Active
        })
        
        # Conductivity Analyzer COND-604
        tags.update({
            'COND0604_VALUE': 485.2,            # Conductivity (µS/cm)
            'COND0604_TEMPERATURE': 25.0,       # Sample Temperature
            'COND0604_CELL_CONSTANT': 1.0,      # Cell Constant
        })
        
        # =====================================================
        # AREA 700 - UTILITY SYSTEMS
        # =====================================================
        
        # Air Compressor System
        tags.update({
            'AIR_COMP_701_RUN': True,           # Air Compressor Running
            'AIR_COMP_701_LOAD': 78.5,          # Compressor Load (%)
            'AIR_COMP_701_DISCHARGE_PRESSURE': 125.8, # Discharge Pressure
            'AIR_COMP_701_DISCHARGE_TEMP': 185.2, # Discharge Temperature
            'AIR_COMP_701_MOTOR_CURRENT': 125.8, # Motor Current
            'AIR_COMP_701_VIBRATION': 2.5,      # Vibration Level
            'AIR_COMP_701_RUNTIME_HOURS': 8547, # Runtime Hours
            
            # Compressed Air System
            'AIR_HEADER_PRESSURE': 110.5,       # Main Air Header Pressure
            'AIR_DRYER_DEWPOINT': -40.0,        # Air Dryer Dewpoint
            'AIR_RECEIVER_LEVEL': 85.2,         # Air Receiver Level
        })
        
        # Steam System
        tags.update({
            'STEAM_HEADER_PRESSURE': 145.8,     # Steam Header Pressure (psig)
            'STEAM_HEADER_TEMP': 365.2,         # Steam Header Temperature
            'STEAM_FLOW_RATE': 15420.5,         # Steam Flow Rate (lb/hr)
            'STEAM_CONDENSATE_RETURN_TEMP': 185.5, # Condensate Return Temp
            'STEAM_BOILER_LOAD': 65.8,          # Boiler Load (%)
            'STEAM_BOILER_EFFICIENCY': 85.2,    # Boiler Efficiency (%)
        })
        
        # Cooling Water System  
        tags.update({
            'CW_SUPPLY_TEMP': 85.2,             # Cooling Water Supply Temperature
            'CW_RETURN_TEMP': 95.8,             # Cooling Water Return Temperature
            'CW_SUPPLY_PRESSURE': 45.8,         # CW Supply Pressure
            'CW_FLOW_RATE': 8500.5,             # CW Flow Rate (GPM)
            'CW_TOWER_FAN_1_STATUS': True,      # Cooling Tower Fan 1
            'CW_TOWER_FAN_2_STATUS': True,      # Cooling Tower Fan 2
            'CW_TOWER_MAKEUP_FLOW': 125.8,      # Makeup Water Flow
        })
        
        # Electrical System
        tags.update({
            'ELEC_MAIN_VOLTAGE_A': 478.5,       # Main Bus Voltage Phase A
            'ELEC_MAIN_VOLTAGE_B': 479.2,       # Main Bus Voltage Phase B
            'ELEC_MAIN_VOLTAGE_C': 478.9,       # Main Bus Voltage Phase C
            'ELEC_MAIN_CURRENT_A': 285.5,       # Main Bus Current Phase A
            'ELEC_MAIN_CURRENT_B': 289.2,       # Main Bus Current Phase B
            'ELEC_MAIN_CURRENT_C': 287.8,       # Main Bus Current Phase C
            'ELEC_MAIN_FREQUENCY': 60.02,       # Line Frequency
            'ELEC_POWER_FACTOR': 0.95,          # Power Factor
            'ELEC_KW_DEMAND': 1250.8,           # kW Demand
            'ELEC_KVAR_DEMAND': 485.2,          # kVAR Demand
            'ELEC_KWH_TOTAL': 2547895,          # Total kWh
        })
        
        # =====================================================
        # AREA 800 - SAFETY INSTRUMENTED SYSTEM (SIS)
        # =====================================================
        
        tags.update({
            # Emergency Shutdown System
            'SIS_REACTOR_TRIP': False,          # Reactor Emergency Trip
            'SIS_HIGH_PRESSURE_TRIP': False,    # High Pressure Trip
            'SIS_HIGH_TEMP_TRIP': False,        # High Temperature Trip
            'SIS_GAS_DETECT_TRIP': False,       # Gas Detection Trip
            'SIS_FIRE_DETECT_TRIP': False,      # Fire Detection Trip
            'SIS_SYSTEM_HEALTHY': True,         # SIS System Health
            'SIS_BYPASS_ACTIVE': False,         # SIS Bypass Active
            'SIS_TEST_MODE': False,             # SIS Test Mode
            
            # Gas Detection System
            'GAS_DETECT_H2S_PPM': 0.0,          # H2S Detection (ppm)
            'GAS_DETECT_LEL_PERCENT': 0.0,      # Lower Explosive Limit (%)
            'GAS_DETECT_O2_PERCENT': 20.9,      # Oxygen Level (%)
            'GAS_DETECT_CO_PPM': 0.0,           # Carbon Monoxide (ppm)
            
            # Fire Detection System
            'FIRE_DETECT_ZONE_1': False,        # Fire Zone 1
            'FIRE_DETECT_ZONE_2': False,        # Fire Zone 2
            'FIRE_DETECT_ZONE_3': False,        # Fire Zone 3
            'FIRE_SUPPRESS_SYSTEM_READY': True, # Fire Suppression Ready
        })
        
        # =====================================================
        # AREA 900 - PRODUCTION & BATCH SYSTEMS
        # =====================================================
        
        tags.update({
            # Batch Control
            'PROD_BATCH_NUMBER': 'B2025073001', # Current Batch Number
            'PROD_RECIPE_NAME': 'POLYMER_GRADE_A', # Current Recipe
            'PROD_RECIPE_VERSION': '1.25',       # Recipe Version
            'PROD_BATCH_STATE': 'RUNNING',       # Batch State
            'PROD_BATCH_PHASE': 'REACTION',      # Current Phase
            'PROD_BATCH_STEP': 'HEATING',        # Current Step
            'PROD_TARGET_QUANTITY': 50000.0,     # Target Production (kg)
            'PROD_ACTUAL_QUANTITY': 12587.5,     # Actual Production (kg)
            'PROD_BATCH_COMPLETE_PCT': 25.2,     # Batch Complete (%)
            'PROD_HOURLY_RATE': 2458.5,          # Production Rate (kg/hr)
            'PROD_DAILY_TOTAL': 58545.2,         # Daily Total (kg)
            'PROD_MONTHLY_TOTAL': 1547825.8,     # Monthly Total (kg)
            'PROD_YIELD_PERCENT': 98.5,          # Process Yield (%)
            
            # Quality Control
            'QC_SAMPLE_ID': 'QC2025073001',      # QC Sample ID
            'QC_MOISTURE_PERCENT': 0.15,         # Moisture Content (%)
            'QC_DENSITY': 0.985,                 # Product Density (g/cm³)
            'QC_VISCOSITY': 125.8,               # Viscosity (cP)
            'QC_COLOR_INDEX': 2.5,               # Color Index
            'QC_PARTICLE_SIZE': 125.5,           # Particle Size (µm)
            'QC_RELEASE_STATUS': 'PENDING',      # Release Status
            
            # Overall Equipment Effectiveness (OEE)
            'OEE_AVAILABILITY': 95.2,            # Availability (%)
            'OEE_PERFORMANCE': 87.8,             # Performance Rate (%)
            'OEE_QUALITY': 99.1,                 # Quality Rate (%)
            'OEE_OVERALL': 82.9,                 # Overall OEE (%)
        })
        
        # =====================================================
        # AREA 1000 - ALARM & STATUS SYSTEMS
        # =====================================================
        
        tags.update({
            # Alarm Counters
            'ALARM_COUNT_CRITICAL': 0,          # Critical Alarms
            'ALARM_COUNT_HIGH': 2,              # High Priority Alarms
            'ALARM_COUNT_MEDIUM': 5,            # Medium Priority Alarms
            'ALARM_COUNT_LOW': 12,              # Low Priority Alarms
            'ALARM_COUNT_TOTAL': 19,            # Total Active Alarms
            'ALARM_COUNT_ACKNOWLEDGED': 15,     # Acknowledged Alarms
            'ALARM_COUNT_UNACKNOWLEDGED': 4,    # Unacknowledged Alarms
            
            # System Status
            'SYSTEM_OPERATOR_COUNT': 3,         # Active Operators
            'SYSTEM_HMI_CONNECTIONS': 5,        # HMI Connections
            'SYSTEM_HISTORIAN_STATUS': True,    # Historian Online
            'SYSTEM_BACKUP_STATUS': True,       # Backup System OK
            'SYSTEM_UPS_STATUS': True,          # UPS System OK
            'SYSTEM_UPS_BATTERY_PERCENT': 95.8, # UPS Battery Level
        })
        
        # =====================================================
        # AREA 1100 - ENVIRONMENTAL MONITORING
        # =====================================================
        
        tags.update({
            # Weather Station
            'WEATHER_TEMP_AMBIENT': 75.2,       # Ambient Temperature (°F)
            'WEATHER_HUMIDITY': 65.5,           # Relative Humidity (%)
            'WEATHER_BAROMETRIC': 29.92,        # Barometric Pressure (inHg)
            'WEATHER_WIND_SPEED': 8.5,          # Wind Speed (mph)
            'WEATHER_WIND_DIRECTION': 225.0,    # Wind Direction (degrees)
            'WEATHER_RAINFALL': 0.0,            # Rainfall Rate (in/hr)
            
            # Environmental Monitoring
            'ENV_NOISE_LEVEL': 68.2,            # Noise Level (dB)
            'ENV_DUST_LEVEL': 25.8,             # Dust Level (µg/m³)
            'ENV_SO2_PPM': 0.02,                # SO2 Emissions (ppm)
            'ENV_NOX_PPM': 0.15,                # NOx Emissions (ppm)
            'ENV_CO_PPM': 0.5,                  # CO Emissions (ppm)
        })
        
        # =====================================================
        # AREA 1200 - SCADA & COMMUNICATION SYSTEMS
        # =====================================================
        
        tags.update({
            # SCADA System
            'SCADA_SYSTEM_STATUS': True,        # SCADA System Online
            'SCADA_COMM_STATUS': True,          # Communication Status
            'SCADA_LAST_UPDATE': datetime.now().isoformat(), # Last Update Time
            'SCADA_CURRENT_USER': 'OPERATOR_01', # Current Operator
            'SCADA_SESSION_COUNT': 3,           # Active Sessions
            'SCADA_DATA_RATE': 1.25,            # Data Rate (MB/s)
            'SCADA_NETWORK_LATENCY': 15.2,      # Network Latency (ms)
            
            # Communication Status
            'COMM_ETHERNET_STATUS': True,       # Ethernet Status
            'COMM_SERIAL_PORT_1_STATUS': True,  # Serial Port 1
            'COMM_SERIAL_PORT_2_STATUS': True,  # Serial Port 2
            'COMM_WIRELESS_SIGNAL': 85.2,       # Wireless Signal (%)
        })
        
        # =====================================================
        # LEGACY COMPATIBILITY TAGS
        # =====================================================
        
        # For backward compatibility with existing systems
        tags.update({
            'TEMPERATURE': 25.5,                # Legacy Temperature Sensor
            'PRESSURE': 101.3,                  # Legacy Pressure Sensor
            'STATUS': True,                     # Legacy System Status
            'COUNTER': 100,                     # Legacy Production Counter
            'TEXT': 'Industrial PLC Simulator', # Legacy System Identifier
            'SCADA': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100], # Legacy SCADA Array
        })
        
        # Add individual array elements for compatibility
        for i in range(10):
            tags[f'SCADA[{i}]'] = tags['SCADA'][i]
        
        return tags
    
    def _initialize_tag_metadata(self):
        """Initialize tag metadata with descriptions and engineering units"""
        metadata = {}
        
        # Sample metadata for key tags
        metadata.update({
            'R0101_TIC_2101_PV': {
                'description': 'Reactor R-101 Temperature Process Variable',
                'units': '°C',
                'data_type': 'REAL',
                'min_value': 0.0,
                'max_value': 500.0,
                'alarm_high': 375.0,
                'alarm_low': 200.0
            },
            'P0201_M_SPEED_ACTUAL': {
                'description': 'Feed Pump P-201 Motor Actual Speed',
                'units': 'RPM',
                'data_type': 'REAL',
                'min_value': 0.0,
                'max_value': 3600.0
            }
        })
        
        return metadata
    
    def simulate_process_dynamics(self):
        """Simulate realistic process dynamics and tag value changes"""
        current_time = time.time()
        elapsed = current_time - self.start_time
        
        # Temperature cycling with realistic dynamics
        temp_noise = random.uniform(-2.0, 2.0)
        self.tags['R0101_TIC_2101_PV'] = 348.5 + 5.0 * math.sin(elapsed / 60.0) + temp_noise
        
        # Pump speed variations
        if self.tags['P0201_M_RUN_STATUS']:
            speed_variation = random.uniform(-10.0, 10.0)
            self.tags['P0201_M_SPEED_ACTUAL'] = min(max(1750.0 + speed_variation, 0), 3600)
        
        # Flow rate based on pump speed and valve position
        pump_factor = self.tags['P0201_M_SPEED_ACTUAL'] / 1750.0
        valve_factor = self.tags['CV0301_POSITION_FB'] / 100.0
        base_flow = 250.0
        self.tags['P0201_FLOW_RATE'] = base_flow * pump_factor * valve_factor + random.uniform(-5, 5)
        
        # Batch progress simulation
        if self.tags['PROD_BATCH_STATE'] == 'RUNNING':
            self.process_params['batch_progress'] += 0.1  # 0.1% per update
            self.tags['PROD_BATCH_COMPLETE_PCT'] = min(self.process_params['batch_progress'], 100.0)
            
            if self.tags['PROD_BATCH_COMPLETE_PCT'] >= 100.0:
                self.tags['PROD_BATCH_STATE'] = 'COMPLETE'
        
        # Production rate calculation
        production_efficiency = self.tags['OEE_OVERALL'] / 100.0
        base_rate = 2500.0  # kg/hr
        self.tags['PROD_HOURLY_RATE'] = base_rate * production_efficiency + random.uniform(-50, 50)
        
        # Vibration monitoring with occasional spikes
        if random.random() < 0.02:  # 2% chance of vibration spike
            self.tags['P0201_VIBRATION_X'] = random.uniform(5.0, 8.0)
        else:
            self.tags['P0201_VIBRATION_X'] = random.uniform(1.5, 2.5)
    
    def get_tag_type(self, value):
        """Determine PLC data type from Python value"""
        if isinstance(value, bool):
            return 'BOOL'
        elif isinstance(value, int):
            if -128 <= value <= 127:
                return 'SINT'
            elif -32768 <= value <= 32767:
                return 'INT'
            else:
                return 'DINT'
        elif isinstance(value, float):
            return 'REAL'
        elif isinstance(value, str):
            if len(value) <= 82:
                return 'SSTRING'
            else:
                return 'STRING'
        elif isinstance(value, list):
            return 'ARRAY'
        else:
            return 'UNKNOWN'
    
    def start_http_server(self):
        """Start HTTP server for API access"""
        server = self
        
        class PLCHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                """Handle GET requests"""
                # Update process dynamics on each request
                server.simulate_process_dynamics()
                
                parsed = urllib.parse.urlparse(self.path)
                query = urllib.parse.parse_qs(parsed.query)
                
                # Serve web interface on root path
                if parsed.path == '/':
                    try:
                        # Check if web/index.html exists
                        import os
                        web_file = os.path.join(os.path.dirname(__file__), 'web', 'index.html')
                        if os.path.exists(web_file):
                            with open(web_file, 'r', encoding='utf-8') as f:
                                content = f.read()
                            self.send_response(200)
                            self.send_header('Content-type', 'text/html')
                            self.end_headers()
                            self.wfile.write(content.encode())
                        else:
                            # Fallback to simple status page
                            self.send_response(200)
                            self.send_header('Content-type', 'text/html')
                            self.end_headers()
                            html = f'''
                            <html>
                            <head><title>Industrial PLC Simulator</title></head>
                            <body style="font-family: Arial, sans-serif; padding: 20px;">
                                <h1>Industrial PLC Simulator</h1>
                                <p>Digital Energy Services - www.digitalenergyservices.ca</p>
                                <h2>Status: Running</h2>
                                <p>Total Tags: {len(server.tags)}</p>
                                <h3>API Endpoints:</h3>
                                <ul>
                                    <li>GET <a href="/tags">/tags</a> - List all tags</li>
                                    <li>GET <a href="/areas">/areas</a> - Tags by area</li>
                                    <li>GET <a href="/alarms">/alarms</a> - Active alarms</li>
                                    <li>GET /read?tags=TAG1,TAG2 - Read tag values</li>
                                    <li>POST /write - Write tag values</li>
                                </ul>
                            </body>
                            </html>
                            '''
                            self.wfile.write(html.encode())
                    except Exception as e:
                        self.send_response(500)
                        self.end_headers()
                    return
                
                # CORS headers for API endpoints
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                
                if parsed.path == '/tags':
                    # Return all available tags with metadata
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    
                    response = {
                        'tags': [
                            {
                                'name': name, 
                                'type': server.get_tag_type(value),
                                'value': value
                            }
                            for name, value in server.tags.items()
                        ],
                        'total_tags': len(server.tags),
                        'status': 'Success',
                        'timestamp': datetime.now().isoformat()
                    }
                    self.wfile.write(json.dumps(response, indent=2).encode())
                    
                elif parsed.path == '/read':
                    # Read specific tag values
                    tag_names = query.get('tags', [])
                    if isinstance(tag_names, list) and len(tag_names) > 0:
                        tag_names = tag_names[0].split(',')
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    
                    values = {}
                    for tag_name in tag_names:
                        tag_name = tag_name.strip()
                        if tag_name in server.tags:
                            values[tag_name] = {
                                'value': server.tags[tag_name],
                                'type': server.get_tag_type(server.tags[tag_name]),
                                'quality': 'GOOD',
                                'timestamp': datetime.now().isoformat()
                            }
                        else:
                            values[tag_name] = {
                                'value': None,
                                'type': 'UNKNOWN',
                                'quality': 'BAD',
                                'error': 'Tag not found'
                            }
                    
                    response = {
                        'values': values,
                        'timestamp': datetime.now().isoformat(),
                        'status': 'Success'
                    }
                    self.wfile.write(json.dumps(response, indent=2).encode())
                
                elif parsed.path == '/areas':
                    # Return tags organized by plant areas
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    
                    areas = {}
                    for tag_name, value in server.tags.items():
                        if tag_name.startswith('R01'):
                            area = 'Reactor Systems'
                        elif tag_name.startswith('P02'):
                            area = 'Pump Systems'
                        elif tag_name.startswith('CV03') or tag_name.startswith('ESD') or tag_name.startswith('MOV'):
                            area = 'Valve Systems'
                        elif tag_name.startswith('HX04') or tag_name.startswith('AC04'):
                            area = 'Heat Exchangers'
                        elif tag_name.startswith('T05'):
                            area = 'Distillation'
                        elif tag_name.startswith('GC06') or tag_name.startswith('MS06') or tag_name.startswith('PH06') or tag_name.startswith('COND06'):
                            area = 'Analyzers'
                        elif tag_name.startswith('AIR') or tag_name.startswith('STEAM') or tag_name.startswith('CW') or tag_name.startswith('ELEC'):
                            area = 'Utilities'
                        elif tag_name.startswith('SIS') or tag_name.startswith('GAS_DETECT') or tag_name.startswith('FIRE'):
                            area = 'Safety Systems'
                        elif tag_name.startswith('PROD') or tag_name.startswith('QC') or tag_name.startswith('OEE'):
                            area = 'Production'
                        elif tag_name.startswith('ALARM') or tag_name.startswith('SYSTEM'):
                            area = 'Alarms & Status'
                        elif tag_name.startswith('WEATHER') or tag_name.startswith('ENV'):
                            area = 'Environmental'
                        elif tag_name.startswith('SCADA') or tag_name.startswith('COMM'):
                            area = 'Communications'
                        else:
                            area = 'Legacy/Other'
                        
                        if area not in areas:
                            areas[area] = []
                        
                        areas[area].append({
                            'name': tag_name,
                            'type': server.get_tag_type(value),
                            'value': value
                        })
                    
                    response = {
                        'areas': areas,
                        'total_areas': len(areas),
                        'status': 'Success'
                    }
                    self.wfile.write(json.dumps(response, indent=2).encode())
                
                elif parsed.path == '/alarms':
                    # Return current alarm status
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    
                    active_alarms = []
                    
                    # Check for active alarms based on tag values
                    if server.tags['R0101_TIC_2101_PV'] > 375.0:
                        active_alarms.append({
                            'tag': 'R0101_TIC_2101_PV',
                            'description': 'Reactor Temperature High',
                            'priority': 'HIGH',
                            'timestamp': datetime.now().isoformat()
                        })
                    
                    if server.tags['P0201_VIBRATION_X'] > 4.0:
                        active_alarms.append({
                            'tag': 'P0201_VIBRATION_X',
                            'description': 'Pump Vibration High',
                            'priority': 'MEDIUM',
                            'timestamp': datetime.now().isoformat()
                        })
                    
                    response = {
                        'active_alarms': active_alarms,
                        'alarm_summary': server.alarm_counts,
                        'status': 'Success'
                    }
                    self.wfile.write(json.dumps(response, indent=2).encode())
                
                else:
                    # 404 for unknown endpoints
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {'error': 'Endpoint not found', 'status': 'Error'}
                    self.wfile.write(json.dumps(response).encode())
            
            def do_POST(self):
                """Handle POST requests for writing tag values"""
                if self.path == '/write':
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    
                    try:
                        data = json.loads(post_data.decode('utf-8'))
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        
                        results = {}
                        for tag_name, value in data.items():
                            if tag_name in server.tags:
                                server.tags[tag_name] = value
                                results[tag_name] = {'status': 'SUCCESS', 'value': value}
                            else:
                                results[tag_name] = {'status': 'ERROR', 'error': 'Tag not found'}
                        
                        response = {
                            'results': results,
                            'timestamp': datetime.now().isoformat(),
                            'status': 'Success'
                        }
                        self.wfile.write(json.dumps(response).encode())
                        
                    except json.JSONDecodeError:
                        self.send_response(400)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        response = {'error': 'Invalid JSON', 'status': 'Error'}
                        self.wfile.write(json.dumps(response).encode())
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def do_OPTIONS(self):
                """Handle OPTIONS requests for CORS"""
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()
        
        httpd = HTTPServer((self.host, self.port), PLCHandler)
        print(f"Industrial PLC Simulator started on http://{self.host}:{self.port}")
        print(f"Total Tags Available: {len(self.tags)}")
        print(f"Available endpoints:")
        print(f"  GET /tags - List all tags with metadata")
        print(f"  GET /read?tags=TAG1,TAG2,... - Read tag values")
        print(f"  GET /areas - Tags organized by plant areas")
        print(f"  GET /alarms - Current alarm status")
        print(f"  POST /write - Write tag values (JSON body)")
        print(f"Example tags: {list(self.tags.keys())[:10]}...")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\\nServer stopped")
            httpd.shutdown()

if __name__ == '__main__':
    import sys
    
    print("Industrial PLC Simulator")
    print("=" * 50)
    print("Professional industrial automation testing platform")
    print("Featuring 295+ industrial tags across 12 process areas")
    print()
    
    # Start the industrial PLC simulator
    simulator = IndustrialPLCSimulator()
    simulator.start_http_server()