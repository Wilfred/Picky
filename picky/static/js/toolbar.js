(function(){
    "use strict";

    var $content = $('#id_content');

    function insert(text) {
        $content.insertAtCaret(text);

        // update the preview
        $content.trigger('keyup');
    }

    // We only show the toolbar if JS is available.
    $('.btn-toolbar').show();

    $('.btn-toolbar .bold').click(function() {
        insert('**bold text**');
    });

    $('.btn-toolbar .italic').click(function() {
        insert('//italic text//');
    });

    $('.btn-toolbar .h1').click(function() {
        insert('= heading =');
    });

    $('.btn-toolbar .h2').click(function() {
        insert('== Sub-heading ==');
    });

    $('.btn-toolbar .h3').click(function() {
        insert('=== Sub-sub-heading ===');
    });

})();
