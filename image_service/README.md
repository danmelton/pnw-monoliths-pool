---
title: Image Microservice
description: A image microservice that resizes, stores, and deletes images
---

# Using Images Microservice
This program uses a Python/Flask Framework 

## Run it with Docker

From the repo root:

```sh
docker compose up --build -d image-service
docker compose ps                       # image-service should be "Up" on 127.0.0.1:5001->5001/tcp
docker compose logs image-service       # look for "Running on http://127.0.0.1:5001"
```

The test page is at http://localhost:5001. `image_service/src/` is mounted into the
container, so edits to `app.py` reload live. After changing `requirements.txt`, rebuild
with `docker compose up --build -d image-service`. Uploaded images are stored inside the
container, so they're gone after a rebuild.

To check the service against `openapi.json`, see [Test against the spec](#test-against-the-spec).

## Testing Image Microservice

1. Open a terminal and navigate to the project directory:\
`cd pnw-monoliths-pool/image_service`

2. Create a python virtual environment\
`python3 -m venv .venv`

3. Active the virtual environment\
`source .venv/bin/activate`

4. Install dependencies:\
`python3 -m pip install -r requirements.txt`

5. Start the app: \
Navigate into the src directory and start flask application:
```sh
cd src
python3 app.py
```
The Flask server should now be running at:
http://localhost:5001

### The tester program supports the following operations:

- Upload an image: Select a JPG or PNG image and click Upload. A success message and image ID should appear.

- Retrieve an image: Enter the image ID returned during upload and click Retrieve. The uploaded image should appear on the page.

- Delete an image: Enter the image ID and click Delete. A message should confirm whether the image was successfully deleted.

# Example calls 
## To request data from the microservice:
- Data is requested via HTTP GET requests. When you press the "retrieve" button on the form, it sends a GET request to the microservice for the image file corresponding to the ID provided.

| Request                    | Status | Body                                                        |
| -------------------------- | ------ | ----------------------------------------------------------- |
| `GET /images/<img_id>`           | 200    | The requested image (JPG or PNG) |
| `GET /images/<img_id>`  | 400    | `{"error": "Invalid image ID"}`           |
| `GET /images/<img_id>`  | 404    | `{"error": "Image not found"}`    |

### Example for how to programatically to request data from the microservice:
```py
import requests
from PIL import Image
from io import BytesIO

image_id = "40290"
url = f"http://localhost:5001/images/{image_id}"

response = requests.get(url)

if response.status_code == 200:
    image = Image.open(BytesIO(response.content))
    image.show()

    print("Image retrieved and displayed successfully!")

else:
    print("Error:", response.status_code)
    print(response.json())
```

## To receive data from the microservice:
- Data is received via HTTP POST requests. When you press the "Upload" button on the form, it sends a POST request to the microservice for the image file to be processed and stored

| Request                    | Status | Body                                                        |
| -------------------------- | ------ | ----------------------------------------------------------- |
| `POST /images`           | 201    |  JSON containing image ID and success message|
| `POST /images`  | 400    | `{"error": "Only JPG and PNG file types allowed!}`           |
| `POST /images`  | 400    | `{"error": "No image added"}`    |

### Example for how to programatically to receive data from the microservice:
```py
import requests

url = "http://localhost:5001/images"

with open("example.jpg", "rb") as image:
    response = requests.post(
        url,
        files={"file": image}
    )
if response.status_code == 201:
    data = response.json()
    print("Image ID:", data["imageID"])
    print("Message:", data["message"])

else:
    print("Error:", response.json())

```

# Test against the spec

The API is described in `openapi.json`. To check the running service against it with
[Schemathesis](https://schemathesis.readthedocs.io), start it (`docker compose up --build -d image-service`),
then from the repo root:

```sh
# upload a real image first, so GET and DELETE have an imageID that exists
export IMAGE_ID=$(curl -s -F file=@image_service/imgservice_UML.png http://localhost:5001/images \
  | python3 -c 'import json, sys; print(json.load(sys.stdin)["imageID"])')

uvx schemathesis --config-file image_service/schemathesis.toml run image_service/openapi.json --url http://localhost:5001
```

Without `IMAGE_ID`, every random ID Schemathesis tries is an image that doesn't exist,
so GET and DELETE only ever return 404 and it warns about "missing test data".

# Image Microservice UML Diagram:
![Image Service UML Diagram](imgservice_UML.png)