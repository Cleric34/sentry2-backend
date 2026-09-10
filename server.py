
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# ============================================================
# OLD IMPORTS — KEPT FOR FUTURE USE
# ============================================================

# import pandas as pd
# import math
# from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent

# OLD ML MODEL — DO NOT DELETE
# from ml_pipeline.mastitis_model import MastitisPredictiveEngine


# ============================================================
# SENTRY 2 - FASTAPI SENSOR SERVER
# CURRENT MODE:
# ONLY TEMPERATURE + TDS RAW + TDS VOLTAGE
# ============================================================

app = FastAPI(
    title="SENTRY 2 API",
    description="Live ESP32 temperature and TDS sensor server",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# CURRENT LIVE SENSOR STATE
# ============================================================

latest_sensor_state = None


# ============================================================
# REQUEST MODEL
# ============================================================

class SensorData(BaseModel):
    device_id: str
    temperature: float
    tds_raw: int
    tds_voltage: float


# ============================================================
# LIVE SENSOR ENDPOINT
# ============================================================
#
# CURRENTLY ACCEPTS ONLY:
#   - temperature
#   - tds_raw
#   - tds_voltage
#
# device_id is accepted only so the current ESP32 JSON format
# does not need to change.
#
# NO pH
# NO milk yield
# NO cow data
# NO ML prediction
# NO 18-feature processing
# ============================================================

@app.post("/sensor-data")
def receive_sensor_data(data: SensorData):

    global latest_sensor_state

    latest_sensor_state = {
        "temperature": data.temperature}
        ,
        {"tds_raw": data.tds_raw},

        {"tds_voltage": data.tds_voltage},
        
    }

    print()
    print("==============================")
    print("       SENTRY 2 LIVE DATA")
    print("==============================")
    print(f"\nTemperature  : {data.temperature:.2f} °C")
    print(f"\nTDS Raw      : {data.tds_raw}")
    print(f"TDS Voltage  : {data.tds_voltage:.6f} V")
    print("==============================")

    return latest_sensor_state


# ============================================================
# LATEST SENSOR DATA
# ============================================================
#
# THIS ENDPOINT ALSO RETURNS ONLY:
#   temperature
#   tds_raw
#   tds_voltage
# ============================================================

@app.get("/latest-sensor")
def latest_sensor():

    if latest_sensor_state is None:
        return {
            "message": "No sensor data received yet."
        }

    return latest_sensor_state


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "project": "SENTRY 2",
        "status": "online",
        "mode": "ESP32 temperature + TDS only",
    }


# ============================================================
# ============================================================
# OLD BACKEND CODE — KEPT HERE FOR FUTURE RESTORATION
# ============================================================
# ============================================================


# ============================================================
# OLD DATA LOADING
# ============================================================

# cow_data = pd.read_csv(BASE_DIR / "cow_data.csv")
# ph_data = pd.read_csv(BASE_DIR / "ph.csv")
# milk_data = pd.read_csv(BASE_DIR / "milk_yield.csv")

# data_index = 0

# active_cow_id = "COW_001"

# mastitis_engine = MastitisPredictiveEngine()


# ============================================================
# OLD JSON SAFETY FUNCTION
# ============================================================

# def make_json_safe(obj):
#
#     if obj is None:
#         return None
#
#     if hasattr(obj, "item"):
#         try:
#             return obj.item()
#         except (ValueError, TypeError):
#             pass
#
#     if isinstance(obj, dict):
#         return {
#             str(key): make_json_safe(value)
#             for key, value in obj.items()
#         }
#
#     if isinstance(obj, (list, tuple)):
#         return [make_json_safe(value) for value in obj]
#
#     return obj


# ============================================================
# OLD COW SELECTION
# ============================================================

# class CowSelection(BaseModel):
#     cow_id: str


# @app.get("/cows")
# def get_cows():
#
#     records = cow_data.to_dict(orient="records")
#
#     return make_json_safe({
#         "success": True,
#         "cows": records,
#     })


# @app.get("/active-cow")
# def get_active_cow():
#
#     return {
#         "success": True,
#         "active_cow_id": active_cow_id,
#     }


# @app.post("/select-cow")
# def select_cow(selection: CowSelection):
#
#     global active_cow_id
#
#     cow_id = selection.cow_id.strip()
#
#     if cow_id not in cow_data["cow_id"].astype(str).values:
#         raise HTTPException(
#             status_code=404,
#             detail=f"Cow ID '{cow_id}' not found"
#         )
#
#     active_cow_id = cow_id
#
#     return {
#         "success": True,
#         "active_cow_id": active_cow_id,
#     }


