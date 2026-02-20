from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

test_passwords = ["123", "test123", "password", "a" * 100]

for pwd in test_passwords:
    print(f"Testing password: '{pwd}' (length: {len(pwd)})")
    try:
        pwd_bytes = pwd.encode('utf-8')[:72]
        print(f"  Bytes length: {len(pwd_bytes)}")
        print(f"  Bytes: {pwd_bytes}")
        hashed = pwd_context.hash(pwd_bytes)
        print(f"  Hash: {hashed}")
        print(f"  Success!")
    except Exception as e:
        print(f"  Error: {e}")
    print()
