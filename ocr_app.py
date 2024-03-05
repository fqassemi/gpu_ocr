from fastapi import FastAPI, UploadFile, File
import paramiko
import os
import time 
#from starlette.responses import FileResponse
from fastapi.responses import FileResponse
import asyncssh
import asyncio
import requests 

app = FastAPI()

async def ssh_operation(file_name):
    remote_server_ip = 'xx.xx.xx.xx'
    private_key_path = '/path/to/private_key'
    private_key = asyncssh.read_private_key(private_key_path)

    async with asyncssh.connect(remote_server_ip, username='fsuser', client_keys=[private_key], known_hosts=None ) as conn:
#        await conn.scp(file_content, f'/home/fsuser/{file_name}')
        result = await conn.run(f'/path/to/nougat /path/to/{file_name} -o  ./  -m 0.1.0-base --recompute', check=True)
        return result


@app.post("/gpu_ocr")
async def process_pdf(file: UploadFile = File(...)):
    pdf_content = await file.read()
    status = "stopped"
    while (status != "starting") and  (status != "running"):
          command = "curl -H 'Content-Type: application/json' -X PUT  'https://api.fluidstack.io/v1/server/server_id/start' -u 'token:key'"
          os.system(command)
          url = 'https://api.fluidstack.io/v1/server/servr_id'
          headers = {'Content-Type': 'application/json'}
          auth = ('token', 'key')

          response = requests.get(url, headers=headers, auth=auth)

          status = response.json()["status"]
          print(status)
          time.sleep(30)

    while status != "running":
          url = 'https://api.fluidstack.io/v1/server/server_id'
          headers = {'Content-Type': 'application/json'}
          auth = ('token', 'key')

          response = requests.get(url, headers=headers, auth=auth)

          status = response.json()["status"]
          print(status)
          time.sleep(30)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    private_key_path = '/path/to/private_key'
    username = 'user'
    remote_server_ip = 'xx.xx.xx.xx'    
    private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
    ssh.connect(remote_server_ip, username=username, pkey=private_key)


    try:
        remote_pdf_path = f"/path/to/{file.filename}"
        with ssh.open_sftp() as sftp:
            with sftp.file(remote_pdf_path, "wb") as remote_file:
                remote_file.write(pdf_content)
        
        output = await ssh_operation(f"{file.filename}")
        
        with ssh.open_sftp() as sftp:
            sftp.get(f"/path/to/{file.filename}"[:-4]+".mmd", f"/path/to/{file.filename}"[:-4]+".mmd")
        return FileResponse(f"/root/temp/{file.filename}"[:-4] + ".mmd")

    finally:
        ssh.close()
        command = "curl -H 'Content-Type: application/json' -X PUT  'https://api.fluidstack.io/v1/server/server_id/stop' -u 'token:key'"
        os.system(command)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8800)
