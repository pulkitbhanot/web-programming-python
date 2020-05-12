// Javascript file used across the app
document.addEventListener('DOMContentLoaded', () => {

    // JS to highlight the selected tab
    $('#topheader .navbar-nav a').on('click', function () {
        $('#topheader .navbar-nav').find('li.active').removeClass('active');
        $(this).parent('li').addClass('active');
    });

    // handle onclick event when the user lookup button is clicked only if this element is present in the current UI page
    var userLookupButton = document.getElementById('userlookup') !== null;
    if (userLookupButton) {
        // This function adds an onclick event to userlookup button. Once this is clicked a modal dialog is opened post
        // retrieving the list of unlinked users from the server.
        document.querySelectorAll('.userlookup').forEach(link => {
            link.onclick = () => {
                var $this = $(this);
                var myNode = document.getElementById("assetNameHiddenAttributes");
                // Add hidden elements for the information to be sent to the server.
                $('<input name="hidden_user_id" id="hidden_user_id"/>')
                    .attr('type', 'hidden')
                    .val(link.dataset.user)
                    .appendTo(myNode);
                var myNode = document.getElementById("assetNameMenu");
                // remove any existing elements in the UI
                while (myNode.firstChild) {
                    myNode.removeChild(myNode.firstChild);
                }
                $('#userLookupModal').modal('show');
                $("#add_linking").attr("disabled", true);
                return false;
            };
        });
    }


    // handle onclick event when the user search button is clicked only if this element is present in the current UI page
    var userLookupModalButton = document.getElementById('lookupusersonname') !== null;
    if (userLookupModalButton) {
        // This function adds an onclick event to user search button. It makes an AJAX call to the server and shows the response in the UI
        document.querySelectorAll('.lookupusersonname').forEach(link => {
            link.onclick = () => {
                var $this = $(this);
                var myNode = document.getElementById("assetNameMenu");
                // remove any existing elements in the UI
                while (myNode.firstChild) {
                    myNode.removeChild(myNode.firstChild);
                }

                const user_id = document.querySelector('input[name=hidden_user_id]').value;
                const search_string = document.querySelector('input[name=searchstring]').value;

                // Add hidden elements for the information to be sent to the server.
                var assetList = $('#assetNameMenu');
                $.post("lookup_unlinked_users", {
                    'user_id': user_id,
                    'search_string': search_string
                })
                    .done(function (data) {

                        var obj = JSON.parse(data);
                        // If there was an error show it on the UI
                        if (obj.status === 'error') {
                            document.querySelector('#user_error_msg').innerHTML = obj.message;
                        } else {
                            // update the html elements.
                            document.querySelector('#user_error_msg').innerHTML = '';
                            if (obj.user_list.length > 0) {
                                $("#add_linking").attr("disabled", false);
                            } else {
                                document.querySelector('#user_error_msg').innerHTML = 'No matching Customers found in the system.';
                            }
                            obj.user_list.forEach(function (item, index) {
                                // Add checkbos for each item.
                                var li = $('<li/>')
                                    .addClass('ui-menu-item')
                                    .attr('role', 'menuitem')
                                    .appendTo(assetList);
                                var aaa = $('<a>')
                                    .addClass('ui-all')
                                    .appendTo(li);
                                var input = $('<input name="user_selection" />')
                                    .addClass('ui-all')
                                    .attr('type', 'checkbox')
                                    .val(item.user_id)
                                    .appendTo(aaa);
                                var aaaa = $('<span>')
                                    .html('&nbsp;&nbsp;&nbsp;&nbsp;<b>' + item.business_name + '</b> (' + item.user_email + ')' + '</b> (' + item.user_address + ')')
                                    .appendTo(aaa);
                            });
                        }
                    });
                return false;
            };
        });

    }

    // Handle clicking of Link user button the UI
    var userLinkModalButton = document.getElementById('add_linking') !== null;
    if (userLinkModalButton) {
        document.querySelectorAll('.add_linking').forEach(link => {

            link.onclick = () => {
                var checkedBoxes = document.querySelectorAll('input[name=user_selection]:checked');

                var selectionList = '';
                checkedBoxes.forEach(topping => {
                    selectionList = selectionList + ',' + topping.value
                });
                $.post("add_customer_linking", {
                    'user_list': selectionList
                })
                    .done(function (data) {
                        var obj = JSON.parse(data);
                        // If there was an error show it on the UI
                        if (obj.status === 'error') {
                            document.querySelector('#user_error_msg').innerHTML = obj.message;
                        } else {
                            // update the html elements.
                            document.querySelector('#user_error_msg').innerHTML = '';
                            $('#userLookupModal').modal('hide');
                            window.location.reload();
                        }
                    });
                return false;
            }
        });
    }

    // Change the show item list based on the tab clicked on.
    $('[data-toggle="tab"]').click(function (e) {
        var $this = $(this),
            loadurl = $this.attr('data-url'),

            targ = $this.attr('data-target');
        $this.tab('show');
        return false;
    });

    // Code to handle CSRF tokens
    var csrftoken = Cookies.get('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Code to handle the add invoice item button in the UI
    var counter = 0;
    var addRowButton = document.getElementById('addrow') !== null;
    if (addRowButton) {

        $("#addrow").on("click", function () {
            var newRow = $('<tr class="row">');
            var cols = "";

            cols += '<td style="width: 60%;"><input type="text" class="form-control" name="description' + counter + '"/></td>';
            cols += '<td style="width: 13%;"><input type="number" class="form-control" name="price' + counter + '" step=".01"/></td>';

            cols += '<td style="width: 17%;"><div class="custom-file"><input type="file" class="form-control" accept="application/pdf" id="inputgroupgile' + counter + '" name="inputgroupfile' + counter + '" aria-describedby="inputgroupgileaddon01"></div></td>';

            cols += '<td style="width: 10%;" align="center"><input type="button" class="ibtnDel btn btn-md btn-danger delete-item"  value="Delete"></td>';
            newRow.append(cols);
            $("table.order-list").append(newRow);
            counter++;
            document.querySelector('#row_count').value = counter;
        });
    }

    $("table.order-list").on("click", ".ibtnDel", function (event) {
        $(this).closest("tr").remove();
        counter -= 1
        document.querySelector('#row_count').value = counter;
    });

    // Code to set the date option for the item
    var date_input = $('input[name="date"]'); //our date input has the name "date"
    var container = $('.bootstrap-iso form').length > 0 ? $('.bootstrap-iso form').parent() : "body";
    var options = {
        format: 'yyyy-mm-dd',
        container: container,
        todayHighlight: true,
        autoclose: true,
    };
    date_input.datepicker(options);
});

// When the page is first loaded show the item list in the first tab
$(function () {
    $('#categoryList li:first-child a').tab('show')
});


