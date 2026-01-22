import uuid

# Unique run identifier (stable for the app session)
RUN_ID = uuid.uuid4().hex[:6]
