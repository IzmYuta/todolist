from .settings import *  # noqa: F401, F403

SECRET_KEY = "test_secret_key"

# テスト実行時のDBはPostgreSQLではなくSQLiteを使用
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
        "ATOMIC_REQUESTS": True,
    },
}

PASSWORD_HASHERS = (
    "django.contrib.auth.hashers.SHA1PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
    "django.contrib.auth.hashers.MD5PasswordHasher",
    "django.contrib.auth.hashers.UnsaltedSHA1PasswordHasher",
    "django.contrib.auth.hashers.UnsaltedMD5PasswordHasher",
    "django.contrib.auth.hashers.CryptPasswordHasher",
)
