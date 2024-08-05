$(document).ready(function() {
    // Variable para almacenar el modo de traducción actual
    var mode = 'text';

    // Manejar el evento de clic para el botón de traducir texto
    $('#translate_text_btn').on('click', function() {
        mode = 'text';

        // Actualizar el área de entrada para aceptar texto
        $('#input_area').html(
            '<label for="input_area" class="form-label">Inglés</label>' +
            '<textarea id="text" name="text" class="form-control" rows="6"></textarea>');

        // Actualizar el área de salida para mostrar la traducción de texto
        $('#output_area').html(
            '<label for="output_area" class="form-label">Francés</label>' + 
            '<textarea id="translated_text" name="translated_text" class="form-control" rows="6" readonly></textarea>');

        // Llamar a la función de traducción cuando el usuario ingrese texto
        $('#text').on('input', translateText);
    });

    // Manejar el evento de clic para el botón de traducir imagen
    $('#translate_image_btn').on('click', function() {
        mode = 'image';
        
        // Actualizar el área de entrada para aceptar una imagen
        $('#input_area').html(
            '<label for="input_area" class="form-label">Inglés</label>' +
            '<input type="file" id="upload_image" name="file" class="form-control" accept="image/*">' +
            '<div id="image_preview" class="mt-3"></div>'
        );
        
        // Actualizar el área de salida para mostrar la traducción del texto extraído de la imagen
        $('#output_area').html(
            '<label for="output_area" class="form-label">Francés</label>' + 
            '<textarea id="translated_image_preview" name="translated_image_preview" class="form-control" rows="6" readonly></textarea>');
        
        // Llamar a la función de carga de imagen cuando el usuario seleccione una imagen
        $('#upload_image').on('change', uploadImage);
    });

    // Manejar el evento de clic para el botón de traducir audio
    $('#translate_audio_btn').on('click', function() {
        mode = 'audio';

        // Actualizar el área de entrada para aceptar un archivo de audio
        $('#input_area').html(
            '<label for="input_area" class="form-label">Inglés</label>' +
            '<input type="file" id="upload_audio" name="audio" class="form-control" accept="audio/*">' +
            '<div id="audio_preview" class="mt-3"></div>'
        );

        // Actualizar el área de salida para mostrar la traducción del texto extraído del audio
        $('#output_area').html(
            '<label for="output_area" class="form-label">Francés</label>' + 
            '<textarea id="translated_audio_text" name="translated_audio_text" class="form-control" rows="6" readonly></textarea>');

        // Llamar a la función de carga de audio cuando el usuario seleccione un archivo de audio
        $('#upload_audio').on('change', uploadAudio);
    });

    // Función para traducir texto
    function translateText() {
        var text = $('#text').val();
        $.ajax({
            url: '/translate',
            type: 'POST',
            data: { text: text },
            success: function(data) {
                $('#translated_text').val(data.translated_text);
            }
        });
    }

    // Función para cargar y traducir una imagen
    function uploadImage() {
        var formData = new FormData();
        formData.append('file', $('#upload_image')[0].files[0]);
    
        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                console.log('Image preview URL:', data.image_url);
                console.log('Extracted text:', data.extracted_text);
    
                // Mostrar la imagen cargada
                $('#image_preview').html('<img src="' + data.image_url + '" class="img-fluid" alt="Uploaded Image">');

                // Mostrar el texto extraído de la imagen
                $('#translated_image_preview').val(data.extracted_text);
    
                // Llamar a translateImageText para traducir el texto extraído
                translateImageText(data.extracted_text);
            }
        });
    }
    
    // Función para traducir el texto extraído de una imagen
    function translateImageText(text) {
        $.ajax({
            url: '/translate',
            type: 'POST',
            data: { text: text },
            success: function(data) {
                $('#translated_image_preview').val(data.translated_text);
            }
        });
    }

    // Función para cargar y traducir un archivo de audio
    function uploadAudio() {
        var formData = new FormData();
        formData.append('audio', $('#upload_audio')[0].files[0]);
    
        $.ajax({
            url: '/upload_audio',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {

                // Mostrar el audio cargado
                $('#audio_preview').html('<audio controls src="' + data.audio_url + '"></audio>');

                // Mostrar el texto extraído del audio
                $('#translated_audio_text').val(data.original_text);
    
                // Llamar a translateAudio para traducir el texto extraído
                translateAudio();
            }
        });
    }
    
    // Función para traducir el texto extraído de un archivo de audio
    function translateAudio() {
        var text = $('#translated_audio_text').val();
        $.ajax({
            url: '/translate_audio',
            type: 'POST',
            data: { text: text },
            success: function(data) {
                $('#translated_audio_text').val(data.translated_text);
            }
        });
    }
    
});
