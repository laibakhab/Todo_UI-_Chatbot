import os
from src.config import settings

print("Environment variables:")
for key, value in os.environ.items():
    if 'DATABASE' in key.upper():
        print(f"{key}: {value}")

print(f"\nSettings database URL: {settings.database_url}")