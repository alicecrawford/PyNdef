# PyNdef

![!python-versions](https://img.shields.io/badge/Python-3.10-blue)

Pure Python library for creating and parsing NDEF messages.  
All codes in this repository are referred to AOSP NDEF implementation.

## Features

- Pure Python implementation (>=3.10)
- No 3rd party dependency
- With tests
- Similar to AOSP NDEF implementation
- Full type hint
- Single file

## Usage

```python
from pyndef import NdefMessage, NdefRecord, NdefTNF, NdefRTD

r1 = NdefRecord(NdefTNF.EMPTY, None, None, None)
print(r1)

r2 = NdefRecord(NdefTNF.EXTERNAL_TYPE, b"type", b"\x01", b"\x01\x02\x03")
print(r2)

r3 = NdefRecord.create_uri("https://www.github.com")
print(r3)

r4 = NdefRecord(NdefTNF.WELL_KNOWN, NdefRTD.SMART_POSTER, None, r3.to_bytes())
print(r4)

msg = NdefMessage(r2, r3)
print(msg)

msg = NdefMessage.parse(b"\xd8\x00\x00\x00")
print(msg)
```

# Reference

```
/platform/frameworks/base/nfc/java/android/nfc/NdefRecord.java
/platform/frameworks/base/nfc/java/android/nfc/NdefMessage.java
/cts/tests/tests/ndef/src/android/ndef/cts/NdefTest.java
```
