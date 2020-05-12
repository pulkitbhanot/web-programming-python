// Javascrpt file with all the functions for view cart screen
document.addEventListener('DOMContentLoaded', () => {

    $('#topheader .navbar-nav a').on('click', function () {
        $('#topheader .navbar-nav').find('li.active').removeClass('active');
        $(this).parent('li').addClass('active');
    });

    // function to make the ajax call to clear the cart on the server and in teh browser
    document.getElementById('clearcart').onclick = function () {
        $.post('clear_cart')
            .done(function (data) {
                var obj = JSON.parse(data);
                const new_item_count = parseInt(obj.item_count);
                document.querySelector('#total_price_count').innerHTML = 'Cart Total( for ' + obj.item_count + ' item): ' + obj.total_price;
                document.querySelector('#cart_item_count').innerHTML = 'Cart(' + obj.item_count + ')';

                if (new_item_count == 0) {
                    document.getElementById('carttable').style.display = 'none';
                    document.getElementById('clearcart').style.display = 'none';
                    document.getElementById('placeorder').style.display = 'none';
                }
            });
    };

    // function to make the ajax call to place an order with all the items in the cart, redirects the user on successful creation of order
    document.getElementById('placeorder').onclick = function () {
        $.post('place_order')
            .done(function (data) {
                var obj = JSON.parse(data);
                if (obj.status === 'success') {
                    document.querySelector('#total_price_count').innerHTML = 'Cart Total( for ' + obj.item_count + ' item): ' + obj.total_price;
                    document.querySelector('#cart_item_count').innerHTML = 'Cart(' + obj.item_count + ')';
                    document.getElementById('carttable').style.display = 'none';
                    document.getElementById('clearcart').style.display = 'none';
                    document.getElementById('placeorder').style.display = 'none';
                    alert('Order Successfully placed. Order id for reference is ' + obj.order_id);
                    window.location.href = '/';
                } else {
                    alert('Unknown error occured when placing an order, please contact us at 1800-my-help')
                }
            });
    };

    // function to make the ajax call when an individual item is removed from the cart
    document.querySelectorAll('.removefromcart').forEach(link => {
        link.onclick = () => {
            const item_id = link.dataset.itemId;
            const cat_id = link.dataset.categoryId;
            const item_unique_id = link.dataset.itemUniqueId;
            const delete_item = "delete_item";
            $.post(delete_item, {'item_id': item_id, 'cat_id': cat_id, 'item_unique_id': item_unique_id})
                .done(function (data) {
                    var obj = JSON.parse(data);
                    var row = document.getElementById('row' + item_unique_id);
                    row.style.display = 'none';
                    const new_item_count = parseInt(obj.item_count);
                    document.querySelector('#total_price_count').innerHTML = 'Cart Total( for ' + obj.item_count + ' item): ' + obj.total_price;
                    document.querySelector('#cart_item_count').innerHTML = 'Cart(' + obj.item_count + ')';

                    if (new_item_count == 0) {
                        document.getElementById('carttable').style.display = 'none';
                        document.getElementById('clearcart').style.display = 'none';
                        document.getElementById('placeorder').style.display = 'none';
                    }
                });
            return false;
        };
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
