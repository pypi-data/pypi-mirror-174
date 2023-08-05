from spinsrv import spinfs

print(
    "THIS IS SMOKE TEST 3: IT TESTS (primarily file related) functionality of src/spin/spinfs.py"
)

fs = spinfs.SpinFileSystem(
    spinfs.Config(public="proteins", private="proteins", citizen="proteins")
)
f = fs.open("/notes.txt", "wb")
f.write(b"Hello world!")
f.close()
f = fs.open("/notes.txt", "rb")
b = f.read()
assert b == b"Hello world!", f"got {b}, wanted Hello world!"
