from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# ============================================================
# OLD / FUTURE IMPORTS
# ============================================================
# These are intentionally commented out for now.
# They can be restored later when the full ML pipeline is
# connected to the live sensor data.
#
# import pandas as pd
# import math
# from pathlib import Path
#
# BASE_DIR = Path(__file__).resolve().parent
#
# from ml_pipeline.mastitis_model import MastitisPredictiveEngine


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="SENTRY 2 API",
    description="Live ESP32 temperature and TDS sensor server",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# LATEST SENSOR DATA
# ============================================================

latest_sensor_state = None


# ============================================================
# SENSOR DATA MODEL
# ============================================================

class SensorData(BaseModel):
    device_id: str
    temperature: float
    tds_raw: int
    tds_voltage: float


# ============================================================
# ROOT / HEALTH CHECK
# ============================================================

@app.get("/")
def root():
    return {
        "project": "SENTRY 2",
        "status": "online",
        "mode": "ESP32 temperature + TDS only",
    }


# ============================================================
# RECEIVE LIVE ESP32 SENSOR DATA
# ============================================================

@app.post("/sensor-data")
def receive_sensor_data(data: SensorData):

    global latest_sensor_state

    # Store only the live sensor values we currently need.
    latest_sensor_state = {
        "temperature": data.temperature,
        "tds_raw": data.tds_raw,
        "tds_voltage": data.tds_voltage,
    }

    # --------------------------------------------------------
    # Server console output
    # --------------------------------------------------------

    print()
    print("==============================")
    print("       SENTRY 2 LIVE DATA")
    print("==============================")

    print(f"Temperature : {data.temperature:.3f} °C")
    print()
    print(f"TDS Raw     : {data.tds_raw}")
    print()
    print(f"TDS Voltage : {data.tds_voltage:.6f} V")

    print("==============================")

    # Return the latest sensor values.
    return latest_sensor_state


# ============================================================
# GET LATEST SENSOR DATA
# ============================================================

@app.get(
    "/latest-sensor",
    response_class=PlainTextResponse
)
def latest_sensor():

    if latest_sensor_state is None:
        return "No sensor data received yet."

    return (
        f"Temperature : {latest_sensor_state['temperature']:.3f} °C\n\n"
        f"TDS Raw     : {latest_sensor_state['tds_raw']}\n\n"
        f"TDS Voltage : {latest_sensor_state['tds_voltage']:.6f} V"
    )


# ============================================================
# ============================================================
# OLD BACKEND / ML PIPELINE
# ============================================================
#
# The following architecture is intentionally NOT active yet.
#
# Your current responsibility is:
#
# ESP32
#    ↓
# Wi-Fi
#    ↓
# Internet / HTTP
#    ↓
# FastAPI
#    ↓
# Receive live sensor data
#
# Later this can become:
#
# ESP32
#    ↓
# Wi-Fi
#    ↓
# FastAPI
#    ↓
# Combine sensor data with cow profile
#    ↓
# Build existing 18-feature schema
#    ↓
# Existing MastitisPredictiveEngine
#
# DO NOT MODIFY THE EXISTING MODEL.
#
# ============================================================


# ------------------------------------------------------------
# OLD DATA LOADING
# ------------------------------------------------------------
#
# import pandas as pd
#
# cow_data_path = BASE_DIR / "cow_data.csv"
# ph_data_path = BASE_DIR / "ph.csv"
# milk_yield_path = BASE_DIR / "milk_yield.csv"
#
# cow_data = pd.read_csv(cow_data_path)
# ph_data = pd.read_csv(ph_data_path)
# milk_yield_data = pd.read_csv(milk_yield_path)


# ------------------------------------------------------------
# OLD COW SELECTION
# ------------------------------------------------------------
#
# active_cow = None
#
#
# @app.post("/select-cow")
# def select_cow(...):
#     ...
#
#
# @app.get("/active-cow")
# def get_active_cow():
#     ...


# ------------------------------------------------------------
# OLD SENSOR PROCESSING
# ------------------------------------------------------------
#
# def calculate_tds(voltage: float, temperature: float) -> float:
#
#     compensation_voltage = voltage / (
#         1 + 0.02 * (temperature - 25.0)
#     )
#
#     tds = (
#         133.42 * compensation_voltage ** 3
#         - 255.86 * compensation_voltage ** 2
#         + 857.39 * compensation_voltage
#     ) * 0.5
#
#     return max(0.0, float(tds))
#
#
# def calculate_conductivity(tds: float) -> float:
#     return float((tds / 0.5) / 1000.0)


# ------------------------------------------------------------
# OLD SENSOR ENDPOINT
# ------------------------------------------------------------
#
# The previous implementation processed:
#
# - temperature
# - TDS
# - conductivity
# - milk pH
# - milk yield
#
# This has intentionally been disabled for now.


# ------------------------------------------------------------
# OLD 18-FEATURE SCHEMA
# ------------------------------------------------------------
#
# The existing ML model expects:
#
# 1.  breed_idx
# 2.  age_years
# 3.  lactation_num
# 4.  vaccination_status
# 5.  prior_mastitis_hist
# 6.  thi_index
# 7.  hygiene_score
# 8.  concentrate_kg
# 9.  water_intake_l
# 10. body_temp
# 11. rumination_mins
# 12. spine_angle
# 13. milk_yield_l
# 14. ec_ms_cm
# 15. milk_ph
# 16. log_scc
# 17. tier1_cv_score
# 18. tier2_cmt_score
#
# This schema is NOT being modified.
#
# The complete feature assembly will be restored when the
# other data sources are connected.


# ------------------------------------------------------------
# OLD MODEL INITIALIZATION
# ------------------------------------------------------------
#
# model = MastitisPredictiveEngine()
#
# The model itself must remain unchanged.


# ------------------------------------------------------------
# OLD MODEL PREDICTION
# ------------------------------------------------------------
#
# prediction = model.predict(cow_profile)
#
# The prediction layer is intentionally disabled for now.


# ============================================================
# END OF SERVER
# ============================================================