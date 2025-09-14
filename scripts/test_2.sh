#!/bin/bash
echo "--- Запуск теста: ls ---"
python konf_1_2.py --script "./scripts/ls_only.sh"
# Предполагается, что ls_only.sh содержит 'ls'
echo "--- Тест завершен ---"