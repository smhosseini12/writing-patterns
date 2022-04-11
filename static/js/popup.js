if (!window.x) {
    x = {};
}

x.Selector = {};
x.Selector.getSelected = function() {
    var t = '';
    if (window.getSelection) {
        t = window.getSelection();
    } else if (document.getSelection) {
        t = document.getSelection();
    } else if (document.selection) {
        t = document.selection.createRange().text;
    }
    return t;
}

var pageX;
var pageY;
var selectedText;
var ID;

$(document).ready(function() {
    $(document).bind("mouseup", function() {
        selectedText = x.Selector.getSelected();
        if(selectedText != ''){
            $('.tools').css({
                'left': pageX - 50,
                'top' : pageY - 65
            }).fadeIn(200);
        } else {
            $('.tools').fadeOut(200);
        }
    });
    $(document).on("mousedown", function(e){
        if ($(e.target).hasClass('selectable')) {
            pageX = e.pageX;
            pageY = e.pageY;
        }
        
    });
});

function set_ID(clickedID){
    ID=clickedID;
}

function Copy2Clipboard(clickedelement) {

    navigator.clipboard.writeText(selectedText.toString());
    var element = document.getElementById('refbutton'+ID);
    clickedelement.value=element.value;
    $('.tools').fadeOut(200);
  }