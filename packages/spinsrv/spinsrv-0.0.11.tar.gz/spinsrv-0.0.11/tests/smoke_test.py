from spinsrv import spinpy as sp
from spinsrv import spin
import json
import hashlib

print("THIS IS SMOKE TEST 1: IT TESTS THE CLIENTS IN src/spin/spinpy.py")

kc = sp.KeyServerHTTPClient()
resp = kc.which(
    spin.KeyWhichRequest(
        public="proteins",
        private="proteins",
    )
)
print(resp)
resp = kc.temp(
    spin.KeyTempRequest(
        public="proteins",
        private="proteins",
        duration=60000000000,
    )
)
print(resp)

dc = sp.DirServerHTTPClient()
resp = dc.lookup(
    spin.DirLookupRequest(
        public="proteins", private="proteins", citizen="proteins", path="/"
    )
)
print(resp)
resp = dc.tree(
    spin.DirTreeRequest(
        public="proteins", private="proteins", citizen="proteins", path="/", level=1
    )
)
print(resp)

resp = dc.apply(
    spin.DirApplyRequest(
        public="proteins",
        private="proteins",
        ops=[
            spin.DirOp(
                operation=spin.PutDirOperation,
                dir_entry=spin.DirEntry(
                    type=spin.EntryDir,
                    citizen="proteins",
                    path="/test",
                    sequence=spin.SeqIgnore,
                ),
            )
        ],
    )
)
print(resp)

bc = sp.BitServerHTTPClient()
data = "Asdf".encode()
resp = bc.apply(
    spin.BitApplyRequest(
        public="proteins",
        private="proteins",
        ops=[
            spin.BitOp(
                operation=spin.PutBitOperation,
                ref=spin.SHA256(data),
                bytes=data,
            )
        ],
    )
)
print(resp)
