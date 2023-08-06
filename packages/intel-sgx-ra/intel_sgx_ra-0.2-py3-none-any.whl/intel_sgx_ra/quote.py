"""intel_sgx_ra.quote module."""

from dataclasses import dataclass, asdict
from io import BytesIO
import re
from typing import Tuple, cast

SGX_QUOTE_MAX_SIZE: int = 8192

RE_CERT: re.Pattern = re.compile(
    b"(-----BEGIN CERTIFICATE-----\n.*?\n-----END CERTIFICATE-----)", re.DOTALL)


@dataclass
class ReportBody:  # 384 bytes
    """SGX report_body structure."""

    cpu_svn: bytes  # 0
    misc_select: int  # 16
    reserved1: bytes  # 20
    isv_ext_prod_id: bytes  # 32
    attributes: Tuple[int, int]  # 48
    mr_enclave: bytes  # 64
    reserved2: bytes  # 96
    mr_signer: bytes  # 128
    reserved3: bytes  # 160
    config_id: bytes  # 192
    isv_prod_id: int  # 256
    isv_svn: int  # 258
    config_svn: int  # 260
    reserved4: bytes  # 262
    isvn_family_id: bytes  # 304
    report_data: bytes  # 320

    @classmethod
    def from_bytes(cls, raw_report_body: bytes) -> 'ReportBody':
        """Deserialize bytes of sgx_report_body structure."""
        buf: BytesIO = BytesIO(raw_report_body)

        cpu_svn: bytes = buf.read(16)
        misc_select: int = int.from_bytes(buf.read(4), byteorder="little")
        reserved1: bytes = buf.read(12)
        isv_ext_prod_id: bytes = buf.read(16)
        attributes: Tuple[int, int] = (
            int.from_bytes(buf.read(8), byteorder="little"),  # flags
            int.from_bytes(buf.read(8), byteorder="little"))  # xfrm
        mr_enclave: bytes = buf.read(32)
        reserved2: bytes = buf.read(32)
        mr_signer: bytes = buf.read(32)
        reserved3: bytes = buf.read(32)
        config_id: bytes = buf.read(64)
        isv_prod_id: int = int.from_bytes(buf.read(2), byteorder="little")
        isv_svn: int = int.from_bytes(buf.read(2), byteorder="little")
        config_svn: int = int.from_bytes(buf.read(2), byteorder="little")
        reserved4: bytes = buf.read(42)
        isvn_family_id: bytes = buf.read(16)
        report_data: bytes = buf.read(64)

        return cls(cpu_svn, misc_select, reserved1, isv_ext_prod_id, attributes,
                   mr_enclave, reserved2, mr_signer, reserved3, config_id,
                   isv_prod_id, isv_svn, config_svn, reserved4, isvn_family_id,
                   report_data)

    def __bytes__(self) -> bytes:
        """Serialize ReportBody."""
        buf = BytesIO()
        buf.write(self.cpu_svn)
        buf.write(self.misc_select.to_bytes(4, byteorder="little"))
        buf.write(self.reserved1)
        buf.write(self.isv_ext_prod_id)
        # flags
        buf.write(self.attributes[0].to_bytes(8, byteorder="little"))
        # xfrm
        buf.write(self.attributes[1].to_bytes(8, byteorder="little"))
        buf.write(self.mr_enclave)
        buf.write(self.reserved2)
        buf.write(self.mr_signer)
        buf.write(self.reserved3)
        buf.write(self.config_id)
        buf.write(self.isv_prod_id.to_bytes(2, byteorder="little"))
        buf.write(self.isv_svn.to_bytes(2, byteorder="little"))
        buf.write(self.config_svn.to_bytes(2, byteorder="little"))
        buf.write(self.reserved4)
        buf.write(self.isvn_family_id)
        buf.write(self.report_data)

        return buf.getvalue()

    def to_dict(self):
        """Dataclass to dict."""
        return asdict(self)


@dataclass
class Quote:
    """SGX quote structure."""

    version: int  # 0
    sign_type: int  # 2
    epid_group_id: bytes  # 4
    qe_svn: int  # 8
    pce_svn: int  # 10
    xeid: int  # 12
    basename: bytes  # 16
    report_body: ReportBody  # 48
    signature_len: int  # 432
    signature: bytes  # 436

    @classmethod
    def from_bytes(cls, raw_quote: bytes) -> 'Quote':
        """Deserialize bytes of sgx_quote structure."""
        buf: BytesIO = BytesIO(raw_quote)

        version: int = int.from_bytes(buf.read(2), byteorder="little")
        sign_type: int = int.from_bytes(buf.read(2), byteorder="little")
        epid_group_id: bytes = buf.read(4)
        qe_svn: int = int.from_bytes(buf.read(2), byteorder="little")
        pce_svn: int = int.from_bytes(buf.read(2), byteorder="little")
        xeid: int = int.from_bytes(buf.read(4), byteorder="little")
        basename: bytes = buf.read(32)

        raw_report_body: bytes = buf.read(384)
        report_body: ReportBody = ReportBody.from_bytes(raw_report_body)

        signature_len: int = int.from_bytes(buf.read(4), byteorder="little")
        signature: bytes = buf.read(signature_len)

        return cls(version, sign_type, epid_group_id, qe_svn, pce_svn, xeid,
                   basename, report_body, signature_len, signature)

    def __bytes__(self) -> bytes:
        """Serialize Quote."""
        buf = BytesIO()
        buf.write(self.version.to_bytes(2, byteorder="little"))
        buf.write(self.sign_type.to_bytes(2, byteorder="little"))
        buf.write(self.epid_group_id)
        buf.write(self.qe_svn.to_bytes(2, byteorder="little"))
        buf.write(self.pce_svn.to_bytes(2, byteorder="little"))
        buf.write(self.xeid.to_bytes(4, byteorder="little"))
        buf.write(self.basename)
        buf.write(bytes(self.report_body))
        buf.write(self.signature_len.to_bytes(4, byteorder="little"))
        buf.write(self.signature)

        return buf.getvalue()

    def certs(self) -> Tuple[bytes, bytes, bytes]:
        """Find all certificates in signature field."""
        return cast(Tuple[bytes, bytes, bytes],
                    tuple(re.findall(RE_CERT, self.signature)))

    def to_dict(self):
        """Dataclass to dict."""
        return asdict(self)
