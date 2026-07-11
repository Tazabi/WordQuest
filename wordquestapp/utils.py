from datetime import datetime, timedelta, date


def calculate_next_review(current_rank, is_correct, time_since_last_review_hours):
    # 1. Вычисляем порог просрочки
    # Ранг 0 — порог 0 часов (всегда просрочено, но это крайний случай)
    # Ранг 50 — порог 2400 часов (100 дней)
    overdue_threshold = 24 * (current_rank * 2)  # в часах

    # 2. Определяем новый ранг
    if is_correct:
        if time_since_last_review_hours <= overdue_threshold:
            # Успех вовремя — повышаем
            new_rank = current_rank + 1
        else:
            # Успех, но с опозданием — понижаем
            new_rank = current_rank - 1
    else:
        # Ошибка — понижаем в любом случае
        new_rank = current_rank - 1

    # 3. Ограничиваем ранг диапазоном [0, 100]
    new_rank = max(0, min(new_rank, 100))

    # 4. Вычисляем новый интервал (в часах)
    # Ранг 0 -> интервал 0 часов (слово можно повторять сразу)
    # Ранг 50 -> интервал 1200 часов (50 дней)
    new_interval_hours = 12 * (new_rank * 2)

    return new_rank, new_interval_hours

def update_streak(user):
    today = date.today()
    changed = False

    # Первая активность — инициализируем все поля
    if user.last_activity_date is None:
        user.streak = 1
        user.max_streak = max(user.max_streak or 0, 1)
        user.last_activity_date = today
        return True  # точно изменили

    # Уже была активность сегодня — не учитываем повторно
    if user.last_activity_date == today:
        return False  # ничего не изменилось

    # Вычисляем разницу в днях между сегодня и последней активностью
    delta = (today - user.last_activity_date).days

    if delta == 1:
        # Активность была вчера — продолжаем стрик
        user.streak += 1
        changed = True
    else:
        # Перерыв больше 1 дня — начинаем заново
        user.streak = 1
        changed = True

    # Обновляем максимальный стрик, если текущий побил рекорд
    if user.streak > (user.max_streak or 0):
        user.max_streak = user.streak

    # Фиксируем сегодняшнюю дату
    user.last_activity_date = today
    return changed  # True, если было изменение


def time_ago(past_datetime, now=None):

    if now is None:
        now = datetime.utcnow()

    diff = now - past_datetime
    seconds = diff.total_seconds()

    if seconds < 0:
        return "в будущем"  # на всякий случай

    if seconds < 60:
        return "только что"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes} мин. назад"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours} ч. назад"
    elif seconds < 2592000:  # 30 дней
        days = int(seconds // 86400)
        return f"{days} дн. назад"
    else:
        return "давно"


# ========== Тесты (можно запустить: python utils.py) ==========
if __name__ == "__main__":
    print("=== Тесты calculate_next_review ===\n")

    # Тест 1: успех без просрочки
    rank, interval = calculate_next_review(5, True, 10)
    # Порог для ранга 5: 24 * (5 * 2) = 240 часов
    # 10 часов <= 240 — не просрочено
    # Ожидаем: rank 6, interval = 12 * (6 * 2) = 144 часов
    assert rank == 6, f"Ожидался ранг 6, получен {rank}"
    assert interval == 144, f"Ожидался интервал 144, получен {interval}"
    print("✓ Успех без просрочки (5 -> 6, интервал 144 ч)")

    # Тест 2: успех с просрочкой
    rank, interval = calculate_next_review(5, True, 500)
    # 500 > 240 — просрочено, ранг понижается
    # Ожидаем: rank 4, interval = 12 * (4 * 2) = 96 часов
    assert rank == 4, f"Ожидался ранг 4, получен {rank}"
    assert interval == 96, f"Ожидался интервал 96, получен {interval}"
    print("✓ Успех с просрочкой (5 -> 4, интервал 96 ч)")

    # Тест 3: ошибка
    rank, interval = calculate_next_review(5, False, 10)
    # Ошибка всегда понижает
    # Ожидаем: rank 4, interval = 12 * (4 * 2) = 96 часов
    assert rank == 4, f"Ожидался ранг 4, получен {rank}"
    assert interval == 96, f"Ожидался интервал 96, получен {interval}"
    print("✓ Ошибка (5 -> 4, интервал 96 ч)")

    # Тест 4: граница ранга 0 (не уходит в минус)
    rank, interval = calculate_next_review(0, False, 10)
    assert rank == 0, f"Ожидался ранг 0, получен {rank}"
    assert interval == 0, f"Ожидался интервал 0, получен {interval}"
    print("✓ Ранг не уходит ниже 0")

    # Тест 5: граница ранга 100 (не уходит выше)
    rank, interval = calculate_next_review(100, True, 1)
    # Порог для 100: 24 * 200 = 4800 часов (200 дней)
    # 1 час <= 4800 — не просрочено, но ранг упёрся в потолок
    assert rank == 100, f"Ожидался ранг 100, получен {rank}"
    assert interval == 12 * (100 * 2), f"Неверный интервал"
    print("✓ Ранг не уходит выше 100")

    print("\n=== Тесты update_streak ===\n")
    print("Для проверки update_streak используйте flask shell:")
    print("  from app import db")
    print("  from Models import User")
    print("  from utils import update_streak")
    print("  u = User.query.first()")
    print("  update_streak(u)")
    print("  db.session.commit()")

    print("\n=== Все тесты пройдены ===")