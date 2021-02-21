$(document).ready(function () {
    // Init
    $('#submit-btn').hide();


    $("#imageUpload").change(function () {

        $('#submit-btn').show();
        readURL(this)

    });


function readURL(input) {
if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
        $('#previewimage')
            .attr('src', e.target.result)
            .width(800)
            .height(600);
    };

    reader.readAsDataURL(input.files[0]);
}
}

});