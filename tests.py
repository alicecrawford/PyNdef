import unittest

from pyndef import NdefRecord, NdefMessage, NdefTNF, NdefRTD


# /cts/tests/tests/ndef/src/android/ndef/cts/NdefTest.java
class NdefTestCase(unittest.TestCase):
    _PAYLOAD_255 = b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08" + \
                   b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08" + \
                   b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08" + \
                   b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08" + \
                   b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08" + \
                   b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08" + \
                   b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08" + \
                   b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07"
    _PAYLOAD_256 = b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08" + \
                   b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08" + \
                   b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08" + \
                   b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08" + \
                   b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08" + \
                   b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08" + \
                   b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08" + \
                   b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08"

    def test_constructor(self) -> None:
        r = NdefRecord(NdefTNF.EMPTY, None, None, None)
        self.assertEqual(bytes(), r.record_id)
        self.assertEqual(bytes(), r.record_type)
        self.assertEqual(bytes(), r.payload)
        self.assertEqual(NdefTNF.EMPTY, r.tnf)
        self.assertRaises(ValueError, NdefMessage)
        self.assertRaises(ValueError, NdefRecord, NdefTNF.UNKNOWN, b"type", None, None)
        self.assertRaises(ValueError, NdefRecord, NdefTNF.RESERVED, b"type", None, None)
        self.assertRaises(ValueError, NdefRecord, NdefTNF.UNCHANGED, None, None, None)

    def test_equals(self) -> None:
        self.assertEqual(NdefRecord(NdefTNF.EMPTY, None, None, None),
                         NdefRecord(NdefTNF.EMPTY, None, None, None))
        self.assertEqual(NdefRecord(NdefTNF.EXTERNAL_TYPE, b"\x01\x02\x03", b"\x04\x05\x06", b"\x07\x08\x09"),
                         NdefRecord(NdefTNF.EXTERNAL_TYPE, b"\x01\x02\x03", b"\x04\x05\x06", b"\x07\x08\x09"))
        self.assertNotEqual(NdefRecord(NdefTNF.EXTERNAL_TYPE, b"\x01\x02\x03", b"\x04\x05\x06", b"\x07\x08\x09"),
                            NdefRecord(NdefTNF.EXTERNAL_TYPE, b"\x01\x02\x03", b"\x04\x05\x06", b"\x07\x08\x09\x10"))
        self.assertEqual(NdefMessage(NdefRecord(NdefTNF.EXTERNAL_TYPE, b"\x01\x02\x03", b"\x04\x05\x06", b"\x07\x08\x09")),
                         NdefMessage(NdefRecord(NdefTNF.EXTERNAL_TYPE, b"\x01\x02\x03", b"\x04\x05\x06", b"\x07\x08\x09")))
        self.assertNotEqual(NdefMessage(NdefRecord(NdefTNF.EXTERNAL_TYPE, b"\x01\x02\x03", b"\x04\x05\x06", b"\x07\x08\x09")),
                            NdefMessage(NdefRecord(NdefTNF.EXTERNAL_TYPE, b"\x01\x02\x03", b"\x04\x05\x06", b"\x07\x08\x09\x10")))
        self.assertNotEqual(NdefMessage(NdefRecord(NdefTNF.EXTERNAL_TYPE, b"\x01\x02\x03", b"\x04\x05\x06", b"\x07\x08\x09")),
                            NdefMessage(NdefRecord(NdefTNF.EXTERNAL_TYPE, b"\x01\x02\x03", b"\x04\x05\x06", b"\x07\x08\x09"),
                                        NdefRecord(NdefTNF.EMPTY, None, None, None)))
        self.assertEqual(hash(NdefRecord(NdefTNF.EMPTY, None, None, None)),
                         hash(NdefRecord(NdefTNF.EMPTY, None, None, None)))
        self.assertEqual(hash(NdefMessage(NdefRecord(NdefTNF.EXTERNAL_TYPE, b"\x01\x02\x03", b"\x04\x05\x06", b"\x07\x08\x09"))),
                         hash(NdefMessage(NdefRecord(NdefTNF.EXTERNAL_TYPE, b"\x01\x02\x03", b"\x04\x05\x06", b"\x07\x08\x09"))))
        self.assertNotEqual(NdefRecord(NdefTNF.EMPTY, None, None, None), None)
        self.assertNotEqual(NdefMessage(NdefRecord(NdefTNF.EMPTY, None, None, None)), None)

    def test_invalid_parsing(self) -> None:
        # noinspection GrazieInspection
        invalid_ndef_messages = [
            b"",  # too short
            b"\xd0",  # too short
            b"\xd0\x00",  # too short
            b"\xd0\x00\x00\x00\x00",  # too long
            b"\x50\x00\x00",  # missing MB
            b"\x90\x00\x00",  # missing ME
            b"\xc0\x00\x00\x00"  # long record, too short
            b"\xc0\x00\x00\x00\x00",  # long record, too short
            b"\xc0\x00\x00\x00\x00\x00\x00",  # long record, too long
            b"\xd8\x01\x03\x01\x00\x00\x00\x00",  # SR w/ payload&type&id, too short
            b"\xd8\x01\x03\x01\x00\x00\x00\x00\x00\x00",  # SR w/ payload&type&id, too long
            b"\xd8\x00\x00\x01\x00",  # TNF_EMPTY cannot have id field
            b"\x90\x00\x00\x10\x00\x00",  # 2 records, missing ME
            b"\xf5\x00\x00",  # CF and ME set
            b"\xd6\x00\x00",  # TNF_UNCHANGED without chunking
            b"\xb6\x00\x01\x01\x56\x00\x01\x02",  # TNF_UNCHANGED in first chunk
            b"\xc5\x00\xff\xff\xff\xff",  # heap-smash check
        ]
        for buffer in invalid_ndef_messages:
            try:
                self.assertRaises(ValueError, NdefMessage.parse, buffer)
            except AssertionError as e:
                raise AssertionError(f"expected ValueError for input {buffer}") from e

    def test_valid_parsing(self) -> None:
        # short record
        self.assertEqual(NdefMessage(NdefRecord(NdefTNF.EMPTY, None, None, None)),
                         NdefMessage.parse(b"\xd0\x00\x00"))
        # full length record
        self.assertEqual(NdefMessage(NdefRecord(NdefTNF.EMPTY, None, None, None)),
                         NdefMessage.parse(b"\xc0\x00\x00\x00\x00\x00"))
        # SR with ID flag and 0-length id
        self.assertEqual(NdefMessage(NdefRecord(NdefTNF.EMPTY, None, None, None)),
                         NdefMessage.parse(b"\xd8\x00\x00\x00"))
        # SR with ID flag and 1-length id
        self.assertEqual(NdefMessage(NdefRecord(NdefTNF.WELL_KNOWN, None, b"\x00", None)),
                         NdefMessage.parse(b"\xd9\x00\x00\x01\x00"))
        # ID flag and 1-length id
        self.assertEqual(NdefMessage(NdefRecord(NdefTNF.WELL_KNOWN, None, b"\x00", None)),
                         NdefMessage.parse(b"\xc9\x00\x00\x00\x00\x00\x01\x00"))
        # SR with payload
        self.assertEqual(NdefMessage(NdefRecord(NdefTNF.WELL_KNOWN, None, None, b"\x01\x02\x03")),
                         NdefMessage.parse(b"\xd1\x00\x03\x01\x02\x03"))
        # SR with payload and type
        self.assertEqual(NdefMessage(NdefRecord(NdefTNF.WELL_KNOWN, b"\x09", None, b"\x01\x02\x03")),
                         NdefMessage.parse(b"\xd1\x01\x03\x09\x01\x02\x03"))
        # SR with payload, type and id
        self.assertEqual(NdefMessage(NdefRecord(NdefTNF.WELL_KNOWN, b"\x08", b"\x09", b"\x01\x02\x03")),
                         NdefMessage.parse(b"\xd9\x01\x03\x01\x08\x09\x01\x02\x03"))
        # payload, type and id
        self.assertEqual(NdefMessage(NdefRecord(NdefTNF.WELL_KNOWN, b"\x08", b"\x09", b"\x01\x02\x03")),
                         NdefMessage.parse(b"\xc9\x01\x00\x00\x00\x03\x01\x08\x09\x01\x02\x03"))
        # 2 records
        self.assertEqual(NdefMessage(
            NdefRecord(NdefTNF.EMPTY, None, None, None),
            NdefRecord(NdefTNF.EMPTY, None, None, None)),
            NdefMessage.parse(b"\x90\x00\x00\x50\x00\x00")
        )
        # 3 records
        self.assertEqual(NdefMessage(
            NdefRecord(NdefTNF.EMPTY, None, None, None),
            NdefRecord(NdefTNF.EMPTY, None, None, None),
            NdefRecord(NdefTNF.EMPTY, None, None, None)),
            NdefMessage.parse(b"\x90\x00\x00\x10\x00\x00\x50\x00\x00")
        )
        # chunked record (2 chunks)
        self.assertEqual(NdefMessage(
            NdefRecord(NdefTNF.UNKNOWN, None, None, b"\x01\x02")),
            NdefMessage.parse(b"\xb5\x00\x01\x01\x56\x00\x01\x02")
        )
        # chunked record (3 chunks)
        self.assertEqual(NdefMessage(
            NdefRecord(NdefTNF.UNKNOWN, None, None, b"\x01\x02")),
            NdefMessage.parse(b"\xb5\x00\x00\x36\x00\x01\x01\x56\x00\x01\x02")
        )
        # chunked with id and type
        self.assertEqual(NdefMessage(NdefRecord(NdefTNF.MIME_MEDIA, b"\x08", b"\x09", b"\x01\x02")),
                         NdefMessage.parse(b"\xba\x01\x00\x01\x08\x09\x36\x00\x01\x01\x56\x00\x01\x02"))
        # 3 records, 7 chunks
        self.assertEqual(NdefMessage(
            NdefRecord(NdefTNF.EXTERNAL_TYPE, b"\x21", None, b"\x01\x02\x03\x04"),
            NdefRecord(NdefTNF.EMPTY, None, None, None),
            NdefRecord(NdefTNF.MIME_MEDIA, b"\x21", None, b"\x11\x12\x13\x14")),
            NdefMessage.parse(b"\xb4\x01\x01\x21\x01\x36\x00\x02\x02\x03\x16\x00\x01\x04" +
                              b"\x10\x00\x00"
                              b"\x32\x01\x02\x21\x11\x12\x36\x00\x01\x13\x56\x00\x01\x14")
        )
        # 255 byte payload
        self.assertEqual(NdefMessage(
            NdefRecord(NdefTNF.UNKNOWN, None, None, self._PAYLOAD_255)),
            NdefMessage.parse(b"\xc5\x00\x00\x00\x00\xff" + self._PAYLOAD_255)
        )
        # 256 byte payload
        self.assertEqual(NdefMessage(
            NdefRecord(NdefTNF.UNKNOWN, None, None, self._PAYLOAD_256)),
            NdefMessage.parse(b"\xc5\x00\x00\x00\x01\x00" + self._PAYLOAD_256)
        )
        # 255 byte type
        self.assertEqual(NdefMessage(
            NdefRecord(NdefTNF.MIME_MEDIA, self._PAYLOAD_255, None, None)),
            NdefMessage.parse(b"\xd2\xff\x00" + self._PAYLOAD_255)
        )
        # 255 byte id
        self.assertEqual(NdefMessage(
            NdefRecord(NdefTNF.MIME_MEDIA, None, self._PAYLOAD_255, None)),
            NdefMessage.parse(b"\xda\x00\x00\xff" + self._PAYLOAD_255)
        )
        # NdefRecord parsing ignores incorrect MB
        self.assertEqual(NdefRecord(NdefTNF.EMPTY, None, None, None),
                         NdefRecord.parse(b"\x50\x00\x00")[0])
        # NdefRecord parsing ignores incorrect ME
        self.assertEqual(NdefRecord(NdefTNF.EMPTY, None, None, None),
                         NdefRecord.parse(b"\x90\x00\x00")[0])
        # NdefRecord parsing can handle chunking with incorrect MB, ME
        self.assertEqual(NdefRecord(NdefTNF.UNKNOWN, None, None, b"\x01\x02"),
                         NdefRecord.parse(b"\x35\x00\x01\x01\x16\x00\x01\x02")[0])
        # A Smart Poster containing a URL and no text (nested NDEF Messages)
        self.assertEqual(NdefMessage(
            NdefRecord(NdefTNF.WELL_KNOWN, NdefRTD.SMART_POSTER, None, NdefMessage(NdefRecord.create_uri("http://www.google.com")).to_bytes())),
            NdefMessage.parse(b"\xd1\x02\x0f\x53\x70\xd1" +
                              b"\x01\x0b\x55\x01\x67\x6f" +
                              b"\x6f\x67\x6c\x65\x2e\x63" +
                              b"\x6f\x6d")
        )

    def test_create_uri(self) -> None:
        self.assertEqual(
            b"\xd1\x01\x08U\x01nfc.com",
            NdefMessage(NdefRecord.create_uri("http://www.nfc.com")).to_bytes()
        )
        self.assertEqual(
            b"\xd1\x01\x0dU\x05+35891234567",
            NdefMessage(NdefRecord.create_uri("tel:+35891234567")).to_bytes()
        )
        self.assertEqual(
            b"\xd1\x01\x04U\x00foo",
            NdefMessage(NdefRecord.create_uri("foo")).to_bytes()
        )
        self.assertEqual(
            b"\xd1\x01\x03U\x00\xc2\xa2",
            NdefMessage(NdefRecord.create_uri("\u00a2")).to_bytes()
        )

    def test_create_mime(self) -> None:
        self.assertEqual(
            NdefRecord(NdefTNF.MIME_MEDIA, b"text/plain", None, b"foo"),
            NdefRecord.create_mime("text/plain", b"foo")
        )
        self.assertRaises(ValueError, NdefRecord.create_mime, "", None)
        self.assertRaises(ValueError, NdefRecord.create_mime, "/", None)
        self.assertRaises(ValueError, NdefRecord.create_mime, "a/", None)
        self.assertRaises(ValueError, NdefRecord.create_mime, "/b", None)
        # The following are valid MIME types and should not throw
        NdefRecord.create_mime("foo/bar", None)
        NdefRecord.create_mime("   ^@#/*   ", None)
        NdefRecord.create_mime("text/plain; charset=us_ascii", None)

    def test_create_external(self) -> None:
        self.assertRaises(ValueError, NdefRecord.create_external, "", "c", None)
        self.assertRaises(ValueError, NdefRecord.create_external, "a", "", None)
        self.assertRaises(ValueError, NdefRecord.create_external, "   ", "c", None)
        self.assertEqual(
            NdefRecord(NdefTNF.EXTERNAL_TYPE, b"a.b:c", None, None),
            NdefRecord.create_external("a.b", "c", None)
        )
        # test force lowercase
        self.assertEqual(
            NdefRecord(NdefTNF.EXTERNAL_TYPE, b"a.b:c!", None, None),
            NdefRecord.create_external("A.b", "C!", None)
        )

    def test_create_application_record(self) -> None:
        # some failure cases
        self.assertRaises(ValueError, NdefRecord.create_application_record, None)
        self.assertRaises(ValueError, NdefRecord.create_application_record, "")
        # create an AAR
        r = NdefRecord.create_application_record("com.foo.bar")
        aar = b"\xd4\x0f\x0b\x61" + \
              b"\x6e\x64\x72\x6f" + \
              b"\x69\x64\x2e\x63" + \
              b"\x6f\x6d\x3a\x70" + \
              b"\x6b\x67\x63\x6f" + \
              b"\x6d\x2e\x66\x6f" + \
              b"\x6f\x2e\x62\x61" + \
              b"\x72"
        self.assertEqual(aar, r.to_bytes())
        rs = NdefMessage.parse(aar).records
        self.assertEqual(1, len(rs))
        r = rs[0]
        self.assertEqual(NdefTNF.EXTERNAL_TYPE, r.tnf)
        self.assertEqual(b"android.com:pkg", r.record_type)
        self.assertEqual(b"", r.record_id)
        self.assertEqual(b"com.foo.bar", r.payload)

    def test_create_text_record(self) -> None:
        s = "Hello"
        r = NdefRecord.create_text_record("en", s)
        self.assertEqual(s.encode("utf-8"), r.payload[r.payload[0] + 1:])
        self.assertRaises(ValueError, NdefRecord.create_text_record, "en", None)
        self.assertRaises(ValueError, NdefRecord.create_text_record, bytearray(64).decode("utf-8"), s)

    def test_to_bytes(self) -> None:
        # single short record
        self.assertEqual(b"\xd8\x00\x00\x00", NdefMessage(NdefRecord(NdefTNF.EMPTY, None, None, None)).to_bytes())
        # with id
        self.assertEqual(b"\xdd\x00\x00\x01\x09", NdefMessage(NdefRecord(NdefTNF.UNKNOWN, None, b"\x09", None)).to_bytes())
        # with type
        self.assertEqual(b"\xd4\x01\x00\x09", NdefMessage(NdefRecord(NdefTNF.EXTERNAL_TYPE, b"\x09", None, None)).to_bytes())
        # with payload
        self.assertEqual(b"\xd5\x00\x01\x09", NdefMessage(NdefRecord(NdefTNF.UNKNOWN, None, None, b"\x09")).to_bytes())
        # 3 records
        r = NdefRecord(NdefTNF.EMPTY, None, None, None)
        self.assertEqual(b"\x98\x00\x00\x00\x18\x00\x00\x00\x58\x00\x00\x00", NdefMessage(r, r, r).to_bytes())
        # 256 byte payload
        self.assertEqual(b"\xc5\x00\x00\x00\x01\x00" + self._PAYLOAD_256, NdefMessage(NdefRecord(NdefTNF.UNKNOWN, None, None, self._PAYLOAD_256)).to_bytes())

    def test_get_bytes_length(self) -> None:
        # single short record
        r = NdefRecord(NdefTNF.EMPTY, None, None, None)
        b = b"\xd8\x00\x00\x00"
        self.assertEqual(len(b), len(NdefMessage(r)))
        # 3 records
        r = NdefRecord(NdefTNF.EMPTY, None, None, None)
        b = b"\x98\x00\x00\x00\x18\x00\x00\x00\x58\x00\x00\x00"
        self.assertEqual(len(b), len(NdefMessage(r, r, r)))

    def test_to_uri(self) -> None:
        # absolute uri
        self.assertEqual("http://www.android.com", NdefRecord(NdefTNF.ABSOLUTE_URI, b"http://www.android.com", None, None).to_uri())
        # wkt uri
        self.assertEqual("http://www.android.com", NdefRecord.create_uri("http://www.android.com").to_uri())
        # smart poster with absolute uri
        self.assertEqual("http://www.android.com",
                         NdefRecord(
                             NdefTNF.WELL_KNOWN, NdefRTD.SMART_POSTER, None,
                             NdefMessage(NdefRecord(NdefTNF.ABSOLUTE_URI, b"http://www.android.com", None, None)).to_bytes()
                         ).to_uri())
        # smart poster with wkt uri
        self.assertEqual("http://www.android.com",
                         NdefRecord(
                             NdefTNF.WELL_KNOWN, NdefRTD.SMART_POSTER, None,
                             NdefRecord.create_uri("http://www.android.com").to_bytes()
                         ).to_uri())
        # smart poster with text and wkt uri
        self.assertEqual("http://www.android.com",
                         NdefRecord(
                             NdefTNF.WELL_KNOWN, NdefRTD.SMART_POSTER, None,
                             NdefMessage(
                                 NdefRecord(NdefTNF.WELL_KNOWN, NdefRTD.TEXT, None, None),
                                 NdefRecord.create_uri("http://www.android.com")
                             ).to_bytes()
                         ).to_uri())
        # external type
        self.assertEqual("vnd.android.nfc://ext/com.foo.bar:type", NdefRecord.create_external("com.foo.bar", "type", None).to_uri())
        # check normalization
        self.assertEqual("http://www.android.com", NdefRecord(NdefTNF.ABSOLUTE_URI, b"HTTP://www.android.com", None, None).to_uri())
        # not uri's
        self.assertEqual(None, NdefRecord.create_mime("text/plain", None).to_uri())
        self.assertEqual(None, NdefRecord(NdefTNF.EMPTY, None, None, None).to_uri())

    def test_to_mime_type(self) -> None:
        self.assertEqual(None, NdefRecord.create_uri("http://www.android.com").to_mime_type())
        self.assertEqual(None, NdefRecord(NdefTNF.EMPTY, None, None, None).to_mime_type())
        self.assertEqual(None, NdefRecord.create_external("com.foo.bar", "type", None).to_mime_type())
        self.assertEqual("a/b", NdefRecord.create_mime("a/b", None).to_mime_type())
        self.assertEqual("text/plain", NdefRecord(NdefTNF.WELL_KNOWN, NdefRTD.TEXT, None, None).to_mime_type())
        self.assertEqual("a/b", NdefRecord.create_mime("A/B", None).to_mime_type())
        self.assertEqual("a/b", NdefRecord(NdefTNF.MIME_MEDIA, b" A/B ", None, None).to_mime_type())

    def test_to_known_rtd(self) -> None:
        self.assertEqual(None, NdefRecord(NdefTNF.EMPTY, None, None, None).to_known_rtd())
        self.assertEqual(NdefRTD.TEXT, NdefRecord.create_text_record("en", "Hello").to_known_rtd())
        self.assertEqual(NdefRTD.URI, NdefRecord.create_uri("http://www.android.com").to_known_rtd())
        self.assertEqual(NdefRTD.SMART_POSTER,
                         NdefRecord(
                             NdefTNF.WELL_KNOWN, NdefRTD.SMART_POSTER, None,
                             NdefMessage(NdefRecord(NdefTNF.ABSOLUTE_URI, b"http://www.android.com", None, None)).to_bytes()
                         ).to_known_rtd())
        self.assertEqual(NdefRTD.ANDROID_APP, NdefRecord.create_application_record("com.android.nfc").to_known_rtd())
        self.assertEqual(NdefRTD.ALTERNATIVE_CARRIER, NdefRecord(NdefTNF.WELL_KNOWN, NdefRTD.ALTERNATIVE_CARRIER, None, None).to_known_rtd())
        self.assertEqual(NdefRTD.HANDOVER_CARRIER, NdefRecord(NdefTNF.WELL_KNOWN, NdefRTD.HANDOVER_CARRIER, None, None).to_known_rtd())
        self.assertEqual(NdefRTD.HANDOVER_REQUEST, NdefRecord(NdefTNF.WELL_KNOWN, NdefRTD.HANDOVER_REQUEST, None, None).to_known_rtd())
        self.assertEqual(NdefRTD.HANDOVER_SELECT, NdefRecord(NdefTNF.WELL_KNOWN, NdefRTD.HANDOVER_SELECT, None, None).to_known_rtd())
        self.assertEqual(None, NdefRecord(NdefTNF.EXTERNAL_TYPE, b"type", None, None).to_known_rtd())

    def test_repr(self) -> None:
        r1 = NdefRecord(NdefTNF.EMPTY, None, None, None)
        r2 = NdefRecord(NdefTNF.EXTERNAL_TYPE, b"type", b"\x01", b"\x02")
        p1 = "NdefRecord(tnf=0x00, type=b'', id=b'', payload=b'')"
        # noinspection SpellCheckingInspection
        p2 = "NdefRecord(tnf=0x04, type=b'type', id=b'\\x01', payload=b'\\x02')"
        self.assertEqual(p1, repr(r1))

        self.assertEqual(p2, repr(r2))
        self.assertEqual(f"NdefMessage({p1})", repr(NdefMessage(r1)))
        self.assertEqual(f"NdefMessage({p1}, {p2})", repr(NdefMessage(r1, r2)))

    def test_len(self) -> None:
        r1 = NdefRecord(NdefTNF.EMPTY, None, None, None)
        r2 = NdefRecord(NdefTNF.EXTERNAL_TYPE, b"type", b"\x01", self._PAYLOAD_256)
        self.assertEqual(4, len(r1))
        self.assertEqual(268, len(r2))
        self.assertEqual(4 + 268, len(NdefMessage(r1, r2)))


if __name__ == "__main__":
    unittest.main()
