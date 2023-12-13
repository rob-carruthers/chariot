"""Global parameters for chariot"""
import os

APP_KEY = os.getenv("TFL_API_KEY")
PREFERRED_MODES = ["tube", "dlr"]
TFL_BASE_URL = "https://api.tfl.gov.uk/"
TIMEOUT = 30
