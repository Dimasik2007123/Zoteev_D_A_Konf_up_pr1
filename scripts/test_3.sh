#!/bin/bash
echo "--- Запуск теста: exit ---"
python konf_1_2.py --script "./scripts/exit_only.sh" # Предполагается, что exit_only.sh содержит 'exit'
echo "--- Тест завершен ---"