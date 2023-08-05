## Overview
OCR Meter Reading
## Setup
`conda create -n ocr_meter python=3.8`

`conda activate ocr_meter`

`pip install ocr-meter==0.0.6`

Example code:
```
from ocr import ocr
img_path = "tests/meter/5/1.png"
ocr_meter = ocr.OcrMeter()
# num_digit: number black digits
# meter_type choice in (water, electicity, gas)
ocr_meter.inference_single(img_path, num_digit=5, meter_type="water")
```