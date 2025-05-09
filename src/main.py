from flask import Flask, request, jsonify
from get_info_from_api import *
from permanent_shifts import *
from assign_permenent_shifts import *
from compatible_employees_for_posts import *
from overlapp import *
from assign_shifts import *
from empty_posts import *
from calculate_overtime import *
from summary import *
import os
import traceback


openai_key='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'
os.environ["OPENAI_API_KEY"]=openai_key

app = Flask(__name__)

@app.route("/get_schedule", methods=['POST'])
def get_schedule():
    try:
        # Check if JSON is valid and Content-Type is correct
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON or missing 'Content-Type: application/json' header"}), 400
        else:
            subdomain = data["subdomain"]
            branch = data["branch"]
            beginning = data["start"]
            end = data["end"]
            mode = data["mode"]

        employees, future_employees, clients, future_clients = get_info_from_api(subdomain, branch, beginning, end)
        if len(clients[0]["posts"][0]["weeks_periods"]) == 0:
            return jsonify({"Error": "No shifts available for the prior week"})
        if len(future_clients[0]["posts"][0]["weeks_periods"]) == 0:
            return jsonify({"Error": "No shifts available for the selected week"})

        permanent_shifts = scan_permanent_shifts(employees)
        new_permanent_shifts, shift_ids = map_permanent_shifts(permanent_shifts=permanent_shifts, future_clients=future_clients)
        permanent_shifts_by_employee, permanent_shift_ids = assign_permanent_shifts(clients=future_clients, future_employees=future_employees, permanent_shift_ids=shift_ids)
        compatible_posts = get_compatibile_employees_for_posts(employees=future_employees, clients=future_clients, permanent=permanent_shifts_by_employee, beta=1)
        clean_posts = eliminate_empty_posts(compatible_posts)
        assigned_posts, assigned_employees, empty_shifts = assign_shifts(posts = clean_posts, employees = future_employees, permanent_shifts_by_employee = permanent_shifts_by_employee, permanent_shift_ids = permanent_shift_ids)
        final_ot_employees = calculate_final_overtime(assigned_employees)
        final_ot_employee_names = match_empid_with_empname(final_ot_employees, future_employees)
        summary_data = generate_data_for_summary(final_ot_employee_names)
        summary = get_final_summary(summary_data, mode)

        return jsonify({"Posts": assigned_posts, "Employees": assigned_employees, "Summary": (summary_data, summary), "Empty": empty_shifts})

    except Exception as e:

        return jsonify({"Error": str(e)})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
