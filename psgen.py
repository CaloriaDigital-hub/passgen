#!/usr/bin/env python3
"""Генератор паролей «в памяти»: пароль не хранится, а считается на лету.

Пароль = SHA-256 по цепочке от "<соль>:<сайт>", повторённой N раз,
затем base64, первые 20 символов, последние два заменены на "9!".
"""

import base64
import getpass
import hashlib

PASSWORD_LENGTH = 20
SUFFIX = "9!"  # гарантирует цифру и спецсимвол для строгих правил сайтов
MIN_ITERATIONS = 40
MAX_ITERATIONS = 50


def derive_password(site: str, salt: str, iterations: int) -> str:
    """Детерминированно считает пароль по сайту, соли и числу итераций."""
    data = f"{salt}:{site}".encode("utf-8")
    for _ in range(iterations):
        data = hashlib.sha256(data).digest()

    encoded = base64.b64encode(data).decode("utf-8")[:PASSWORD_LENGTH]
    return encoded[: -len(SUFFIX)] + SUFFIX


def main() -> None:
    print("=== ГЕНЕРАТОР ПАРОЛЕЙ В ПАМЯТИ ===")

    site = input("Введите имя сайта или сервера: ").lower().strip()
    if not site:
        print("Ошибка: имя сайта не может быть пустым.")
        return

    salt = getpass.getpass("Введите вашу секретную соль (скрытый ввод): ")
    if not salt:
        print("Ошибка: соль не может быть пустой.")
        return

    try:
        iterations = int(
            getpass.getpass(
                f"Введите секретное число от {MIN_ITERATIONS} до {MAX_ITERATIONS} "
                "(скрытый ввод): "
            )
        )
    except ValueError:
        print("Ошибка: нужно ввести целое число.")
        return

    if not MIN_ITERATIONS <= iterations <= MAX_ITERATIONS:
        print(
            f"Предупреждение: число вне диапазона "
            f"{MIN_ITERATIONS}-{MAX_ITERATIONS}, но алгоритм сработает."
        )

    password = derive_password(site, salt, iterations)

    line = "=" * 40
    print(f"\n{line}")
    print(f"Ваш пароль для [{site}]:")
    print(password)
    print(line)
    print("Внимание: очистите консоль после копирования пароля!")


if __name__ == "__main__":
    main()
