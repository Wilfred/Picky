function creoleToHtml(creoleSource) {
    var parser = new creole({
        linkFormat: '/page/'
    });

    var div = document.createElement('div');
    parser.parse(div, creoleSource);

    return div.innerHTML;
}

function showPreview() {
    var pageSource =  $("#id_content").val();

    var $preview = $("#preview");
    $preview.html(creoleToHtml(pageSource));
}

$(document).ready(function() {
    $("#id_content").keyup(showPreview);
});
