import os
import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# ����������� ������ ��� ������ �������
class RunScriptRequest(BaseModel):
    config: str
    userId: str

# ������������� FastAPI ����������
app = FastAPI()

@app.post("/run")
async def run_script(request: RunScriptRequest):
    config_content = request.config
    user_id = request.userId

    # �������� ����� ����� ������������
    config_filename = f"config-id_{user_id}.ini"
    try:
        # ������ ������������ � ����
        with open(config_filename, 'w') as f:
            f.write(config_content)

        # ���������� ������� ����� subprocess
        result = subprocess.run(
            ['python3', 'main.py', '-c', config_filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # ����������� ����������� ���������� �������
        return {"stdout": result.stdout, "stderr": result.stderr}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"������: {str(e)}")

# ������ ���������� (��� ������������� � Uvicorn)
if __name__ == "__main__":
    # ������ FastAPI � �������������� Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
