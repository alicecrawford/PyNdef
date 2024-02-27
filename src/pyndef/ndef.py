import enum
import io
from typing import List, Tuple, Optional, Union, Iterator
from urllib.parse import urlparse


@enum.unique
class NdefTNF(int, enum.Enum):
    EMPTY = 0x00
    WELL_KNOWN = 0x01
    MIME_MEDIA = 0x02
    ABSOLUTE_URI = 0x03
    EXTERNAL_TYPE = 0x04
    UNKNOWN = 0x05
    UNCHANGED = 0x06
    RESERVED = 0x07


@enum.unique
class NdefRTD(bytes, enum.Enum):
    TEXT = b"T"
    URI = b"U"
    SMART_POSTER = b"Sp"
    ALTERNATIVE_CARRIER = b"ac"
    HANDOVER_CARRIER = b"Hc"
    HANDOVER_REQUEST = b"Hr"
    HANDOVER_SELECT = b"Hs"
    ANDROID_APP = b"android.com:pkg"


# noinspection SpellCheckingInspection
_URI_PREFIX_MAP: Tuple[str, ...] = (
    "",  # 0x00
    "http://www.",  # 0x01
    "https://www.",  # 0x02
    "http://",  # 0x03
    "https://",  # 0x04
    "tel:",  # 0x05
    "mailto:",  # 0x06
    "ftp://anonymous:anonymous@",  # 0x07
    "ftp://ftp.",  # 0x08
    "ftps://",  # 0x09
    "sftp://",  # 0x0A
    "smb://",  # 0x0B
    "nfs://",  # 0x0C
    "ftp://",  # 0x0D
    "dav://",  # 0x0E
    "news:",  # 0x0F
    "telnet://",  # 0x10
    "imap:",  # 0x11
    "rtsp://",  # 0x12
    "urn:",  # 0x13
    "pop:",  # 0x14
    "sip:",  # 0x15
    "sips:",  # 0x16
    "tftp:",  # 0x17
    "btspp://",  # 0x18
    "btl2cap://",  # 0x19
    "btgoep://",  # 0x1A
    "tcpobex://",  # 0x1B
    "irdaobex://",  # 0x1C
    "file://",  # 0x1D
    "urn:epc:id:",  # 0x1E
    "urn:epc:tag:",  # 0x1F
    "urn:epc:pat:",  # 0x20
    "urn:epc:raw:",  # 0x21
    "urn:epc:",  # 0x22
    "urn:nfc:",  # 0x23
)


def _normalize_mime_type(raw_mime_type: str) -> str:
    mime_type = raw_mime_type.strip().lower()
    if ";" in mime_type:
        mime_type, _ = mime_type.split(";", 1)
    return mime_type


def _normalize_uri_scheme(raw_uri: str) -> str:
    parsed_uri = urlparse(raw_uri)
    parsed_uri = parsed_uri._replace(scheme=parsed_uri.scheme.lower())
    return parsed_uri.geturl()


class _BytesBuffer(io.BytesIO):
    def __init__(self, buffer: Optional[bytes] = None, byte_order: str = "big") -> None:
        super().__init__(buffer)
        self._byte_order: str = byte_order

    def read_uint8(self) -> int:
        return self.read_int(1, False)

    def read_uint32(self) -> int:
        return self.read_int(4, False)

    def read_int(self, size: int, signed: bool) -> int:
        buffer = self.read(size)
        if 0 < size != len(buffer):
            raise IndexError("buffer is too short")
        # noinspection PyTypeChecker
        return int.from_bytes(bytes=buffer, byteorder=self._byte_order, signed=signed)

    def read_bytes(self, size: int) -> bytes:
        buffer = self.read(size)
        if len(buffer) != size:
            raise IndexError("buffer is too short")
        return buffer

    def write_uint8(self, value: int) -> int:
        return self.write_int(value, 1, False)

    def write_uint32(self, value: int) -> int:
        return self.write_int(value, 4, False)

    def write_int(self, value: int, size: int, signed: bool) -> int:
        # noinspection PyTypeChecker
        return self.write(value.to_bytes(length=size, byteorder=self._byte_order, signed=signed))


