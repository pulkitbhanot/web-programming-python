// This js function is used to show a pop-up dialog for private channels list to share the link to add someone for the chat
function copyURL(channel_id, channel_name) {


    var newURL = window.location.protocol + "//" + window.location.host;
    var shareable_url = newURL.concat('/connect_channel?channel_id=', channel_id, '&channel_type=', channel_name);


    /** Following code is just copy the url to the clipboard **/

    var textArea = document.createElement("textarea");

    // Below code is referenced from https://stackoverflow.com/questions/400212/how-do-i-copy-to-the-clipboard-in-javascript

    // Place in top-left corner of screen regardless of scroll position.
    textArea.style.position = 'fixed';
    textArea.style.top = 0;
    textArea.style.left = 0;

    // Ensure it has a small width and height. Setting to 1px / 1em
    // doesn't work as this gives a negative w/h on some browsers.
    textArea.style.width = '2em';
    textArea.style.height = '2em';

    // We don't need padding, reducing the size if it does flash render.
    textArea.style.padding = 0;

    // Clean up any borders.
    textArea.style.border = 'none';
    textArea.style.outline = 'none';
    textArea.style.boxShadow = 'none';

    // Avoid flash of white box if rendered for any reason.
    textArea.style.background = 'transparent';


    textArea.value = shareable_url;

    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();


    /* Copy the text inside the text field */
    document.execCommand("copy");

    /* Alert the copied text */
    alert("Please share the URL: " + textArea.value + " .This has already been copied on your clipboard");
}