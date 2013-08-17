(function(){
    "use strict";

    var $content = $('#id_content');

    // We only show the toolbar if JS is available.
    $('.toolbar').show();

    $('.toolbar .bold').click(function() {
        $content.insertAtCaret('**bold text**');

        // update the preview
        $content.trigger('keyup');
    });

    $('.toolbar .italic').click(function() {
        $content.insertAtCaret('//italic text//');

        // update the preview
        $content.trigger('keyup');
    });

})();
