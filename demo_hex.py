"""Demonstrate hexadecimal key export and import for Falcon-512."""

from falcon import Falcon


def main():
    falcon = Falcon(512)
    sk, vk = falcon.keygen()

    sk_hex = falcon.pack_sk_hex(sk)
    vk_hex = falcon.pack_vk_hex(vk)
    sk_len = len(bytes.fromhex(sk_hex))
    vk_len = len(bytes.fromhex(vk_hex))

    print(f"Falcon-512 signing key      ({sk_len} bytes): {sk_hex[:64]}...")
    print(f"Falcon-512 verification key ({vk_len} bytes): {vk_hex[:64]}...")

    imported_sk = falcon.unpack_sk_hex(sk_hex)
    imported_vk = falcon.unpack_vk_hex(vk_hex)
    print(f"Signing key round-trip identical:      {imported_sk == sk}")
    print(f"Verification key round-trip identical: {imported_vk == vk}")

    message = b"Hello from issue #7"
    signature = falcon.sign(imported_sk, message)
    is_valid = falcon.verify(imported_vk, message, signature)
    print(f"Signature from hex-imported keys valid: {is_valid}")

    try:
        falcon.unpack_vk_hex(vk_hex[:-2])
    except ValueError as error:
        print(f"Truncated key rejected: {error}")


if __name__ == "__main__":
    main()