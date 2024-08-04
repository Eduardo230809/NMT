$(document).ready(function() {
    var mode = 'text';

    $('#translate_text_btn').on('click', function() {
        mode = 'text';
        $('#input_area').html('<textarea id="text" name="text" class="form-control" rows="6"></textarea>');
        $('#output_area').html('<textarea id="translated_text" name="translated_text" class="form-control" rows="6" readonly></textarea>');
        $('#text').on('input', translateText);
    });

    $('#translate_image_btn').on('click', function() {
        mode = 'image';
        $('#input_area').html(
            '<input type="file" id="upload_image" name="file" class="form-control" accept="image/*">' +
            '<div id="image_preview" class="mt-3"></div>'
        );
        $('#output_area').html('<textarea id="translated_image_preview" name="translated_image_preview" class="form-control" rows="6" readonly></textarea>');
        $('#upload_image').on('change', uploadImage);
    });

    $('#translate_audio_btn').on('click', function() {
        mode = 'audio';
        $('#input_area').html(
            '<input type="file" id="upload_audio" name="audio" class="form-control" accept="audio/*">' +
            '<div id="audio_preview" class="mt-3"></div>'
        );
        $('#output_area').html('<textarea id="translated_audio_text" name="translated_audio_text" class="form-control" rows="6" readonly></textarea>');

        $('#upload_audio').on('change', uploadAudio);
    });

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
    
                $('#image_preview').html('<img src="' + data.image_url + '" class="img-fluid" alt="Uploaded Image">');
                $('#translated_image_preview').val(data.extracted_text);
    
                // Llamar a translateImageText para traducir el texto extraído
                translateImageText(data.extracted_text);
            }
        });
    }
    
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
                $('#audio_preview').html('<audio controls src="' + data.audio_url + '"></audio>');
                $('#translated_audio_text').val(data.original_text);
    
                // Llamar a translateAudio para traducir el texto extraído
                translateAudio();
            }
        });
    }
    
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
