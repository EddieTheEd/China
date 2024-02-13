import io

main = {}

file = io.open("cedict_ts.u8", mode="r", encoding = "utf-8")
for string in file.read().split("\n"):
    print(string)

