from openai import OpenAI

def match_empid_with_empname(employee_shift_time, future_employees):
  emp_name_shift_time = {}
  for emp_id in employee_shift_time:
    for employee in future_employees:
      id = employee["employee_id"]
      if id == emp_id:
        name = employee["employee_name"]
        emp_name_shift_time[name] = employee_shift_time[id]

  return emp_name_shift_time

def generate_data_for_summary(final_employees):
  info_string = ""
  for emp_id in final_employees:
    employee = final_employees[emp_id]
    total_t = employee['total_shift_time']
    info_string += f"For Employee {emp_id} the total weekly shift time is {total_t} \n"
    if "daily_OT" in employee:
      daily_ot_list = employee["daily_OT"]
      for day in daily_ot_list:
        info_string += f"For Employee {emp_id} the daily shift time is {daily_ot_list[day]} \n"
  return info_string


def get_final_summary(text, mode):

  client = OpenAI()
  content = f"""I need you to read this text: {text}. It's about the shifts and work time for the week assigned to some employees.
      I want you to write a summary of this information that includes the any weekly overtime (>40hrs) for any employee if they have some or
      any daily overtime (>8hrs) if it exists. The goal of this schedule was to optimize for overtime (minimize it) so highlight infomration accordingly.
      """
  if mode == "informal":
    content = content + "Try to make it no so formal, more in a storytelling kind of way"

  try:
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You're a useful assistant, editing texts according to precise instructions"},
        {"role": "user", "content": content}
      ]
    )
    return completion.choices[0].message.content

  except Exception as e:
    return "Error:" + str(e)
