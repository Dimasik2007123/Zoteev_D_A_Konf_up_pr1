#!/bin/bash
echo "4. Запуск с несуществующим VFS"
python konf_1_4.py --vfs "./vfs_data/.my_vfs/vfs3.zip" --script "./scripts/init.sh"
echo "--- Тест завершен ---"