set base_dir=%~dp0
set alias_path=%cmder_home%\config\user_aliases.cmd
echo query=python %base_dir%\main.py $* >> "%alias_path%"

python %base_dir%\init.py

echo "finished, please restart your terminal to enjoy it."
