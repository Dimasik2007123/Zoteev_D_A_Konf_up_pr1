#!/bin/bash
echo "--- Запуск теста: все параметры ---"
python konf_1_2.py --vfs "./vfs_data/.my_vfs" --script "./scripts/init.sh"
echo "--- Тест завершен ---"