# ============================================================
# OLD TDS CALCULATION
# ============================================================
#
# KEPT FOR FUTURE USE.
#
# IMPORTANT:
# This was the original generic TDS conversion.
# It is NOT laboratory calibrated for milk.
# ============================================================

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


# ============================================================
# OLD CONDUCTIVITY CALCULATION
# ============================================================

# def calculate_conductivity(tds: float) -> float:
#
#     return float((tds / 0.5) / 1000.0)


# ============================================================
# OLD SENSOR PROCESSING
# ============================================================

# def old_receive_sensor_data(data: SensorData):
#
#     global data_index
#
#     selected_rows = cow_data[
#         cow_data["cow_id"].astype(str) == active_cow_id
#     ]
#
#     cow = selected_rows.iloc[0]
#
#     ph_value = float(
#         ph_data.iloc[data_index % len(ph_data)]["ph"]
#     )
#
#     milk_yield = float(
#         milk_data.iloc[data_index % len(milk_data)]["milk_yield"]
#     )
#
#     data_index += 1
#
#     estimated_tds = calculate_tds(
#         data.tds_voltage,
#         data.temperature,
#     )
#
#     conductivity = calculate_conductivity(
#         estimated_tds
#     )


# ============================================================
# OLD 18-FEATURE SCHEMA
# ============================================================

# features = {
#     "breed_idx": int(cow["breed_idx"]),
#     "age_years": float(cow["age_years"]),
#     "lactation_num": int(cow["lactation_num"]),
#     "vaccination_status": int(cow["vaccination_status"]),
#     "prior_mastitis_hist": int(cow["prior_mastitis_hist"]),
#     "thi_index": None,
#     "hygiene_score": float(cow["hygiene_score"]),
#     "concentrate_kg": None,
#     "water_intake_l": None,
#     "body_temp": float(data.temperature),
#     "rumination_mins": None,
#     "spine_angle": float(cow["spine_angle"]),
#     "milk_yield_l": milk_yield,
#     "ec_ms_cm": conductivity,
#     "milk_ph": ph_value,
#     "log_scc": None,
#     "tier1_cv_score": None,
#     "tier2_cmt_score": None,
# }


# ============================================================
# OLD PREDICTION PROFILE
# ============================================================

# prediction_profile = {
#     "cow_id": active_cow_id,
#     "breed": "Unknown",
#
#     "breed_idx": features["breed_idx"],
#     "age_years": features["age_years"],
#     "lactation_num": features["lactation_num"],
#     "vaccination_status": features["vaccination_status"],
#     "prior_mastitis_hist": features["prior_mastitis_hist"],
#     "hygiene_score": features["hygiene_score"],
#
#     "body_temp": features["body_temp"],
#     "spine_angle": features["spine_angle"],
#     "milk_yield_l": features["milk_yield_l"],
#     "ec_ms_cm": features["ec_ms_cm"],
#     "milk_ph": features["milk_ph"],
# }


# ============================================================
# OLD MODEL CALL
# ============================================================

# prediction = mastitis_engine.predict_cow_risk(
#     prediction_profile
# )

# prediction = make_json_safe(prediction)


# ============================================================
# OLD RESPONSE
# ============================================================

# response = {
#
#     "success": True,
#
#     "cow_id": active_cow_id,
#
#     "device_id": data.device_id,
#
#     "live_sensor_data": {
#         "temperature": data.temperature,
#         "tds_raw": data.tds_raw,
#         "tds_voltage": data.tds_voltage,
#         "estimated_tds_ppm": estimated_tds,
#         "conductivity_ms_cm": conductivity,
#     },
#
#     "simulated_data": {
#         "milk_ph": ph_value,
#         "milk_yield_l": milk_yield,
#     },
#
#     "cow_database": {
#         "cow_id": active_cow_id,
#         "breed_idx": cow["breed_idx"],
#         "age_years": cow["age_years"],
#         "lactation_num": cow["lactation_num"],
#         "vaccination_status": cow["vaccination_status"],
#         "prior_mastitis_hist": cow["prior_mastitis_hist"],
#         "hygiene_score": cow["hygiene_score"],
#         "spine_angle": cow["spine_angle"],
#     },
#
#     "features": features,
#
#     "prediction": prediction,
# }
#
# latest_sensor_state = response
#
# return make_json_safe(response)