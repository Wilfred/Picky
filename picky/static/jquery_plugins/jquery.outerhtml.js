/* outerHTML plugin for jQuery.
 *
 * From http://www.yelotofu.com/2008/08/jquery-outerhtml/ via
 * http://stackoverflow.com/a/2319259 .
 */
jQuery.fn.outerHTML = function(s) {
    return (s)
        ? this.before(s).remove()
        : jQuery("<p>").append(this.eq(0).clone()).html();
}
