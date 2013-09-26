(function() {
    "use strict";

    var $tocHeading = $('.table-of-contents h3');

    if ($tocHeading.length) {
        $tocHeading.replaceWith(
            '<h3><a id="collapse-toc">Table Of Contents <i id="collapse-icon" class="icon-minus"></i></a></h3>');

        $('#collapse-toc').click(function() {
            $('.table-of-contents ul').slideToggle();

            $('#collapse-icon')
                .toggleClass('icon-plus')
                .toggleClass('icon-minus');
        });
    }

})();
