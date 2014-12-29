(function(){
    "use strict";
    var $preview = $("#preview"),
        knownUrls = [];
    
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

        $('#preview-wrapper').show();
    }

    /* Asychronously update our known URLs, as other pages may have
     * been created whilst we're editing.
     */
    function updateKnownUrls() {
        $.ajax("/all_pages/urls/").done(function(urls) {
            knownUrls = urls;

            $preview.trigger('previewChanged');
        });
    }

    // get the known URLs, and update them every 30 seconds
    updateKnownUrls();
    setInterval(updateKnownUrls, 30*1000);

    function endsWith(str, suffix) {
        return str.indexOf(suffix, str.length - suffix.length) !== -1;
    }

    $preview.on('previewChanged', function() {
        showPreview();
        
        // add favicons after the preview is rendered
        $('#preview a').each(function() {
            var $a = $(this),
                url = $a.attr('href'),
                iconUrl;

            if (isExternal(url)) {
                iconUrl = "//www.google.com/s2/favicons?domain=" + encodeURIComponent(url);
                $a.after('<img class="favicon" src="' + iconUrl + '">');
            }
        });

        // highlight nonexistent urls
        $('#preview a').each(function() {
            var $a = $(this),
                url = $a.attr('href');

            if (!endsWith(url, "/")) {
                url = url + "/";
            }

            if (!isExternal(url) && !_.contains(knownUrls, url) && !_.isEmpty(knownUrls)) {
                $a.addClass('nonexistent');
            } else {
                $a.removeClass('nonexistent');
            }
        });

    });

    // render the content on initial pageload
    $preview.trigger('previewChanged');

    // update the preview whenever the source changes
    $("#id_content").keyup(function() {
        $preview.trigger('previewChanged');
    });

})();
