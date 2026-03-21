#!/bin/bash
#Скрипт по удалению файла или файлов по параметру

echo "Script is started"
#exec 2>log

show_help() {
	echo "------------------------------------------------------"
	echo "$0 [-p] <имя_файла>"
	echo "Использование параметра [-p] позволяет удалять файлы по шаблону"
	echo "Без параметра [-p] удаление конкретного файла"
	echo "------------------------------------------------------"
}

if [ $# -eq 0 ]; then
	echo "Не указан параметр"
	show_help
	exit 1
fi

if [ $# -gt 2 ]; then
	echo "Слишком много параметров"
	show_help
	exit 1
fi

pattern=false
par=""

if [ "$1" = "-p" ]; then
	pattern=true
	if [ -z "$2" ]; then
		echo "Имя файла не указано"
		show_help
		exit 1
	fi
	par="$2"
else
	pattern=false
	par="$1"
fi

if [ "$pattern" = true ]; then
	read -p "Удалить файлы, содержащие '$par'? (Y/N)" -n 1 -r 
	echo
	if [[ $REPLY =~ ^[Yy]$ ]]; then
		echo "Удаление файлов, содержащих '$par'"
		for file in *"$par"*; do
			if [ -e "$file" ] && [ -f $par ]; then
				echo "Удаление ./$file"
				rm "./$file"
			else
				echo "Файлы с содержанием '$par' не найдены"
				continue
			fi
		done
	else
		echo "Отмена удаления"
		exit 1
	fi
else
	read -p "Удалить файлы, содержащие '$par'? (Y/N)" -n 1 -r 
	echo
	if [[ $REPLY =~ ^[Yy]$ ]]; then
		if [ -e "$par" ] && [ -f $par ]; then
			echo "Удаление файла ./$par"
			rm "./$par"
		else
			echo "Файл '$par' не найден"
			exit 1
		fi
	else
		echo "Отмена удаления"
		exit 1
	fi
fi	

echo "Script is finished, yipie"
