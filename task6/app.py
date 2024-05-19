from flask import Flask, request, render_template, url_for, redirect, flash, send_file
from PIL import Image, ImageEnhance
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# храненим инфу текущего и скорректированного изображения
current_image = None
adjusted_image = None

# значения слайдеров
brightness_value = 1.0
contrast_value = 1.0
sharpness_value = 1.0

@app.route('/', methods=['GET', 'POST'])
def index():
    global current_image, adjusted_image
    global brightness_value, contrast_value, sharpness_value

    if request.method == 'POST':
        # Проверка, была ли нажата кнопка сброса
        if 'reset' in request.form:
            # Сброс значений слайдеров до исходных
            brightness_value = 1.0
            contrast_value = 1.0
            sharpness_value = 1.0
            flash("Значения слайдеров сброшены.")
            return redirect(url_for('index'))

        # Загрузка нового изображения
        uploaded_file = request.files.get('image')
        if uploaded_file and uploaded_file.filename != '':
            # Открытие и сохранение загруженного изображения
            current_image = Image.open(uploaded_file)
            adjusted_image = current_image

        # Получение значений яркости, контрастности и резкости из формы
        brightness_value = float(request.form.get('brightness', 1.0))
        contrast_value = float(request.form.get('contrast', 1.0))
        sharpness_value = float(request.form.get('sharpness', 1.0))

        if current_image:
            # Создание копии текущего изображения для коррекции
            image = current_image

            # Коррекция яркости
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(brightness_value)

            # Коррекция контрастности
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(contrast_value)

            # Коррекция резкости
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(sharpness_value)

            # Сохранение скорректированного изображения
            adjusted_image = image
            flash("Изображение успешно скорректировано.")

        return redirect(url_for('index'))

    # Отображение страницы с формой и текущим состоянием изображения
    return render_template(
        'index.html',
        image_url=url_for('display_image') if adjusted_image else None,
        brightness_value=brightness_value,
        contrast_value=contrast_value,
        sharpness_value=sharpness_value
    )

@app.route('/display')
def display_image():
    if adjusted_image:
        # Конвертация изображения в формат, пригодный для отправки в ответе
        img_io = BytesIO()
        adjusted_image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    return '', 404

if __name__ == '__main__':
    app.run(debug=True)
