// Javascript file used by the landing page post login
document.addEventListener('DOMContentLoaded', () => {

    // JS to highlight the selected tab
    $('#topheader .navbar-nav a').on('click', function () {
        $('#topheader .navbar-nav').find('li.active').removeClass('active');
        $(this).parent('li').addClass('active');
    });

    // function called when addtocart message is clicked post addition of toppings, this does ajax calls to see if the
    // number of toppings criteria is met for the item and then add the item to the cart.
    document.querySelector('#add_toppings').onclick = () => {

        var checkedBoxes = document.querySelectorAll('input[name=topping_selection]:checked');

        var selectionList = '';
        checkedBoxes.forEach(topping => {
            selectionList = selectionList + ',' + topping.value
        });
        const item_id = document.querySelector('input[name=item_hidden_id]').value;
        const cat_id = document.querySelector('input[name=cat_hidden_id]').value;
        const price_id = document.querySelector('input[name=price_hidden_id]').value;
        // Make a post request to add the item + toppings to the cart.
        $.post("add_item", {
            'item_id': item_id,
            'cat_id': cat_id,
            'price_id': price_id,
            'topping_list': selectionList
        })
            .done(function (data) {
                var obj = JSON.parse(data);
                // If there was an error show it on the UI
                if (obj.status === 'error') {
                    document.querySelector('#topping_error_msg').innerHTML = obj.message;
                } else {
                    // update the html elements.
                    document.querySelector('#topping_error_msg').innerHTML = '';
                    document.querySelector('#total_price_count').innerHTML = 'Cart Total( for ' + obj.item_count + ' item): ' + obj.total_price;
                    document.querySelector('#cart_item_count').innerHTML = 'Cart(' + obj.item_count + ')';
                    $('#toppingsModal').modal('hide')
                }
            });
        return false;
    };

// This function looks for all the items that have Customize button. Once this is clicked a modal dialog is opened post retrieving the toppings list from the server.
    document.querySelectorAll('.customizeitem').forEach(link => {
        link.onclick = () => {
            var $this = $(this);

            const item_id = link.dataset.itemId;
            const cat_id = link.dataset.categoryId;
            const price_id = link.dataset.priceId;
            const topping_list_url = "topping_list";

            // update html elements in the Modal dialogue with the item details.
            $('#modal_item_name').html('Item Name: ' + link.dataset.itemName);
            $('#modal_item_price').html('Item Price: ' + link.dataset.itemPrice);
            $('#modal_item_Size').html('Size: ' + link.dataset.itemSize);

            document.querySelector('#topping_error_msg').innerHTML = '';

            var myNode = document.getElementById("assetNameMenu");
            // remove any existing elements in the UI
            while (myNode.firstChild) {
                myNode.removeChild(myNode.firstChild);
            }
            // Add hidden elements for the information to be sent to the server.
            var assetList = $('#assetNameMenu');
            $('<input name="item_hidden_id" id="item_hidden_id"/>')
                .attr('type', 'hidden')
                .val(item_id)
                .appendTo(assetList);
            $('<input name="cat_hidden_id" id="cat_hidden_id"/>')
                .attr('type', 'hidden')
                .val(cat_id)
                .appendTo(assetList);
            $('<input name="price_hidden_id" id="price_hidden_id"/>')
                .attr('type', 'hidden')
                .val(price_id)
                .appendTo(assetList);
            // make a post request to get the toppings list
            $.post(topping_list_url, {'item_id': item_id, 'cat_id': cat_id, 'price_id': price_id})
                .done(function (data) {
                    var obj = JSON.parse(data);
                    //add all the toppings to the modal dialog
                    obj.forEach(function (item, index) {
                        // Add checkbos for each item.
                        var li = $('<li/>')
                            .addClass('ui-menu-item')
                            .attr('role', 'menuitem')
                            .appendTo(assetList);
                        var aaa = $('<a>')
                            .addClass('ui-all')
                            .appendTo(li);
                        var input = $('<input name="topping_selection" />')
                            .addClass('ui-all')
                            .attr('type', 'checkbox')
                            .val(item.topping_id)
                            .appendTo(aaa);
                        var aaaa = $('<span>')
                            .text(item.topping_name + ' $(' + item.topping_price + ')')
                            .appendTo(aaa);

                    });


                });
            //show the modal dialogue
            $('#toppingsModal').modal('show')
            return false;
        };
    });

    //iterate over all the Add buttons to make an AJAX call to add the item to session and update the UI for item count and item total
    document.querySelectorAll('.addtocart').forEach(link => {
        link.onclick = () => {
            var $this = $(this);

            const item_id = link.dataset.itemId;
            const cat_id = link.dataset.categoryId;
            const price_id = link.dataset.priceId;
            const add_cart_url = "add_item";
            // Make a call to add the item
            $.post(add_cart_url, {'item_id': item_id, 'cat_id': cat_id, 'price_id': price_id})
                .done(function (data) {
                    var obj = JSON.parse(data);
                    document.querySelector('#total_price_count').innerHTML = 'Cart Total( for ' + obj.item_count + ' item): ' + obj.total_price;
                    document.querySelector('#cart_item_count').innerHTML = 'Cart(' + obj.item_count + ')';
                });
            targ = $this.attr('data-target');
            return false;
        };
    });

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

});

// When the page is first loaded show the item list in the first tab
$(function () {
    $('#categoryList li:first-child a').tab('show')
});
