# SPDX-FileCopyrightText: Copyright (c) 2023-2026 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
# SPDX-License-Identifier: MIT

lint:
	poetry run isort pyeo tests
	poetry run flake8 pyeo
	poetry run mypy pyeo

test:
	poetry run pytest
