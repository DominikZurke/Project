from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import StreamingResponse
from PIL import Image, ImageChops
from io import BytesIO
import secrets
from datetime import datetime

app = FastAPI()
security = HTTPBasic()


@app.get("/Prime")
async def prime(number: int):
    if 1 < number <= 9223372036854775807:
        for i in range(2, int(number ** 0.5) + 1):
            if (number % i) == 0 and number == 1:
                return {f"Number {number} is not prime"}
        return {f"Number {number} is prime"}
    elif number == 1:
        return {f"Number {number} is not prime"}
    else:
        return {"Out of range"}


@app.post("/Invert")
async def invert(file: UploadFile = File(...)):
    original_image = Image.open(file.file)
    invert_image = ImageChops.invert(original_image)
    invert_image.show()
    image = BytesIO()
    invert_image.save(image, "JPEG")
    image.seek(0)

    return StreamingResponse(image, media_type="image/jpeg")


@app.post("/Auth")
def Authentication(credentials: HTTPBasicCredentials = Depends(security)):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"admin"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"admin"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {current_time}
