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

    /* from http://stackoverflow.com/a/6238456 */
    function isExternal(url) {
        var match = url.match(/^([^:\/?#]+:)?(?:\/\/([^\/?#]*))?([^?#]+)?(\?[^#]*)?(#.*)?/);
        if (typeof match[1] === "string" && match[1].length > 0 && match[1].toLowerCase() !== location.protocol) {
            return true;
        }
        if (typeof match[2] === "string" && match[2].length > 0 && match[2].replace(new RegExp(":("+{"http:":80,"https:":443}[location.protocol]+")?$"), "") !== location.host) {
            return true;
        }
        return false;
    }

    function showPreview() {
        var pageSource =  $("#id_content").val();

        var $preview = $("#preview");
        $preview.html(creoleToHtml(pageSource));

        $preview.trigger('previewChanged');
    }

    // add favicons after the preview is rendered
    var $preview = $("#preview");
    $preview.on('previewChanged', function() {
        $('#preview a').each(function() {
            var $a = $(this),
                url = $a.attr('href'),
                iconUrl;

            if (isExternal(url)) {
                iconUrl = "//getfavicon.appspot.com/" + encodeURIComponent(url);
                $a.before('<img class="favicon" src="' + iconUrl + '">');
            }

        });
    });

    // render the content on initial pageload
    showPreview();

    // update the preview whenever the source changes
    $("#id_content").keyup(showPreview);

})();
