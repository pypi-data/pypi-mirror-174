## Overview
OCR Meter Reading
## Setup
`conda create -n ocr_license python=3.7`

`conda activate ocr_license`

`pip install ocr-license==0.0.2`

Example code:
```
from ocr import ocr_license
img_path = "tests/1.png"
ocr = ocr_license.OcrLicense()
# license_type choice in (my_number_card, driver_license)
ocr.inference_single(img_path, license_type="my_number_card")
```