# /platform/frameworks/base/nfc/java/android/nfc/NdefRecord.java
class NdefRecord:
    _FLAG_MB: int = 0x80
    _FLAG_ME: int = 0x40
    _FLAG_CF: int = 0x20
    _FLAG_SR: int = 0x10
    _FLAG_IL: int = 0x08

    _MAX_PAYLOAD_SIZE: int = 10 * (1 << 20)

    def __init__(self, tnf: NdefTNF, record_type: Union[NdefRTD, bytes, None], record_id: Optional[bytes], payload: Optional[bytes]) -> None:
        self._tnf: NdefTNF = tnf
        self._record_type: bytes = bytes(record_type) if record_type is not None else bytes()
        self._record_id: bytes = bytes(record_id) if record_id is not None else bytes()
        self._payload: bytes = bytes(payload) if payload is not None else bytes()

        self._validate_tnf(tnf, self._record_type, self._record_id, self._payload)

    @property
    def tnf(self) -> NdefTNF:
        return self._tnf

    @property
    def record_type(self) -> bytes:
        return self._record_type

    @property
    def record_id(self) -> bytes:
        return self._record_id

    @property
    def payload(self) -> bytes:
        return self._payload

    def to_known_rtd(self) -> Optional[NdefRTD]:
        try:
            return NdefRTD(self._record_type)
        except ValueError:
            return None

    @staticmethod
    def create_application_record(package_name: str) -> 'NdefRecord':
        if package_name is None or len(package_name) == 0:
            raise ValueError("packageName is empty")
        return NdefRecord(NdefTNF.EXTERNAL_TYPE, NdefRTD.ANDROID_APP, None, package_name.encode("utf-8"))

    @staticmethod
    def create_uri(uri: str) -> 'NdefRecord':
        uri_string = _normalize_uri_scheme(uri.strip())
        prefix = 0
        for i, uri_prefix in enumerate(_URI_PREFIX_MAP[1:]):
            if uri_string.startswith(uri_prefix):
                prefix = i + 1
                uri_string = uri_string[len(uri_prefix):]
                break
        prefix_bytes = prefix.to_bytes(length=1, byteorder="big", signed=False)
        record = prefix_bytes + uri_string.encode("utf-8")
        return NdefRecord(NdefTNF.WELL_KNOWN, NdefRTD.URI, None, bytes(record))

    @staticmethod
    def create_mime(mime_type: str, mime_data: Optional[bytes]) -> 'NdefRecord':
        mime_type = _normalize_mime_type(mime_type)

        if len(mime_type) == 0:
            raise ValueError("mimeType is empty")
        slash_index = mime_type.index('/')
        if slash_index == 0:
            raise ValueError("mimeType must have major type")
        if slash_index == len(mime_type) - 1:
            raise ValueError("mimeType must have minor type")

        return NdefRecord(NdefTNF.MIME_MEDIA, mime_type.encode("ascii"), None, mime_data)

    @staticmethod
    def create_external(domain: str, external_type: str, data: Optional[bytes]) -> 'NdefRecord':
        domain = domain.strip().lower()
        external_type = external_type.strip().lower()

        if len(domain) == 0:
            raise ValueError("domain is empty")
        if len(external_type) == 0:
            raise ValueError("type is empty")

        record_type = domain.encode("utf-8") + b':' + external_type.encode("utf-8")
        return NdefRecord(NdefTNF.EXTERNAL_TYPE, record_type, None, data)

    @staticmethod
    def create_text_record(language_code: str, text: str) -> 'NdefRecord':
        if text is None:
            raise ValueError("text is None")

        text_bytes = text.encode("utf-8")
        language_code_bytes = language_code.encode("ascii")

        if len(language_code_bytes) >= 64:
            raise ValueError("language code is too long, must be <64 bytes.")

        status_bytes = len(language_code_bytes).to_bytes(length=1, byteorder="big", signed=False)
        buffer = status_bytes + language_code_bytes + text_bytes
        return NdefRecord(NdefTNF.WELL_KNOWN, NdefRTD.TEXT, None, buffer)

    @staticmethod
    def parse(buffer: bytes, ignore_mb_me: bool = True) -> Tuple['NdefRecord', ...]:
        def _ensure_sane_payload_size(size: int) -> None:
            if size > NdefRecord._MAX_PAYLOAD_SIZE:
                raise ValueError(f"payload above max limit: {size} > {NdefRecord._MAX_PAYLOAD_SIZE}")

        records: List['NdefRecord'] = []

        record_type: Optional[bytes] = None
        record_id: Optional[bytes] = None

        bytes_buffer = _BytesBuffer(buffer)
        chunks: List[bytes] = []
        in_chunk: bool = False
        chunk_tnf: Optional[NdefTNF] = None
        me: bool = False

        try:
            while not me:
                flag = bytes_buffer.read_uint8()

                mb = flag & NdefRecord._FLAG_MB != 0
                me = flag & NdefRecord._FLAG_ME != 0
                cf = flag & NdefRecord._FLAG_CF != 0
                sr = flag & NdefRecord._FLAG_SR != 0
                il = flag & NdefRecord._FLAG_IL != 0
                tnf = NdefTNF(flag & 0x07)

                if not mb and len(records) == 0 and not in_chunk and not ignore_mb_me:
                    raise ValueError("expected MB flag")
                elif mb and (len(records) != 0 or in_chunk) and not ignore_mb_me:
                    raise ValueError("unexpected MB flag")
                elif in_chunk and il:
                    raise ValueError("unexpected IL flag in non-leading chunk")
                elif cf and me:
                    raise ValueError("unexpected ME flag in non-trailing chunk")
                elif in_chunk and tnf != NdefTNF.UNCHANGED:
                    raise ValueError("expected TNF_UNCHANGED in non-leading chunk")
                elif not in_chunk and tnf == NdefTNF.UNCHANGED:
                    raise ValueError("unexpected TNF_UNCHANGED in first chunk or not chunked record")

                type_length = bytes_buffer.read_uint8()
                payload_length = bytes_buffer.read_uint8() if sr else bytes_buffer.read_uint32()
                id_length = bytes_buffer.read_uint8() if il else 0

                if in_chunk and type_length != 0:
                    raise ValueError("expected zero-length type in non-leading chunk")

                if not in_chunk:
                    record_type = bytes_buffer.read_bytes(type_length)
                    record_id = bytes_buffer.read_bytes(id_length)

                _ensure_sane_payload_size(payload_length)
                payload = bytes_buffer.read_bytes(payload_length)

                if cf and not in_chunk:
                    if type_length == 0 and tnf != NdefTNF.UNKNOWN:
                        raise ValueError("expected non-zero type length in first chunk")
                    chunks.clear()
                    chunk_tnf = tnf

                if cf or in_chunk:
                    chunks.append(payload)

                if not cf and in_chunk:
                    payload_length = sum(len(chunk) for chunk in chunks)
                    _ensure_sane_payload_size(payload_length)
                    payload = b''.join([chunk for chunk in chunks])
                    tnf = chunk_tnf

                if cf:
                    in_chunk = True
                    continue
                else:
                    in_chunk = False

                NdefRecord._validate_tnf(tnf, record_type, record_id, payload)
                records.append(NdefRecord(tnf, record_type, record_id, payload))

                if ignore_mb_me:
                    break
        except IndexError as e:
            raise ValueError("expected more data") from e

        if bytes_buffer.read():
            raise ValueError("data too long")

        return tuple(records)

    @property
    def _flag_sr(self) -> bool:
        return len(self._payload) < 256

    @property
    def _flag_il(self) -> bool:
        return True if self._tnf == NdefTNF.EMPTY else len(self._record_id) > 0

    def to_mime_type(self) -> Optional[str]:
        if self._tnf == NdefTNF.WELL_KNOWN:
            if self._record_type == NdefRTD.TEXT:
                return "text/plain"
        elif self._tnf == NdefTNF.MIME_MEDIA:
            raw_mime_type = self._record_type.decode("ascii")
            return _normalize_mime_type(raw_mime_type)
        return None

    def to_uri(self) -> Optional[str]:
        return self._to_uri(False)

    def _to_uri(self, in_smart_poster: bool) -> Optional[str]:
        if self._tnf == NdefTNF.WELL_KNOWN:
            if self._record_type == NdefRTD.SMART_POSTER and not in_smart_poster:
                for record in NdefMessage.parse(self._payload):
                    uri = record._to_uri(True)
                    if uri is not None:
                        return _normalize_uri_scheme(uri)
            elif self._record_type == NdefRTD.URI:
                if len(self._payload) >= 2:
                    prefix_index = self._payload[0]
                    if 0 <= prefix_index < len(_URI_PREFIX_MAP):
                        return _URI_PREFIX_MAP[prefix_index] + self._payload[1:].decode("utf-8")
        elif self._tnf == NdefTNF.ABSOLUTE_URI:
            return _normalize_uri_scheme(self._record_type.decode("utf-8"))
        elif self._tnf == NdefTNF.EXTERNAL_TYPE:
            if not in_smart_poster:
                return "vnd.android.nfc://ext/" + self._record_type.decode("ascii")
        return None

    def to_bytes(self, flag_mb: bool = True, flag_me: bool = True) -> bytes:
        buffer = _BytesBuffer()

        flag = (self._FLAG_MB if flag_mb else 0) | \
               (self._FLAG_ME if flag_me else 0) | \
               (self._FLAG_SR if self._flag_sr else 0) | \
               (self._FLAG_IL if self._flag_il else 0) | self._tnf.value

        buffer.write_uint8(flag)
        buffer.write_uint8(len(self._record_type))

        if self._flag_sr:
            buffer.write_uint8(len(self._payload))
        else:
            buffer.write_uint32(len(self._payload))
        if self._flag_il:
            buffer.write_uint8(len(self._record_id))

        buffer.write(self._record_type)
        buffer.write(self._record_id)
        buffer.write(self._payload)

        return buffer.getvalue()

    @staticmethod
    def _validate_tnf(tnf: NdefTNF, record_type: bytes, record_id: bytes, payload: bytes) -> None:
        if tnf == NdefTNF.EMPTY:
            if len(record_type) != 0 or len(record_id) != 0 or len(payload) != 0:
                raise ValueError("unexpected data in TNF_EMPTY record")
        elif tnf == NdefTNF.UNKNOWN or tnf == NdefTNF.RESERVED:
            if len(record_type) != 0:
                raise ValueError("unexpected type field in TNF_UNKNOWN or TNF_RESERVED record")
        elif tnf == NdefTNF.UNCHANGED:
            raise ValueError("unexpected TNF_UNCHANGED in first chunk or logical record")

    def bytes_size(self) -> int:
        length = 3 + len(self._record_type) + len(self._record_id) + len(self._payload)
        if not self._flag_sr:
            length += 3
        if self._flag_il:
            length += 1
        return length

    def __bytes__(self) -> bytes:
        return self.to_bytes()

    def __repr__(self) -> str:
        return ("NdefRecord("
                f"tnf=0x{self._tnf.value:02x}, "
                f"type={self._record_type}, "
                f"id={self._record_id}, "
                f"payload={self._payload})")

    def __eq__(self, __value) -> bool:
        if __value is None or not isinstance(__value, NdefRecord):
            return super().__eq__(__value)
        else:
            return self._tnf == __value._tnf and \
                self._record_type == __value._record_type and \
                self._record_id == __value._record_id and \
                self._payload == __value._payload

    def __hash__(self) -> int:
        return hash((self._tnf.value, self._record_type, self._record_id, self._payload))


