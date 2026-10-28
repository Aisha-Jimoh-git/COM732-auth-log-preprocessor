from log_reader import read_log_file


log_lines = read_log_file("sample_data/auth.log")

for line in log_lines:
    print(line.strip())