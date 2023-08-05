from spinsrv import spinfs

print(
    "THIS IS SMOKE TEST 2: IT TESTS (primarily directory related) functionality of src/spin/spinfs.py"
)

fs = spinfs.SpinFileSystem(
    spinfs.Config(public="proteins", private="proteins", citizen="proteins")
)

resp = fs.ls("/")
print(resp)

resp = fs.makedirs("/this/a/test")
print(resp)

resp = fs.rm_file("/this/a/test")
print(resp)

resp = fs.touch("/this/a/test.txt")
print(resp)

assert fs.exists("/this/a/test.txt")
assert fs.isfile("/this/a/test.txt")
assert fs.cat("/this/a/test.txt") == b""
resp = fs.copy("/this/a/test.txt", "/this/a/copy.txt")
print(resp)
out = {x: True for x in fs.ls("/this/a", detail=False)}
assert "/this/a/test.txt" in out, f"out was {out}"
assert "/this/a/copy.txt" in out, f"out was {out}"
resp = fs.rm("/this/a", recursive=True)
print(resp)
