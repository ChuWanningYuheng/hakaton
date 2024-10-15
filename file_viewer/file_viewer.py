import flet as ft
import markdown2  # Для конвертации markdown в HTML (если нужно для других целей)

# Глобальная переменная для хранения содержимого файла
file_content = ""

def main(page: ft.Page):
    global file_content
    page.title = "Markdown Редактор"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Поле для ввода Markdown текста
    markdown_input = ft.TextField(
        label="Введите или загрузите Markdown текст",
        multiline=True,
        expand=True,
        min_lines=10,
        on_change=lambda e: convert_markdown(),  # Обновляем при изменении
    )

    # Поле для отображения результата конвертации через ft.Markdown
    markdown_display = ft.Markdown(
        value="",
        extension_set="gitHubWeb",  # Используем расширенный синтаксис Markdown (как на GitHub)
        expand=True,
    )

    # Функция для конвертации Markdown и отображения
    def convert_markdown():
        if markdown_input.value:
            print("Конвертируем Markdown текст: ", markdown_input.value)  # Проверка содержимого
            # Не требуется явное преобразование через markdown2, используем ft.Markdown напрямую
            markdown_display.value = markdown_input.value
            page.update()

    # Файловый селектор для открытия файла
    file_picker = ft.FilePicker(on_result=lambda e: None)
    page.overlay.append(file_picker)

    # Функция для открытия файла
    def open_file(e):
        print("Открываем диалог выбора файла...")
        file_picker.pick_files(allow_multiple=False)
        print("Диалог выбора файла вызван...")

    # Обработка открытия файла
    def on_file_open_result(e: ft.FilePickerResultEvent):
        global file_content
        print("Событие выбора файла сработало")
        print(f"Файлы: {e.files}")  # Проверка списка файлов
        if e.files:
            selected_file = e.files[0]
            print("Файл выбран: ", selected_file.name)
            try:
                # Чтение содержимого файла через путь
                with open(selected_file.path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                print("Содержимое файла:\n", file_content)  # Проверка содержимого файла
                markdown_input.value = file_content
                convert_markdown()  # Обновляем содержимое
                page.update()
            except Exception as ex:
                print(f"Ошибка открытия файла: {ex}")
        else:
            print("Файл не был выбран.")

    # Привязываем обработчик выбора файла
    file_picker.on_result = on_file_open_result

    # Кнопка для открытия файла
    open_button = ft.ElevatedButton("Открыть файл", icon=ft.icons.FOLDER_OPEN, on_click=open_file)

    # Добавляем элементы на страницу
    page.add(
        ft.Column(
            [
                open_button,
                markdown_input,
                markdown_display,  # Поле для отображения конвертированного текста
            ],
            expand=True,
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
        )
    )
def view_file():
    ft.app(target=main)
    return file_content
