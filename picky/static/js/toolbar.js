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

    $('.toolbar .h1').click(function() {
        $content.insertAtCaret('= heading =');

        // update the preview
        $content.trigger('keyup');
    });

    $('.toolbar .h2').click(function() {
        $content.insertAtCaret('== Sub-heading ==');

        // update the preview
        $content.trigger('keyup');
    });

    $('.toolbar .h3').click(function() {
        $content.insertAtCaret('=== Sub-sub-heading ===');

        // update the preview
        $content.trigger('keyup');
    });

})();
