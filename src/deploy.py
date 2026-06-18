import subprocess
from fastapi import APIRouter, HTTPException, Header

router = APIRouter(prefix="/deploy")
DEPLOY_TOKEN = "secret-token-12345"

@router.post("/")
async def deploy(authorization: str = Header(None)):
    if authorization != f"Bearer {DEPLOY_TOKEN}":
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    # Запускаем деплой в фоне
    subprocess.Popen(["/home/chaplygin/deploy.sh"])
    return {"status": "deploy started"}
