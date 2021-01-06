import os

# zpgk

# KANNST DU VERÄNDERN
root = r"\\srilch4\Projekte"
file_max_length = 241
# BITTE NICHT MEHR VERÄNDERN

def find():
    os.system(r"net use P: \\srilch4\Projekte ilchmI04 /user:administrator")
    for path, _, files in os.walk(root):
        for name in files:
            if len(os.path.join(path, name)) > file_max_length:
                print(os.path.join(path, name))

find()
print("\nDONE")
input()

# \\192.168.4.133\Dateigrab z
# \\srilch4\Projekte p
# \\srilch4\daten k
# \\srilch4\gl g