import time

class OrbitSmartPortV2:
    def __init__(self):
        self.max_supported_wattage = 100.0  # Max vehicle output
        self.warning_temp_limit = 40.0      # Start throttling
        self.critical_temp_limit = 45.0     # Pause charging (User Point 4)
        self.base_car_usb_wattage = 5.0     # Standard weak port (User Point 2)

    def assess_cable_quality(self, cable_resistance_ohms):
        # User Point 3: Weak cable causes heat, limit current if resistance is high
        if cable_resistance_ohms > 1.5:
            print("[Diagnostics] High-resistance cable detected. Limiting power to prevent heat.")
            return 0.5  # 50% efficiency drop to stay safe
        return 1.0

    def negotiate_power(self, device_profile):
        print(f"[Orbit-V2] Connecting device: {device_profile['brand']}")
        time.sleep(0.05)
        
        cable_efficiency = self.assess_cable_quality(device_profile['cable_resistance_ohms'])
        
        # Maximize power dynamically based on cable capability
        target_wattage = min(self.max_supported_wattage, device_profile['max_sub_watt']) * cable_efficiency
        
        return self.monitor_charging_session(target_wattage, device_profile)

    def monitor_charging_session(self, wattage, device_profile):
        temp = device_profile['current_temp']
        
        # User Point 1 & 4: Active Thermal Management System
        if temp >= self.critical_temp_limit:
            print("[ALERT] Critical temperature! Charging PAUSED to cool down device.")
            return {
                "status": "Cooling Pause", 
                "final_watt": 0.0, 
                "action": "Waiting for temperature drop"
            }
        elif temp >= self.warning_temp_limit:
            print("[WARNING] Device is getting warm. Throttling power output.")
            wattage *= 0.5
            
        voltage = 20.0 if wattage > 15 else 5.0
        current = wattage / voltage if voltage > 0 else 0
        
        return {
            "status": "Charging Active", 
            "voltage_v": voltage, 
            "current_a": round(current, 2), 
            "final_watt": round(wattage, 2)
        }

# ---- Execution Simulation Test (V0.2) ----
port = OrbitSmartPortV2()

# Simulating a driver's phone with a bad cable and high heat
passenger_phone = {
    "brand": "X-Phone",
    "protocol": "SuperCharge",
    "max_sub_watt": 66.0,
    "current_temp": 46.0,          # Critical heat (Will trigger pause)
    "cable_resistance_ohms": 2.1   # Bad cheap cable
}

print("\n--- Starting Orbit-V2 Diagnostics ---")
charge_output = port.negotiate_power(passenger_phone)
print(f"Final Output: {charge_output}")
