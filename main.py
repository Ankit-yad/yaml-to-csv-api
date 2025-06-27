# from fastapi import FastAPI, UploadFile, File
# from fastapi.responses import StreamingResponse
# import yaml
# import csv
# import io

# app = FastAPI()


# def parse_yaml_to_csv(yaml_content: str) -> io.BytesIO:
#     documents = list(yaml.safe_load_all(yaml_content))
    
#     merged_data = []
#     for doc in documents:
#         if isinstance(doc, list):
#             merged_data.extend(doc)
#         elif isinstance(doc, dict):
#             merged_data.append(doc)
#         else:
#             continue

#     if not merged_data:
#         raise ValueError("No valid data found in YAML")

#     # Get headers
#     headers = set()
#     for item in merged_data:
#         headers.update(item.keys())
#     headers = list(headers)

#     # Write to CSV in memory
#     csv_stream = io.StringIO()
#     writer = csv.DictWriter(csv_stream, fieldnames=headers)
#     writer.writeheader()
#     writer.writerows(merged_data)

#     # Convert to BytesIO
#     result = io.BytesIO()
#     result.write(csv_stream.getvalue().encode())
#     result.seek(0)
#     return result


# @app.post("/convert/")
# async def convert_yaml_to_csv(file: UploadFile = File(...)):
#     content = await file.read()
#     try:
#         csv_stream = parse_yaml_to_csv(content.decode())
#     except Exception as e:
#         return {"error": str(e)}

#     return StreamingResponse(
#         csv_stream,
#         media_type="text/csv",
#         headers={"Content-Disposition": "attachment; filename=converted.csv"}
#     )






from module.converter import yaml_to_csv_stream

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/convert/")
async def convert_yaml(file: UploadFile = File(...)):
    content = await file.read()
    try:
        csv_stream = yaml_to_csv_stream(content.decode())
    except Exception as e:
        return {"error": str(e)}

    return StreamingResponse(
        csv_stream,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=converted.csv"}
    )
