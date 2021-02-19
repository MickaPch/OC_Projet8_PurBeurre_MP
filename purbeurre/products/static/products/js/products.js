
$(".product-link").click(function(e) {
    e.preventDefault();
    var this_link = $(this);
    var form = $(this).parent();
    var code = $(this).find('.code').val();
    var code_input = form.find('input[name="product_code"]');
    code_input.val(code);
    form.submit()
});