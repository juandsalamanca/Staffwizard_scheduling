def order_rate_and_distance(ordered_employees):
  OT_groups = {}
  for emp in ordered_employees:
    d_ot = emp["weekly_time"]
    if d_ot not in OT_groups:
      OT_groups[d_ot] = []
    OT_groups[d_ot].append(emp)
  final_sorted_list = []
  for ot in OT_groups:
    group = OT_groups[ot]
    sorted_group = sorted(group, key=lambda x: x["score"])
    for employee in sorted_group:
      final_sorted_list.append(employee)
  return final_sorted_list
