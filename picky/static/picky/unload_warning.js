(function() {
    $(document).ready(function() {
        // Store the initial value on all element that we've been
        // asked to check.
        $(".warn-on-unload").each(function() {
            var $input = $(this);
            $input.data("initial-value", $input.val());
        });
    });

    var submittingForm = false;

    $('form').submit(function() {
        submittingForm = true;
    });

    window.onbeforeunload = function() {
        // If the user tries to navigate away with unsaved changed,
        // confirm that's what they want to do.
        if (!submittingForm) {

            var unsavedChanges = false;
            
            $(".warn-on-unload").each(function() {
                var $input = $(this);
                if ($input.val() !== $input.data("initial-value")) {
                    unsavedChanges = true;
                    return false; // break
                }
            });

            if (unsavedChanges) {
                return 'You have unsaved edits, are you sure you want to leave?';
            }
        }
    };
    
})();
