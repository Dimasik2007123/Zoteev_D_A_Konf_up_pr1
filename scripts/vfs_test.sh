# --- Тесты VFS ---
echo "--- Запуск тестов VFS ---"

# 1. Запуск с минимальным VFS
echo "1. Запуск с минимальным VFS"
python konf_1_3.py --vfs "./vfs_data/.my_vfs/vfs1.zip" --script "./scripts/test_vfs1.sh"

# 2. Запуск со сложным VFS
echo "2. Запуск со сложным VFS"
python konf_1_3.py --vfs "./vfs_data/.my_vfs/vfs2.zip" --script "./scripts/test_vfs2.sh"

# 3. Запуск с бинарным VFS
echo "3. Запуск с бинарным VFS"
python konf_1_3.py --vfs "./vfs_data/.my_vfs/vfs_bin.zip" --script "./scripts/test_vfsbin.sh"


# 4. Тест несуществующего VFS архива
echo "4. Тест несуществующего VFS архива"
python shell_emulator.py --vfs "./vfs_data/.my_vfs/vfs3.zip" --script "./scripts/test_vfs_not_found.sh"

echo "--- Тесты VFS завершены ---"