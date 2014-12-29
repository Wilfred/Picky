(function(){
    "use strict";

    var $content = $('#id_content');

    function insert(text) {
        $content.insertAtCaret(text);

        // update the preview
        $content.trigger('keyup');
    }

    // We only show the editing toolbar if JS is available.
    $('.button-toolbar').show();

    $('.button-toolbar .bold').click(function() {
        insert('**bold text**');
    });

    $('.button-toolbar .italic').click(function() {
        insert('//italic text//');
    });

    $('.button-toolbar .h1').click(function() {
        insert('= heading =');
    });

    $('.button-toolbar .h2').click(function() {
        insert('== Sub-heading ==');
    });

    $('.button-toolbar .h3').click(function() {
        insert('=== Sub-sub-heading ===');
    });

})();
