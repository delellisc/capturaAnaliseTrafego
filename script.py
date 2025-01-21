with open("./input.csv", "r") as input, open("./teste1.csv", "r") as f1, open("./teste2.csv", "r") as f2:
    input_lines = input.readlines()
    f1_lines = f1.readlines()
    f2_lines = f2.readlines()
with open("./output.csv", "w") as output:
    for line1, line2, input_line in zip(f1_lines, f2_lines, input_lines):
        output.write(f"{input_line.strip()}, {line1.strip()}, {line2.strip()}\n")

