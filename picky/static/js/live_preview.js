(function(){
    "use strict";
    
    function creoleToHtml(creoleSource) {
        /* Return the creole source rendered to html.
         *
         * We wrap the output in a div tag, so we can easily use it
         * with jQuery.
         */
        var parser = new creole({
            linkFormat: '/page/'
        });

        var div = document.createElement('div');
        parser.parse(div, creoleSource);

        return $(div).outerHTML();
    }

    function showPreview() {
        var pageSource =  $("#id_content").val();

        var $preview = $("#preview");
        $preview.html(creoleToHtml(pageSource));
    }

    $(document).ready(function() {
        $("#id_content").keyup(showPreview);
    });

})();
