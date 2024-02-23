# PyNdef

![!python-versions](https://img.shields.io/badge/Python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue)
![Pypi](https://img.shields.io/pypi/v/pyndef?color=orange)

[![codecov](https://codecov.io/gh/XFY9326/PyNdef/graph/badge.svg?token=QVJNICD0GA)](https://codecov.io/gh/XFY9326/PyNdef)
[![Test](https://github.com/XFY9326/PyNdef/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/XFY9326/PyNdef/actions/workflows/test.yml)
[![Release](https://github.com/XFY9326/PyNdef/actions/workflows/release.yml/badge.svg?branch=master)](https://github.com/XFY9326/PyNdef/actions/workflows/release.yml)

Pure Python library for creating and parsing NDEF messages.  
All codes in this repository are referred to AOSP NDEF implementation.

## Features

- Pure Python implementation (>=3.6)
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

## Reference

```
/platform/frameworks/base/nfc/java/android/nfc/NdefRecord.java
/platform/frameworks/base/nfc/java/android/nfc/NdefMessage.java
/cts/tests/tests/ndef/src/android/ndef/cts/NdefTest.java
```

## License

```
   Copyright 2024 XFY9326

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
```
