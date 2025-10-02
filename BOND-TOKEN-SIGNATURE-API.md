# BondToken Signature API

## Overview

The BondToken endpoint includes cryptographic signatures to authenticate device responses. This document describes the signature field in the token API response.

## Token Response Format

When a client requests token information, the response includes a signature field:

```json
{
  "B": "SMAXX75499",
  "t": "token",
  "b": {
    "account_code": "00000000000001",
    "nonce": "765196d974a92828",
    "token": "8e023cc4f40bb115",
    "sig": "MEYCIQCu1CV/9BG6+GmHHjipRW093ktWp/2pOLi3T2gxZP5iqgIhAIjNC79KwFDffhZDUgfxz8OXh+caLKWbAWFqU0gNPmki",
    ...
  }
}
```

## Signature Format

### Signing Input

The signature covers three fields concatenated with colons:
```
bond_id:account_code:nonce_hex
```

Example:
```
SMAXX75499:00000000000001:765196d974a92828
```

### Cryptographic Details

- **Algorithm**: ECDSA with P-256 (secp256r1) curve
- **Hash**: SHA-256 (performed internally by signing function)
- **Encoding**: Base64-encoded DER format (ASN.1 SEQUENCE of r,s values)
- **Typical Size**: ~70 bytes (vs 384 bytes for RSA-3072)

### Signing Process

1. Construct the signing input string
2. The mbedtls_bond_ecdsa_sign function internally:
   - Computes SHA-256 hash of the input
   - Signs the hash with the device's ECDSA private key
   - Returns DER-encoded signature
3. Base64-encode the signature for JSON response

## Key Management

### Device Keys

Each device has a unique ECDSA key pair stored in its BONDID partition:
- Private key: `bond-{BONDID}.iot.ecdsa.key` (on device only)
- Certificate: `bond-{BONDID}.iot.ecdsa.crt.chain` (contains public key)

### Certificate Chain

The certificate chain includes:
1. Device certificate (signed by Olibra ECDSA CA)
2. Olibra ECDSA root CA certificate

## Verification

To verify a signature:

1. Extract the public key from the device's certificate
2. Reconstruct the signing input: `{bond_id}:{account_code}:{nonce_hex}`
3. Verify the signature against the signing input using ECDSA-SHA256

### Python Example

```python
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography import x509
import base64

# Load certificate and extract public key
cert = x509.load_pem_x509_certificate(cert_data)
public_key = cert.public_key()

# Reconstruct signing input
signing_input = f"{bond_id}:{account_code}:{nonce_hex}"

# Decode and verify signature
signature = base64.b64decode(signature_b64)
public_key.verify(
    signature,
    signing_input.encode('utf-8'),
    ec.ECDSA(hashes.SHA256())
)
```

## Security Considerations

1. **Device Binding**: Including BOND ID prevents signature replay between devices
2. **Nonce**: Prevents replay of old signatures for the same account
3. **Account Binding**: Ties the signature to a specific account code
4. **Certificate Validation**: Verify certificate chain to ensure device authenticity

## Backend Integration

For production use:
1. Store device certificates indexed by BOND ID
2. Cache certificates locally to reduce lookups
3. Implement signature verification before processing token requests
4. Consider certificate revocation mechanisms for compromised devices

## Migration Notes

- Previous format: `account_code:nonce`
- Current format: `bond_id:account_code:nonce`
- Firmware updates required for devices using old format