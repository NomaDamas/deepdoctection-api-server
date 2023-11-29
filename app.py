import os
from http import HTTPStatus
from typing import List, Dict, Union, Any

from fastapi.middleware.cors import CORSMiddleware

import deepdoctection as dd
from fastapi import FastAPI, File, UploadFile

app = FastAPI(title="DeepDoctection API")
origins = ["http://localhost", "http://127.0.0.1"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    response = {
        "status-code": HTTPStatus.OK,
        "data": {},
    }
    return response


@app.post("/extract")
async def extract(file: UploadFile = File(...)) -> List[Dict[str, Union[Union[int, List[str], List[Any]], Any]]]:
    analyzer = dd.get_dd_analyzer()
    # Save the uploaded file to a temporary location
    with open(file.filename, 'wb+') as out_file:
        out_file.write(await file.read())
        
    # Get the file path
    file_path = os.path.abspath(file.filename)

    # Analyze the file
    df = analyzer.analyze(path=file_path)

    # Don't forget to remove the file if it's no longer needed
    os.remove(file_path)
    
    df.reset_state()
    doc = iter(df)

    pages_result = []
    for i, page in enumerate(doc):
        title = []
        for layout in page.layouts:
            if layout.category_name == "title":
                title.append(f"{layout.text}")
                # title = layout.text
        text = page.text
        tables = page.tables or []
        tables_html = [table.html for table in tables]
        page_result = {
            "page_number": i + 1,
            "title": title,
            "text": text,
            "table": tables_html,
        }
        pages_result.append(page_result)
    return pages_result


def main():
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0" ,port=8000)


if __name__ == "__main__":
    main()
