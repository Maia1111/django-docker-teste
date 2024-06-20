document.getElementById('foto').addEventListener('change', function(event) {
    var imgPreview = document.getElementById('imgPreview');
    var file = event.target.files[0];
    var reader = new FileReader();

    reader.onload = function(e) {
        imgPreview.src = e.target.result;
        imgPreview.style.display = 'block';
    }

    if (file) {
        reader.readAsDataURL(file);
    }
});