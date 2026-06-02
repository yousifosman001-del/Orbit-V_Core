import time

class OrbitSmartPort:
    def __init__(self):
        self.max_supported_wattage = 100.0  # Maximum port output for vehicle
        self.safety_temp_limit = 45.0       # Thermal safety threshold for battery

    def negotiate_power(self, device_profile):
        print(f"[Orbit-V] New device detected: {device_profile['brand']}")
        time.sleep(0.05)  # 50ms negotiation latency
        
        # Determine the optimal safe wattage
        target_wattage = min(self.max_supported_wattage, device_profile['max_sub_watt'])
        
        print(f"[Orbit-V] Protocol decoded successfully: {device_profile['protocol']}")
        return self.monitor_charging_session(target_wattage, device_profile)

    def monitor_charging_session(self, wattage, device_profile):
        current_temp = device_profile['current_temp']
        
        # Dynamic Thermal Safety Algorithm
        if current_temp >= self.safety_temp_limit:
            print("[WARNING] High temperature detected! Throttling power for battery safety.")
            wattage *= 0.5  # Reduce power by 50% for safety
        
        voltage = 20.0  # Standard stable voltage
        current = wattage / voltage
        
        return {
            "status": "Charging", 
            "voltage_v": voltage, 
            "current_a": round(current, 2), 
            "final_watt": wattage
        }

# ---- Execution Simulation Test ----
port = OrbitSmartPort()

passenger_phone = {
    "brand": "X-Phone",
    "protocol": "SuperCharge_Proprietary",
    "max_sub_watt": 66.0,
    "current_temp": 38.5
}

charge_output = port.negotiate_power(passenger_phone)
print(f"Current Charging Output: {charge_output}")
