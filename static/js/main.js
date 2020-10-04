$(function () {
  $('[data-toggle="popover"]').popover({trigger: 'hover', placement: 'right',
  boundary: 'viewport', html: true, animation: false});
  $('[data-toggle="popover-cover"]').popover({trigger: "hover", placement: "right",
  boundary: 'viewport', title: "Deck Information", html: true, template: '<div class="popover" style="width: 35em" role="tooltip"><div class="arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>'});
});

// Use hidden text field in DOM to copy deck code to clipboard
function copyDeckCode() {
  var copyText = document.getElementById("deck-code");

  copyText.select();
  copyText.setSelectionRange(0, 99999); /*For mobile devices*/

  copy_button = document.getElementById("copy-button");

  copy_button.innerText = "Copied!";

  setTimeout(function(){ copy_button.innerText = "Copy Deck Code"; }, 3000);

  document.execCommand("copy");
}

// TODO: Change this logic, may have unintended effects in tab focus
// Keep deck code button from being visibly focused when clicked
$('#deck-code-button').on({
    focus: function () {
        $(this).blur();
    }
});