# /platform/frameworks/base/nfc/java/android/nfc/NdefMessage.java
class NdefMessage:
    def __init__(self, *records: NdefRecord) -> None:
        if len(records) == 0:
            raise ValueError("must have at least one record")
        self._records: Tuple[NdefRecord, ...] = records

    @property
    def records(self) -> Tuple[NdefRecord, ...]:
        return self._records

    @staticmethod
    def parse(buffer: bytes) -> 'NdefMessage':
        records = NdefRecord.parse(buffer, False)
        return NdefMessage(*records)

    def to_bytes(self) -> bytes:
        return b''.join(
            [
                record.to_bytes(i == 0, i == len(self._records) - 1)
                for i, record in enumerate(self._records)
            ]
        )

    def bytes_size(self) -> int:
        return sum(i.bytes_size() for i in self._records)

    def __bytes__(self) -> bytes:
        return self.to_bytes()

    def __iter__(self) -> Iterator[NdefRecord]:
        return iter(self._records)

    def __len__(self) -> int:
        return len(self._records)

    def __repr__(self) -> str:
        return f"NdefMessage({', '.join([repr(i) for i in self._records])})"

    def __eq__(self, __value) -> bool:
        if __value is None or not isinstance(__value, NdefMessage):
            return super().__eq__(__value)
        else:
            return self._records == __value._records

    def __hash__(self) -> int:
        return hash(self._records)
