(function(){
    "use strict";

    var $content = $('#id_content');

    function insert(text) {
        $content.insertAtCaret(text);

        // update the preview
        $content.trigger('keyup');
    }

    // We only show the toolbar if JS is available.
    $('.toolbar').show();

    $('.toolbar .bold').click(function() {
        insert('**bold text**');
    });

    $('.toolbar .italic').click(function() {
        insert('//italic text//');
    });

    $('.toolbar .h1').click(function() {
        insert('= heading =');
    });

    $('.toolbar .h2').click(function() {
        insert('== Sub-heading ==');
    });

    $('.toolbar .h3').click(function() {
        insert('=== Sub-sub-heading ===');
    });

})();
