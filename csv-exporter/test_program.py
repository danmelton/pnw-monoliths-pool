# Test program for the CSV Exporter
# start the service first (from the repo root): docker compose up --build -d csv-exporter
# then run this from the csv-exporter folder: python test_program.py
#
# this only talks to the service over HTTP, it doesn't import main.py or converter.py
# since microservices aren't allowed to call each other's code directly

import csv
import io
import json
import urllib.error
import urllib.request

URL = "http://localhost:3002/export"

passed = 0
failed = 0


# sends a POST to the exporter and gives back (status, headers, body text)
def send_request(body_text):
    request = urllib.request.Request(URL, data=body_text.encode("utf-8"),
                                     headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(request) as response:
            return response.status, response.headers, response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        # urllib counts a 400 as an error but we still want to read what came back
        return error.code, error.headers, error.read().decode("utf-8")


def check(description, result):
    global passed, failed
    if result:
        print("  PASS", description)
        passed += 1
    else:
        print("  FAIL", description)
        failed += 1


# make sure the service is actually running first
try:
    send_request("{}")
except urllib.error.URLError:
    print("Could not reach the CSV Exporter at " + URL)
    print("Start it with: docker compose up --build -d csv-exporter")
    raise SystemExit


print("=== Story 1: JSON records to CSV ===")
body = {"data": [{"date": "2026-11-01", "exercise": "Squat", "reps": 10},
                 {"date": "2026-11-02", "exercise": "Bench Press", "reps": 8}]}
status, headers, text = send_request(json.dumps(body))
print(text)
check("returns 200", status == 200)
check("Content-Type is text/csv", "text/csv" in headers["Content-Type"])
check("first line is the header row", text.startswith("date,exercise,reps\r\n"))
check("rows are in the same order as the input",
      text == "date,exercise,reps\r\n2026-11-01,Squat,10\r\n2026-11-02,Bench Press,8\r\n")

print("=== Story 1: records with different fields ===")
body = {"data": [{"date": "2026-11-01", "exercise": "Squat"},
                 {"date": "2026-11-02", "notes": "felt strong"}]}
status, headers, text = send_request(json.dumps(body))
print(text)
check("header has every field in the order it shows up", text.startswith("date,exercise,notes\r\n"))
check("missing fields are empty cells", "2026-11-01,Squat,\r\n" in text and "2026-11-02,,felt strong" in text)

print("=== Story 2: choose columns and file name ===")
body = {"data": [{"date": "2026-11-01", "exercise": "Squat", "reps": 10}],
        "columns": ["exercise", "reps"],
        "filename": "workouts_nov.csv"}
status, headers, text = send_request(json.dumps(body))
print(text)
check("only the chosen columns, in that order", text.startswith("exercise,reps\r\n"))
check("file name is in Content-Disposition", headers["Content-Disposition"] == 'attachment; filename="workouts_nov.csv"')

print("=== Story 2: default file name ===")
status, headers, text = send_request(json.dumps({"data": [{"date": "2026-11-01"}]}))
check("file name defaults to export.csv", 'filename="export.csv"' in headers["Content-Disposition"])

print("=== Story 3: commas, quotes, and line breaks ===")
records = [{"note": 'She said "hi", then left'}, {"note": "line one\nline two"}]
status, headers, text = send_request(json.dumps({"data": records}))
print(text)
check("quotes get doubled and the value gets wrapped in quotes", '"She said ""hi"", then left"' in text)
# read the csv back with python's csv module, should match what we sent
rows = list(csv.reader(io.StringIO(text)))
check("reading the CSV back gives the same values", rows[1][0] == records[0]["note"] and rows[2][0] == records[1]["note"])

print("=== Story 3: nested values ===")
body = {"data": [{"exercise": {"name": "Squat"}, "reps": [10, 8, 6]}]}
status, headers, text = send_request(json.dumps(body))
print(text)
check("nested object turns into a dotted column", text.startswith("exercise.name,reps\r\n"))
check("list goes in one cell", "Squat,10;8;6" in text)

print("=== Story 3: values that look like formulas ===")
body = {"data": [{"a": "=SUM(A1:A9)", "b": "+1", "c": "-cmd", "d": "@x", "e": "normal", "f": -5}]}
status, headers, text = send_request(json.dumps(body))
print(text)
check("text starting with = + - @ gets a ' in front", "'=SUM(A1:A9),'+1,'-cmd,'@x" in text)
check("normal text and numbers don't change", text.endswith(",normal,-5\r\n"))

print("=== Story 3: body isn't valid JSON ===")
status, headers, text = send_request("this is not json")
print(text)
check("returns 400", status == 400)
check("error is INVALID_INPUT", json.loads(text)["error"] == "INVALID_INPUT")

print("=== Story 3: data is an empty list ===")
status, headers, text = send_request(json.dumps({"data": []}))
print(text)
check("returns 400", status == 400)
check("error is EMPTY_DATA", json.loads(text)["error"] == "EMPTY_DATA")

print("=== Story 3: data isn't a list of objects ===")
status, headers, text = send_request(json.dumps({"data": [1, 2, 3]}))
print(text)
check("returns 400", status == 400)
check("message says what went wrong", json.loads(text)["message"] == "data must be an array of objects")

print()
print(f"{passed} passed, {failed} failed")
