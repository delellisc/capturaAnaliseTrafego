with open("./csv/captura_exportada2.csv", "r") as input, open("./csv/tempo", "r") as f1, open("./csv/porta_origem", "r") as f2:
    input_lines = input.readlines()
    f1_lines = f1.readlines()
    f2_lines = f2.readlines()
with open("./csv/captura_alterada.csv", "w") as captura_alterada:
    for line1, line2, input_line in zip(f1_lines, f2_lines, input_lines):
        captura_alterada.write(f"{input_line.strip()}, {line1.strip()}, {line2.strip()}\n")