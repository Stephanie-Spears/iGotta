/*globals $:false */
var myScripts = function(){
    'use strict';

    $(".errorpage").closest("body").addClass("alert-warning");

    var warninglevel1 = 'alert-warning';
    var warninglevel2 = 'alert-danger';
    var warning = true;
    setInterval(function(){
        $(".errorpage").closest("body").toggleClass((warning ? warninglevel2 : warninglevel1));
    }, 9000);

}();