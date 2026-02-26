factor = 9.7/9.5
val = 6.4
scaled = val / factor
rounded = round(scaled, 1)
print("6.4/factor = {:.10f}".format(scaled))
print("round = {}".format(rounded))
old_str = "{:.1f}".format(val)
new_str = "{:.1f}".format(rounded)
print("old_str = {}".format(old_str))
print("new_str = {}".format(new_str))
print("changed = {}".format(old_str != new_str))
